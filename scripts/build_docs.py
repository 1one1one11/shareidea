#!/usr/bin/env python3
"""Build Markdown docs into a static HTML site."""

from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path

try:
    import markdown  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "[build_docs] Missing dependency: 'markdown'. Install with: pip install markdown"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "site" / "docs"
DIST_DIR = ROOT / "site" / "dist"
ASSETS_DIR = ROOT / "site" / "assets"
TEMPLATE_PATH = ROOT / "templates" / "base.html"
CONFIG_PATH = ROOT / "config" / "site.json"


@dataclass
class SiteConfig:
    site_name: str
    base_url: str
    footer: str
    navigation: list[dict[str, str]]


def load_config() -> SiteConfig:
    if not CONFIG_PATH.exists():
        raise SystemExit(f"[build_docs] Config file not found: {CONFIG_PATH}")

    try:
        payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[build_docs] Invalid JSON in {CONFIG_PATH}: {exc}") from exc

    return SiteConfig(
        site_name=payload.get("siteName", "Docs"),
        base_url=payload.get("baseUrl", "/"),
        footer=payload.get("footer", ""),
        navigation=payload.get("navigation", []),
    )


def clean_dist() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def copy_assets() -> None:
    if not ASSETS_DIR.exists():
        raise SystemExit(f"[build_docs] Assets directory not found: {ASSETS_DIR}")
    shutil.copytree(ASSETS_DIR, DIST_DIR / "assets", dirs_exist_ok=True)


def ensure_template() -> str:
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"[build_docs] Template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8-sig")


def asset_prefix(relative_html: Path) -> str:
    depth = len(relative_html.parts) - 1
    return "../" * depth


def rewrite_md_links(md_text: str) -> str:
    # Convert relative markdown links to html, preserving anchors.
    pattern = re.compile(r"(\[[^\]]+\]\()([^):#][^)#]*?)\.md(#[^)]+)?(\))", re.IGNORECASE)
    return pattern.sub(lambda m: f"{m.group(1)}{m.group(2)}.html{m.group(3) or ''}{m.group(4)}", md_text)


def render_navigation(nav_items: list[dict[str, str]], current_html: Path, prefix: str) -> str:
    current = current_html.as_posix()
    links: list[str] = []
    for item in nav_items:
        title = escape(item.get("title", "Untitled"))
        path = item.get("path", "index.html").lstrip("/")
        href = f"{prefix}{path}"
        css_class = "nav-link active" if path == current else "nav-link"
        links.append(f'<a class="{css_class}" href="{escape(href)}">{title}</a>')
    return "\n        ".join(links)


def md_to_html(md_text: str) -> str:
    transformed = rewrite_md_links(md_text)
    return markdown.markdown(
        transformed,
        extensions=["extra", "fenced_code", "tables", "sane_lists", "nl2br"],
        output_format="html5",
    )


def output_rel_path(md_file: Path) -> Path:
    rel = md_file.relative_to(DOCS_DIR)
    if rel.name == "index.md" and len(rel.parts) == 1:
        return Path("index.html")
    return rel.with_suffix(".html")


def build() -> int:
    if not DOCS_DIR.exists():
        raise SystemExit(f"[build_docs] Docs directory not found: {DOCS_DIR}")

    config = load_config()
    template = ensure_template()
    clean_dist()
    copy_assets()

    markdown_files = sorted(DOCS_DIR.rglob("*.md"))
    if not markdown_files:
        raise SystemExit(f"[build_docs] No markdown files found in: {DOCS_DIR}")

    build_time = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    built_count = 0
    for md_file in markdown_files:
        rel_html = output_rel_path(md_file)
        out_path = DIST_DIR / rel_html
        out_path.parent.mkdir(parents=True, exist_ok=True)

        md_source = md_file.read_text(encoding="utf-8-sig")
        html_body = md_to_html(md_source)

        prefix = asset_prefix(rel_html)
        nav_html = render_navigation(config.navigation, rel_html, prefix)

        title = rel_html.stem.replace("-", " ").title()
        text = template
        text = text.replace("{{PAGE_TITLE}}", escape(title))
        text = text.replace("{{SITE_NAME}}", escape(config.site_name))
        text = text.replace("{{NAVIGATION}}", nav_html)
        text = text.replace("{{CONTENT}}", html_body)
        text = text.replace("{{FOOTER_TEXT}}", escape(config.footer))
        text = text.replace("{{BUILD_TIME}}", escape(build_time))
        text = text.replace("{{BASE_URL}}", escape(config.base_url))
        text = text.replace("{{ASSET_PREFIX}}", prefix)

        out_path.write_text(text, encoding="utf-8")
        built_count += 1

    print(f"[build_docs] Built {built_count} pages into {DIST_DIR}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(build())
    except Exception as exc:  # pragma: no cover
        print(f"[build_docs] ERROR: {exc}", file=sys.stderr)
        raise
