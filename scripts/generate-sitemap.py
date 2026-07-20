from pathlib import Path
import subprocess

BASE_URL = "https://cliffable.com"
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT_DIR / "sitemap.xml"

EXCLUDED_FILES = {
    "404.html",
}

EXCLUDED_DIRS = {
    "assets",
    "favicon",
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

def get_last_modified_date(path):
    relative_path = path.relative_to(ROOT_DIR)

    result = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--format=%cs",
            "--",
            relative_path.as_posix(),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT_DIR,
    )

    return result.stdout.strip()

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
    last_modified = get_last_modified_date(file_path)

    entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{last_modified}</lastmod>
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