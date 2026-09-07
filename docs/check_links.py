"""Validate the built site's local links, fragments and assets without network I/O.

Run: python docs/check_links.py docs/_build/html
"""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def check(root):
    root = root.resolve()
    pages = {path: Page(path) for path in root.rglob("*.html")}
    if root / "index.html" not in pages:
        raise ValueError(f"No built index.html in {root}")
    errors = []
    count = 0
    for path, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            count += 1
            target = (root / unquote(parts.path).lstrip("/") if parts.path.startswith("/")
                      else path.parent / unquote(parts.path)) if parts.path else path
            target = target.resolve()
            if not target.is_relative_to(root):
                errors.append(f"{path.relative_to(root)}: link escapes the site: {link}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(root)}: missing target: {link}")
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(root)}: missing anchor: {link}")
    if errors:
        raise ValueError("\n".join(sorted(set(errors))))
    print(f"Validated {count} local links/assets across {len(pages)} HTML pages.")


if __name__ == "__main__":
    try:
        check(Path(sys.argv[1] if len(sys.argv) > 1 else "docs/_build/html"))
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
