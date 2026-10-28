#!/usr/bin/env python3
"""Browser smoke tests for the report shell and public demo."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = (
    ROOT / "templates" / "report-shell.html",
    ROOT / "demo" / "index.html",
)
DRAW_RE = re.compile(
    r"""\b(?:drawBars|drawSignedBars|drawNodeLine|drawGrouped|drawStacked|drawMini|drawScores|drawRanges)\(\s*['\"]([^'\"]+)['\"]"""
)


class DocumentIndex(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hash_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])  # type: ignore[arg-type]
        href = data.get("href")
        if tag == "a" and href and href.startswith("#") and len(href) > 1:
            self.hash_links.append(href[1:])


def fail(message: str) -> None:
    raise AssertionError(message)


def extract_draw_all(html: str) -> str:
    match = re.search(
        r"function\s+drawAll\(\)\s*\{([\s\S]*?)\n\s*\}\s*\n\s*drawAll\(\);",
        html,
    )
    if not match:
        fail("drawAll() block not found")
    body = re.sub(r"/\*[\s\S]*?\*/", "", match.group(1))
    body = re.sub(r"//.*", "", body)
    return body


def static_checks(path: Path) -> None:
    html = path.read_text(encoding="utf-8")

    if not html.rstrip().endswith("</html>"):
        fail(f"{path}: content exists after closing HTML or closing tag is missing")
    if html.count("</html>") != 1:
        fail(f"{path}: expected exactly one </html>")

    uncommented = re.sub(r"<!--[\s\S]*?-->", "", html)
    style_open_count = len(re.findall(r"<style(?:\s[^>]*)?>", uncommented))
    style_close_count = len(re.findall(r"</style\s*>", uncommented))
    if style_open_count != 1 or style_close_count != 1:
        fail(
            f"{path}: expected exactly one real <style> block, found "
            f"{style_open_count} open / {style_close_count} close"
        )
    if "-->" in uncommented:
        fail(f"{path}: stray HTML comment terminator outside a comment")

    parser = DocumentIndex()
    parser.feed(html)

    missing_targets = sorted(set(parser.hash_links) - parser.ids)
    if missing_targets:
        fail(f"{path}: TOC/hash targets missing: {missing_targets}")

    draw_all = extract_draw_all(html)
    chart_ids = set(DRAW_RE.findall(draw_all))
    missing_charts = sorted(chart_ids - parser.ids)
    if missing_charts:
        fail(f"{path}: drawAll() references missing chart hosts: {missing_charts}")

    scripts = re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", html)
    if not scripts:
        fail(f"{path}: no inline script found")

    node = shutil.which("node")
    if node:
        with tempfile.TemporaryDirectory() as tmp:
            for i, script in enumerate(scripts):
                js = Path(tmp) / f"{path.stem}-{i}.js"
                js.write_text(script, encoding="utf-8")
                proc = subprocess.run(
                    [node, "--check", str(js)],
                    capture_output=True,
                    text=True,
                )
                if proc.returncode:
                    fail(
                        f"{path}: JavaScript syntax check failed\n"
                        f"{proc.stdout}{proc.stderr}"
                    )

    print(f"✓ static HTML/JS checks: {path.relative_to(ROOT)}")


def browser_checks(path: Path) -> None:
    errors: list[str] = []
    url = path.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": 1440, "height": 1000},
                color_scheme="light",
            )
            page.on(
                "console",
                lambda msg: errors.append(f"console: {msg.text}")
                if msg.type == "error"
                else None,
            )
            page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))

            page.goto(url)
            page.wait_for_timeout(150)

            if errors:
                fail(f"{path}: browser errors: {errors}")

            body_text = page.locator("body").inner_text()
            for leaked in ("drawAll();", "drawBars(", "drawScores("):
                if leaked in body_text:
                    fail(f"{path}: JavaScript leaked into rendered body: {leaked}")

            button = page.locator("#tbtn")
            if button.count() != 1:
                fail(f"{path}: theme toggle #tbtn missing")

            bg_before = page.evaluate("getComputedStyle(document.body).backgroundColor")
            button.click()
            page.wait_for_timeout(80)
            theme_after = page.locator("html").get_attribute("data-theme")
            bg_after = page.evaluate("getComputedStyle(document.body).backgroundColor")
            if theme_after != "dark":
                fail(f"{path}: first theme toggle did not switch to dark")
            if bg_after == bg_before:
                fail(f"{path}: theme toggle did not change rendered colors")

            button.click()
            page.wait_for_timeout(80)
            if page.locator("html").get_attribute("data-theme") != "light":
                fail(f"{path}: second theme toggle did not switch back to light")

            page.close()

            mobile = browser.new_page(
                viewport={"width": 390, "height": 844},
                color_scheme="light",
            )
            mobile_errors: list[str] = []
            mobile.on(
                "console",
                lambda msg: mobile_errors.append(f"console: {msg.text}")
                if msg.type == "error"
                else None,
            )
            mobile.on(
                "pageerror",
                lambda exc: mobile_errors.append(f"pageerror: {exc}"),
            )
            mobile.goto(url)
            mobile.wait_for_timeout(150)
            if mobile_errors:
                fail(f"{path}: mobile browser errors: {mobile_errors}")

            overflow = mobile.evaluate(
                "document.documentElement.scrollWidth - window.innerWidth"
            )
            if overflow > 1:
                fail(f"{path}: mobile horizontal overflow: {overflow}px")

            mobile.close()
        finally:
            browser.close()

    print(f"✓ browser smoke checks: {path.relative_to(ROOT)}")



def security_checks() -> None:
    """Untrusted chart text must never create executable tooltip/legend markup."""
    source = (ROOT / "templates" / "report-shell.html").read_text(encoding="utf-8")
    start_marker = "  /* RDD_REPORT_DATA_START */"
    end_marker = "  /* RDD_REPORT_DATA_END */"
    start = source.index(start_marker)
    end = source.index(end_marker, start) + len(end_marker)
    attack = '<img src=x onerror="window.__rdd_xss = true">'
    data = (
        start_marker + "\n"
        "  function drawAll(){\n"
        "    drawBars('c-demo',[{y:'Test',v:10,note:" + json.dumps(attack) + "}],{max:12});\n"
        "    legend('leg-xss',[[" + json.dumps(attack) + ",'--series-1']]);\n"
        "  }\n"
        "  drawAll();\n"
        + end_marker
    )
    fixture = (source[:start] + data + source[end:]).replace(
        "<script>", '<div id="leg-xss"></div>\n<script>', 1
    )
    with tempfile.TemporaryDirectory() as tmp:
        test_path = Path(tmp) / "xss-fixture.html"
        test_path.write_text(fixture, encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.goto(test_path.resolve().as_uri())
                page.locator("#c-demo svg path").first.dispatch_event(
                    "mouseenter", {"clientX": 30, "clientY": 30}
                )
                if attack not in page.locator("#tt").inner_text():
                    fail("Tooltip did not preserve untrusted label as readable text")
                if attack not in page.locator("#leg-xss").inner_text():
                    fail("Legend did not preserve untrusted label as readable text")
                if page.locator("#tt img, #leg-xss img").count():
                    fail("Untrusted chart text produced an HTML image element")
                page.wait_for_timeout(100)
                if page.evaluate("Boolean(window.__rdd_xss)"):
                    fail("Untrusted chart text executed an event handler")
                page.close()
            finally:
                browser.close()
    print("✓ untrusted tooltip and legend labels remain inert text")

def main() -> int:
    for path in HTML_FILES:
        static_checks(path)
    for path in HTML_FILES:
        browser_checks(path)
    security_checks()
    print("\nAll browser QA checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
