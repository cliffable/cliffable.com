from pathlib import Path

BASE_URL = "https://cliffable.com"
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT_DIR / "sitemap.xml"

EXCLUDED_FILES = {
    "404.html",
}

EXCLUDED_DIRS = {
    "assets",
    "scripts",
    ".git",
    ".github",
    "__pycache__",
    "templates",
}

def should_exclude(path):
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True

    if path.name in EXCLUDED_FILES:
        return True

    return False


def generate_url(path):
    relative_path = path.relative_to(ROOT_DIR)

    if relative_path.name == "index.html":
        parent = str(relative_path.parent)

        if parent == ".":
            return f"{BASE_URL}/"

        return f"{BASE_URL}/{parent}/"

    return f"{BASE_URL}/{relative_path.as_posix()}"


html_files = []

for file_path in ROOT_DIR.rglob("*.html"):
    if should_exclude(file_path):
        continue

    html_files.append(file_path)

html_files.sort()

url_entries = []

for file_path in html_files:
    url = generate_url(file_path)

    entry = f"""  <url>
    <loc>{url}</loc>
  </url>"""

    url_entries.append(entry)

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

{chr(10).join(url_entries)}

</urlset>
"""

OUTPUT_FILE.write_text(sitemap_content, encoding="utf-8")

print(f"Generated sitemap with {len(url_entries)} URLs")
print(f"Saved to: {OUTPUT_FILE}")