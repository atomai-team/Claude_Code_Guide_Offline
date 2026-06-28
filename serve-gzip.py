#!/usr/bin/env python3
"""
GzipHTTPRequestHandler · 替代 Python SimpleHTTPServer 支持 gzip 压缩
· 零依赖 · Python 3.14 兼容 · 自动检测 Accept-Encoding
· 端口 18766(避开 18765 当前 SimpleHTTPServer)
· 启动：python3 serve-gzip.py [PORT] [--dir DIR]
· 修复版 v2：完整重写 do_GET，headers 在 body 之前正确发送
"""

import sys
import os
import gzip
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote


COMPRESSIBLE_TYPES = (".html", ".css", ".js", ".json", ".svg", ".txt", ".md")


class GzipHTTPRequestHandler(BaseHTTPRequestHandler):
    """完整重写：先 send_response + headers，再发 body（含可选 gzip）"""

    server_version = "GzipHTTP/1.0"

    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory or os.getcwd()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return

        # MIME type
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "application/octet-stream"

        # 读 body
        with open(path, "rb") as f:
            body = f.read()

        # 决定是否 gzip
        accept_encoding = self.headers.get("Accept-Encoding", "").lower()
        will_gzip = "gzip" in accept_encoding and path.endswith(COMPRESSIBLE_TYPES)
        if will_gzip:
            body = gzip.compress(body, compresslevel=6)
            encoding = "gzip"
        else:
            encoding = None

        # Last-Modified
        import datetime
        mtime = os.path.getmtime(path)
        last_modified = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 发响应
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Last-Modified", last_modified)
        if encoding:
            self.send_header("Content-Encoding", encoding)
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        """HEAD = GET without body · curl -I 用得到"""
        # 复用 do_GET 流程但跳过 wfile.write
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return

        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "application/octet-stream"

        with open(path, "rb") as f:
            body = f.read()

        accept_encoding = self.headers.get("Accept-Encoding", "").lower()
        will_gzip = "gzip" in accept_encoding and path.endswith(COMPRESSIBLE_TYPES)
        if will_gzip:
            body = gzip.compress(body, compresslevel=6)
            encoding = "gzip"
        else:
            encoding = None

        import datetime
        mtime = os.path.getmtime(path)
        last_modified = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Last-Modified", last_modified)
        if encoding:
            self.send_header("Content-Encoding", encoding)
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()  # HEAD: 不写 body

    def translate_path(self, path):
        """Override：从 self.directory 而不是 CWD 解析"""
        # 去掉 query string
        path = path.split("?", 1)[0].split("#", 1)[0]
        path = unquote(path)
        # 防越权
        words = [w for w in path.split("/") if w]
        full = os.path.normpath(os.path.join(self.directory, *words))
        if not full.startswith(os.path.abspath(self.directory)):
            return "/dev/null"  # 安全降级
        return full

    def log_message(self, format, *args):
        """精简日志"""
        sys.stderr.write(f"[gzip] {self.address_string()} - {format % args}\n")


if __name__ == "__main__":
    port = 18766
    directory = os.getcwd()
    # 解析参数
    args = sys.argv[1:]
    if "--dir" in args:
        idx = args.index("--dir")
        directory = os.path.abspath(args[idx + 1])
        del args[idx:idx + 2]
    if args:
        port = int(args[0])

    os.chdir(directory)
    server = HTTPServer(("127.0.0.1", port), GzipHTTPRequestHandler)
    print(f"Serving HTTP with gzip on http://127.0.0.1:{port}/")
    print(f"Directory: {directory}")
    print(f"Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print("\nStopped.")