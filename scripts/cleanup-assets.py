from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
LIVE_TEXT_FILES = [
    ROOT / "index.html",
    ROOT / "ui-components" / "index.html",
    ROOT / "background-generator" / "index.html",
    ROOT / "design-md" / "index.html",
    ROOT / "README.md",
    ROOT / "site.webmanifest",
    *sorted((ROOT / "assets" / "css").glob("*.css")),
    *sorted((ROOT / "assets" / "js").glob("*.js")),
]
ASSET_PATTERN = re.compile(r"assets/[A-Za-z0-9._/-]+\.(?:png|jpg|jpeg|webp|svg|ico|css|js)")
KEEP = {
    "assets/vendor/README.md",
    "assets/vendor/lenis/LICENSE",
    # Root /favicon.ico fallback for browsers that request it directly.
    "assets/images/favicon.ico",
}


def referenced_assets() -> set[str]:
    found = set()
    for path in LIVE_TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        for match in ASSET_PATTERN.finditer(text):
            found.add(match.group(0))
    return found


def main() -> None:
    dry_run = "--delete" not in sys.argv
    referenced = referenced_assets()
    delete_list = []

    for folder in ("previews", "logos", "images"):
        for path in sorted((ROOT / "assets" / folder).rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            if relative in referenced or relative in KEEP:
                continue
            delete_list.append(path)

    total = sum(path.stat().st_size for path in delete_list)
    print(f"{'Would delete' if dry_run else 'Deleting'} {len(delete_list)} files, {total / 1024 / 1024:.1f} MB")
    for path in delete_list:
        print(path.relative_to(ROOT).as_posix())

    if not dry_run:
        for path in delete_list:
            path.unlink()


if __name__ == "__main__":
    main()
