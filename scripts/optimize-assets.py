from pathlib import Path
import re

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LIVE_FILES = [
    ROOT / "index.html",
    ROOT / "ui-components" / "index.html",
    ROOT / "background-generator" / "index.html",
    ROOT / "design-md" / "index.html",
    ROOT / "assets" / "css" / "components.css",
]

ASSET_PATTERN = re.compile(
    r"(?:\.\./)?assets/(?:previews|logos|images)/[A-Za-z0-9._-]+\.(?:png|jpg|jpeg)"
)

# Social platforms prefer JPEG for link previews, so keep this out of the WebP pass.
SKIP = {"assets/images/og-image.jpg"}


def webp_path(path: Path) -> Path:
    return path.with_suffix(".webp")


def optimize_preview(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    if image.width > 960:
        height = round(image.height * 960 / image.width)
        image = image.resize((960, height), Image.Resampling.LANCZOS)
    image.save(webp_path(path), "WEBP", quality=80, method=6)


def optimize_logo(path: Path) -> None:
    image = Image.open(path).convert("RGBA")
    if image.width > 128 or image.height > 128:
        image.thumbnail((128, 128), Image.Resampling.LANCZOS)
    image.save(webp_path(path), "WEBP", quality=85, method=6)


def optimize_hero(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    image.save(webp_path(path), "WEBP", quality=82, method=6)


def main() -> None:
    texts = {path: path.read_text(encoding="utf-8") for path in LIVE_FILES}
    references = set()

    for text in texts.values():
        for match in ASSET_PATTERN.finditer(text):
            if match.group(0) in SKIP:
                continue
            references.add(match.group(0))

    converted = []
    for reference in sorted(references):
        relative = reference.replace("../", "")
        source = ROOT / relative
        if not source.exists():
            print("Missing:", reference)
            continue

        if "/previews/" in relative:
            optimize_preview(source)
        elif "/logos/" in relative:
            optimize_logo(source)
        elif "/images/" in relative and source.suffix.lower() in {".jpg", ".jpeg"}:
            optimize_hero(source)
        else:
            continue

        converted.append((reference, reference.rsplit(".", 1)[0] + ".webp"))

    for path, text in texts.items():
        updated = text
        for old, new in converted:
            updated = updated.replace(old, new)
        path.write_text(updated, encoding="utf-8")

    logo = ROOT / "assets" / "images" / "logo.png"
    if logo.exists():
        image = Image.open(logo).convert("RGB")
        image = image.resize((512, 512), Image.Resampling.LANCZOS)
        image.save(logo, optimize=True)

    print(f"Converted {len(converted)} referenced assets to WebP")
    for old, new in converted:
        print(f"  {old} -> {new}")


if __name__ == "__main__":
    main()
