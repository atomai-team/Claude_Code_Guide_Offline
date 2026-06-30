#!/usr/bin/env python3
"""board-bridge.py · v7 micro-server · 端口 18767

功能:
- 接收 dashboard POST 写回请求 (update_status / add_note / create_task)
- 调 lib/board.py 子命令写回 (board.py 自动原子写 + 投影)
- 返回 JSON 结果给 dashboard

启动: python3 bin/board-bridge.py [--port 18767]

约束:
- 端口 18767 唯一可用 (18765=Playwright / 18766=dashboard conftest)
- 单用户 lockfile: ~/.omc/snapshots/board-bridge.lock
- 反讽 R1: 直写 board-tasks.json 违反单向投影 → 必须走 board.py
- 反讽 R5: board.py 子命令为 done/doing/todo/partial/block/note/add (无通用 update)
  → micro-server 仅支持这些操作, 跨字段更新通过 add_note 或重写 strategy
- 实际数据 SSoT: docs/project-ledger.json (board-tasks.json 是只读投影)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BOARD_PY = os.path.expanduser("~/.claude/lib/board.py")
LOCKFILE = os.path.expanduser("~/.omc/snapshots/board-bridge.lock")

# CORS 白名单 (reviewer P2 加固): 原 Allow-Origin:* 任何本地网页可跨域 POST,
# 收窄到已知 dashboard 来源 (18766 serve-gzip / 18765 Playwright / 18771 旧端口 / 18767 自身)。
ALLOWED_ORIGINS = {
    "http://127.0.0.1:18766", "http://localhost:18766",
    "http://127.0.0.1:18765", "http://127.0.0.1:18771",
    "http://127.0.0.1:18767",
}


def _run_board_py(*args):
    """调 board.py 子命令 → 返回 (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            [sys.executable, BOARD_PY, *args],
            capture_output=True, text=True, timeout=30,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", f"board.py 调用异常: {e}"


def _acquire_lock():
    """单用户 lockfile (atomic · 防止并发写)."""
    os.makedirs(os.path.dirname(LOCKFILE), exist_ok=True)
    try:
        fd = os.open(LOCKFILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.write(fd, f"{os.getpid()}\n{time.time()}\n".encode())
        os.close(fd)
        return True
    except FileExistsError:
        # 已存在 lockfile, 检查是否过期 (>5min 视为过期)
        try:
            mtime = os.path.getmtime(LOCKFILE)
            if time.time() - mtime > 300:
                os.remove(LOCKFILE)
                return _acquire_lock()
        except Exception:
            pass
        return False


def _release_lock():
    """释放 lockfile (best-effort)."""
    try:
        os.remove(LOCKFILE)
    except Exception:
        pass


class BridgeHandler(BaseHTTPRequestHandler):
    """HTTP handler · 仅接受 POST /api/board/<action>."""

    def log_message(self, fmt, *args):
        """静默默认 access log (避免刷屏)."""
        sys.stderr.write(f"[bridge] {fmt % args}\n")

    def _allow_origin(self):
        """CORS: 回显白名单内 Origin, 否则默认 dashboard 18766 (拒绝未知来源跨域)。"""
        origin = self.headers.get("Origin", "")
        return origin if origin in ALLOWED_ORIGINS else "http://127.0.0.1:18766"

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", self._allow_origin())
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self._allow_origin())
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if not self.path.startswith("/api/board/"):
            self._json_response(404, {"error": "not_found", "path": self.path})
            return

        action = self.path.split("/")[-1].lower()
        # board.py 子命令映射: update_status → done/doing/todo/partial/block
        #                    add_note / create_task → add (新增) / note (自由文本)
        if action not in ("update_status", "add_note", "create_task", "health"):
            self._json_response(400, {"error": "invalid_action", "action": action})
            return

        if action == "health":
            self._json_response(200, {"ok": True, "service": "board-bridge"})
            return

        # 读 body
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception as e:
            self._json_response(400, {"error": "invalid_json", "detail": str(e)})
            return

        if not _acquire_lock():
            self._json_response(423, {"error": "locked", "detail": "board.py 正在被其他进程使用"})
            return

        try:
            if action == "update_status":
                # board.py <status> <id> (status=todo/doing/done/partial/block)
                status = body.get("status", "todo")
                task_id = body.get("id", "")
                if status not in ("todo", "doing", "done", "partial", "block"):
                    self._json_response(400, {"error": "invalid_status", "status": status})
                    return
                args = [status, task_id]
                ok, out, err = _run_board_py(*args)

            elif action == "add_note":
                # board.py note <思考/决策文本>
                note_text = body.get("text", "")
                if not note_text:
                    self._json_response(400, {"error": "empty_note"})
                    return
                ok, out, err = _run_board_py("note", note_text)

            elif action == "create_task":
                # board.py add <req|wbs|subplan|milestone> <id> <标题>
                task_type = body.get("type", "req")
                task_id = body.get("id", "")
                task_title = body.get("title", "")
                if not task_id or not task_title:
                    self._json_response(400, {"error": "missing_id_or_title"})
                    return
                ok, out, err = _run_board_py("add", task_type, task_id, task_title)

            else:
                self._json_response(400, {"error": "unhandled", "action": action})
                return

            if ok:
                self._json_response(200, {"ok": True, "action": action, "stdout": out.strip()[:500]})
            else:
                self._json_response(500, {"ok": False, "action": action, "error": err.strip()[:500]})
        finally:
            _release_lock()


def main():
    parser = argparse.ArgumentParser(description="v7 board-bridge micro-server")
    parser.add_argument("--port", type=int, default=18767, help="监听端口 (默认 18767)")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址 (默认 127.0.0.1)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), BridgeHandler)
    print(f"[bridge] 🚀 board-bridge 启动: http://{args.host}:{args.port}", flush=True)
    print(f"[bridge] board.py: {BOARD_PY}", flush=True)
    print(f"[bridge] lockfile: {LOCKFILE}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[bridge] 退出")
        server.shutdown()


if __name__ == "__main__":
    main()