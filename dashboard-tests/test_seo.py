"""test_seo.py · SEO meta 契约 v1.0 (P2-2 Web Dev 0.91 落地)

实测起点 (2026-06-29):
- 0 og: / 0 twitter: / 0 canonical / 0 JSON-LD / 0 meta description (干净增量)
- GitHub Pages 未开 (404 + 无 gh-pages 分支) → 离线工具页
- canonical 用 repo 唯一规范 URL (GitHub Pages 默认规则推导, 未来开即生效)

设计原则 (反讽 R1-R4 + 一致性优先):
- R1 显式报问题: 漏字段 → hard fail, 错误信息说明缺什么 + 影响 (爬虫/社交卡)
- R2 baseline 不固化: 不硬编码 description 整句, 只断言"四处一致 + 关键词 + 长度",
  改文案不误伤, 漏改一处必 fail (SEO meta 最常见 bug = 改 title 忘改 og:title)
- R3 不猜死: og:title/twitter:title/document title 三处必须一致 (内部一致性契约)
- R4 严重缺陷不软化: JSON-LD 非法 JSON → fail loud
- 诚实性守护: 无 og:image (无真实图源, 不造假) + JSON-LD 无占位 URL (example.com/TODO)
"""
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"

# canonical / og:url / JSON-LD url 三处应一致指向的规范 URL.
# repo = atomai-team/Claude_Code_Guide_Offline → GitHub Pages 默认 URL.
EXPECTED_CANONICAL = (
    "https://atomai-team.github.io/Claude_Code_Guide_Offline/dashboard.html"
)


# ─────────────────────────────────────────────────────────────────
# Helpers: meta/title/jsonld 提取 (顺序无关, 容忍属性前后)
# ─────────────────────────────────────────────────────────────────

def _meta_content(html: str, key_attr: str, key_val: str) -> str | None:
    """提取 `<meta {key_attr}="{key_val}" ... content="...">` 的 content.

    先定位含该 key 的整个 <meta> 标签, 再从标签内取 content —
    对 content 在 key 之前/之后都工作 (顺序无关).
    """
    tag_m = re.search(
        rf'''<meta\b[^>]*\b{re.escape(key_attr)}=["']{re.escape(key_val)}["'][^>]*>''',
        html,
        re.IGNORECASE,
    )
    if not tag_m:
        return None
    # content 值用配对引号反向引用, 兼容单/双引号 (P2 健壮性, code-reviewer 建议)
    cm = re.search(r'''\bcontent=(["'])(.*?)\1''', tag_m.group(0), re.IGNORECASE)
    return cm.group(2) if cm else None


def _document_title(html: str) -> str | None:
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    return m.group(1).strip() if m else None


def _canonical_href(html: str) -> str | None:
    tag_m = re.search(
        r'<link\b[^>]*\brel="canonical"[^>]*>', html, re.IGNORECASE
    )
    if not tag_m:
        return None
    hm = re.search(r'\bhref="([^"]*)"', tag_m.group(0), re.IGNORECASE)
    return hm.group(1) if hm else None


def _jsonld(html: str):
    """提取并 parse 第一个 application/ld+json script. 非法 JSON 会 raise."""
    m = re.search(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None
    return json.loads(m.group(1))


# ─────────────────────────────────────────────────────────────────
# TestMetaDescription: 搜索引擎摘要
# ─────────────────────────────────────────────────────────────────

class TestMetaDescription:
    """<meta name="description"> 是搜索结果摘要的来源."""

    def test_description_present(self, dashboard_html: str):
        desc = _meta_content(dashboard_html, "name", "description")
        assert desc is not None, (
            "<meta name='description'> 缺失. 搜索引擎只能截取正文片段当摘要, "
            "无法控制搜索结果展示文案."
        )

    def test_description_meaningful_length(self, dashboard_html: str):
        desc = _meta_content(dashboard_html, "name", "description")
        assert desc and len(desc) > 20, (
            f"description 太短 ({len(desc or '')} chars): {desc!r}. "
            f"应 50-160 字符 (中文 30-80 字) 才有 SEO 价值."
        )

    def test_description_mentions_product(self, dashboard_html: str):
        """description 必须含产品关键词 (与页面真实主题一致, 非通用占位)."""
        desc = _meta_content(dashboard_html, "name", "description") or ""
        assert "Claude Code" in desc, (
            f"description 未提及 'Claude Code' (页面核心主题): {desc!r}"
        )


# ─────────────────────────────────────────────────────────────────
# TestCanonical: 规范 URL (防重复内容)
# ─────────────────────────────────────────────────────────────────

class TestCanonical:
    """<link rel="canonical"> 声明页面规范身份, 防搜索引擎判重复内容."""

    def test_canonical_present(self, dashboard_html: str):
        href = _canonical_href(dashboard_html)
        assert href is not None, (
            "<link rel='canonical'> 缺失. 多 URL 访问 (http/https, 带不带斜杠) "
            "会被判重复内容, 稀释排名权重."
        )

    def test_canonical_is_absolute(self, dashboard_html: str):
        """canonical 必须绝对 URL (相对 URL 在 canonical 中无效)."""
        href = _canonical_href(dashboard_html) or ""
        assert href.startswith("https://"), (
            f"canonical 必须 https 绝对 URL, 实际: {href!r}. "
            f"相对路径在 canonical 中会被忽略."
        )

    def test_canonical_matches_expected(self, dashboard_html: str):
        href = _canonical_href(dashboard_html)
        assert href == EXPECTED_CANONICAL, (
            f"canonical 与规范 URL 不符.\n  期望: {EXPECTED_CANONICAL}\n  实际: {href}"
        )


# ─────────────────────────────────────────────────────────────────
# TestOpenGraph: 社交分享卡 (Facebook/LinkedIn/微信等)
# ─────────────────────────────────────────────────────────────────

class TestOpenGraph:
    """og: 标签控制社交平台分享时的卡片展示."""

    REQUIRED = ["og:type", "og:title", "og:description", "og:url", "og:site_name"]

    @pytest.mark.parametrize("prop", REQUIRED)
    def test_required_og_property_present(self, prop, dashboard_html: str):
        val = _meta_content(dashboard_html, "property", prop)
        assert val, (
            f"<meta property='{prop}'> 缺失或空. 社交分享卡展示不完整."
        )

    def test_og_type_is_website(self, dashboard_html: str):
        val = _meta_content(dashboard_html, "property", "og:type")
        assert val == "website", (
            f"og:type 应为 'website' (单页指导书), 实际: {val!r}"
        )

    def test_og_title_matches_document_title(self, dashboard_html: str):
        """og:title 必须 == <title> (内部一致性, 防改标题漏改 og)."""
        og_title = _meta_content(dashboard_html, "property", "og:title")
        doc_title = _document_title(dashboard_html)
        assert og_title == doc_title, (
            f"og:title 与 <title> 不一致 (改标题时漏改了 og:title?).\n"
            f"  <title>:   {doc_title!r}\n  og:title:  {og_title!r}"
        )

    def test_og_url_matches_canonical(self, dashboard_html: str):
        """og:url 必须 == canonical (社交卡与搜索引擎指向同一规范页)."""
        og_url = _meta_content(dashboard_html, "property", "og:url")
        canonical = _canonical_href(dashboard_html)
        assert og_url == canonical, (
            f"og:url 与 canonical 不一致.\n  og:url:    {og_url}\n  canonical: {canonical}"
        )

    def test_og_locale_is_zh_cn(self, dashboard_html: str):
        """页面 lang='zh-CN' → og:locale 应 zh_CN (注意下划线, 非连字符)."""
        val = _meta_content(dashboard_html, "property", "og:locale")
        assert val == "zh_CN", (
            f"og:locale 应 'zh_CN' (OG 规范用下划线), 实际: {val!r}"
        )


# ─────────────────────────────────────────────────────────────────
# TestTwitterCard: Twitter/X 分享卡
# ─────────────────────────────────────────────────────────────────

class TestTwitterCard:
    """twitter: 标签控制 Twitter/X 分享卡展示."""

    def test_twitter_card_present(self, dashboard_html: str):
        val = _meta_content(dashboard_html, "name", "twitter:card")
        assert val, "<meta name='twitter:card'> 缺失. Twitter 分享退化为纯链接."

    def test_twitter_card_type_valid(self, dashboard_html: str):
        """card 类型必须合法. summary (无大图) / summary_large_image (需大图)."""
        val = _meta_content(dashboard_html, "name", "twitter:card")
        assert val in ("summary", "summary_large_image"), (
            f"twitter:card 非法值: {val!r}. 应 summary 或 summary_large_image."
        )

    def test_twitter_card_no_image_claim_without_image(self, dashboard_html: str):
        """诚实性: 用 summary_large_image 却无 og:image/twitter:image → 破图.

        本页无真实图源, 故应 summary (不声称有大图).
        """
        card = _meta_content(dashboard_html, "name", "twitter:card")
        has_image = (
            _meta_content(dashboard_html, "property", "og:image") is not None
            or _meta_content(dashboard_html, "name", "twitter:image") is not None
        )
        if card == "summary_large_image":
            assert has_image, (
                "twitter:card='summary_large_image' 但无 og:image/twitter:image → "
                "社交卡显示破图. 无图源时应用 'summary'."
            )

    def test_twitter_title_matches_document_title(self, dashboard_html: str):
        tw_title = _meta_content(dashboard_html, "name", "twitter:title")
        doc_title = _document_title(dashboard_html)
        assert tw_title == doc_title, (
            f"twitter:title 与 <title> 不一致.\n"
            f"  <title>:      {doc_title!r}\n  twitter:title: {tw_title!r}"
        )

    def test_twitter_description_present(self, dashboard_html: str):
        val = _meta_content(dashboard_html, "name", "twitter:description")
        assert val, "<meta name='twitter:description'> 缺失."


# ─────────────────────────────────────────────────────────────────
# TestJsonLd: 结构化数据 (Google 富结果)
# ─────────────────────────────────────────────────────────────────

class TestJsonLd:
    """JSON-LD WebSite schema — Google 理解站点身份的结构化数据."""

    def test_jsonld_present(self, dashboard_html: str):
        m = re.search(
            r'type="application/ld\+json"', dashboard_html, re.IGNORECASE
        )
        assert m, "<script type='application/ld+json'> 缺失."

    def test_jsonld_is_valid_json(self, dashboard_html: str):
        """JSON-LD 必须合法 JSON (非法 → Google 静默忽略整块)."""
        try:
            data = _jsonld(dashboard_html)
        except json.JSONDecodeError as e:
            pytest.fail(f"JSON-LD 非法 JSON: {e}. Google 会静默丢弃整个结构化数据块.")
        assert data is not None, "JSON-LD script 未找到或内容空."

    def test_jsonld_type_is_webpage(self, dashboard_html: str):
        """单页工具 → WebPage (非 WebSite). WebSite.url 惯例指站点根, 与本页 canonical 不符.

        web-perf-auditor 规范背书: schema.org WebSite.url = 站点根 URL,
        本页 url 指 dashboard.html → 用 WebPage 语义自洽 + 与 canonical 一致.
        """
        data = _jsonld(dashboard_html)
        assert data.get("@type") == "WebPage", (
            f"JSON-LD @type 应 'WebPage' (单个页面, url 指本页与 canonical 一致), "
            f"实际: {data.get('@type')!r}"
        )

    def test_jsonld_has_description(self, dashboard_html: str):
        """JSON-LD description 必须独立守护存在 (补 P1 假阴性盲区).

        code-reviewer mutation 实测: 删 JSON-LD description → 一致性测试因 None
        过滤仍 PASS (假阴性). 故需此独立存在性断言, 不依赖一致性测试兜底.
        """
        data = _jsonld(dashboard_html)
        desc = data.get("description")
        assert desc and len(desc) > 20, (
            f"JSON-LD description 缺失或太短: {desc!r}."
        )

    def test_jsonld_has_context(self, dashboard_html: str):
        data = _jsonld(dashboard_html)
        assert "schema.org" in str(data.get("@context", "")), (
            f"JSON-LD @context 应指向 schema.org, 实际: {data.get('@context')!r}"
        )

    def test_jsonld_name_nonempty(self, dashboard_html: str):
        data = _jsonld(dashboard_html)
        assert data.get("name"), "JSON-LD name 缺失或空 (站点名是 WebSite schema 核心)."

    def test_jsonld_url_matches_canonical(self, dashboard_html: str):
        data = _jsonld(dashboard_html)
        canonical = _canonical_href(dashboard_html)
        assert data.get("url") == canonical, (
            f"JSON-LD url 与 canonical 不一致.\n"
            f"  JSON-LD url: {data.get('url')}\n  canonical:   {canonical}"
        )

    def test_jsonld_has_inlanguage(self, dashboard_html: str):
        data = _jsonld(dashboard_html)
        assert data.get("inLanguage", "").lower().startswith("zh"), (
            f"JSON-LD inLanguage 应 zh-CN (页面中文), 实际: {data.get('inLanguage')!r}"
        )

    def test_jsonld_no_placeholder_urls(self, dashboard_html: str):
        """诚实性守护: JSON-LD 不含占位/造假 URL."""
        raw = re.search(
            r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            dashboard_html,
            re.DOTALL | re.IGNORECASE,
        )
        assert raw, "JSON-LD script 未找到."
        body = raw.group(1).lower()
        for placeholder in ("example.com", "placeholder", "todo", "yourdomain"):
            assert placeholder not in body, (
                f"JSON-LD 含占位 URL '{placeholder}' — 造假资源链接, 应删或填真实值."
            )


# ─────────────────────────────────────────────────────────────────
# TestSeoConsistency: 跨字段一致性 (核心契约)
# ─────────────────────────────────────────────────────────────────

class TestSeoConsistency:
    """SEO meta 最常见 bug = 改一处漏改其它. 这组锁定跨字段一致性."""

    def test_description_consistent_across_all_surfaces(self, dashboard_html: str):
        """meta / og / twitter / JSON-LD 四处 description 必须同一文本."""
        surfaces = {
            "meta": _meta_content(dashboard_html, "name", "description"),
            "og": _meta_content(dashboard_html, "property", "og:description"),
            "twitter": _meta_content(dashboard_html, "name", "twitter:description"),
            "json-ld": (_jsonld(dashboard_html) or {}).get("description"),
        }
        # 反讽 R1 (code-reviewer mutation 实测): 不可过滤 None — 否则"某处整个缺失"
        # 会让剩余项一致而假阴性通过. 先断言每处存在, 再断言一致.
        missing = [k for k, v in surfaces.items() if not v]
        assert not missing, (
            f"description 在这些处缺失 (漏字段, 非一致性问题): {missing}\n"
            + "\n".join(f"  {k}: {v!r}" for k, v in surfaces.items())
        )
        unique = set(surfaces.values())
        assert len(unique) == 1, (
            f"description 在 4 处不一致 (改了一处漏改其它):\n"
            + "\n".join(f"  {k}: {v!r}" for k, v in surfaces.items())
        )

    def test_title_consistent_across_og_twitter(self, dashboard_html: str):
        """document title / og:title / twitter:title 三处必须一致."""
        doc = _document_title(dashboard_html)
        og = _meta_content(dashboard_html, "property", "og:title")
        tw = _meta_content(dashboard_html, "name", "twitter:title")
        assert doc == og == tw, (
            f"title 三处不一致:\n  <title>: {doc!r}\n  og: {og!r}\n  twitter: {tw!r}"
        )

    def test_url_consistent_across_canonical_og_jsonld(self, dashboard_html: str):
        """canonical / og:url / JSON-LD url 三处必须指向同一规范 URL."""
        canonical = _canonical_href(dashboard_html)
        og_url = _meta_content(dashboard_html, "property", "og:url")
        jsonld_url = (_jsonld(dashboard_html) or {}).get("url")
        assert canonical == og_url == jsonld_url, (
            f"规范 URL 三处不一致:\n  canonical: {canonical}\n"
            f"  og:url: {og_url}\n  json-ld: {jsonld_url}"
        )
