from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "assets" / "images"
SCREENSHOT = Path(r"C:\Users\Miqdad\Pictures\Screenshots\Screenshot 2026-11-01 112427.png")
LOGO = IMAGES / "logo.png"


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    source_ratio = image.width / image.height
    target_ratio = width / height
    if source_ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    else:
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def rounded_icon(source: Image.Image, size: int, radius_ratio: float = 0.22, padding_ratio: float = 0.08) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    padding = int(size * padding_ratio)
    inner = size - (padding * 2)
    mark = source.resize((inner, inner), Image.Resampling.LANCZOS)
    mask = Image.new("L", (inner, inner), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, inner - 1, inner - 1),
        radius=int(inner * radius_ratio),
        fill=255,
    )
    canvas.paste(mark, (padding, padding), mask)
    return canvas


def rounded_image(source: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, source.width - 1, source.height - 1),
        radius=radius,
        fill=255,
    )
    output = source.convert("RGBA")
    output.putalpha(mask)
    return output


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)

    screenshot = Image.open(SCREENSHOT).convert("RGB")
    cover_crop(screenshot, 1200, 630).save(IMAGES / "og-image.jpg", quality=90, optimize=True)

    readme_width = 1600
    readme_height = round(readme_width * screenshot.height / screenshot.width)
    readme = screenshot.resize((readme_width, readme_height), Image.Resampling.LANCZOS)
    rounded_image(readme, 30).save(IMAGES / "readme-hero.webp", quality=88, method=6)

    logo = Image.open(LOGO).convert("RGB")
    luminance = logo.convert("L")
    bright = luminance.point(lambda value: 255 if value > 200 else 0)
    bbox = bright.getbbox()
    if bbox is None:
        raise SystemExit("Could not find the white mark in logo.png")

    left, top, right, bottom = bbox
    side = max(right - left, bottom - top)
    pad = int(side * 0.18)
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    half = (side // 2) + pad
    crop = (
        max(0, center_x - half),
        max(0, center_y - half),
        min(logo.width, center_x + half),
        min(logo.height, center_y + half),
    )
    mark = logo.crop(crop)

    for size in (16, 32):
        icon = rounded_icon(mark, size)
        icon.save(IMAGES / f"favicon-{size}x{size}.png", optimize=True)

    rounded_icon(mark, 180).save(IMAGES / "apple-touch-icon.png", optimize=True)
    rounded_icon(mark, 192).save(IMAGES / "icon-192.png", optimize=True)
    rounded_icon(mark, 512).save(IMAGES / "icon-512.png", optimize=True)

    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    rounded_icon(mark, 48).save(IMAGES / "favicon.ico", sizes=ico_sizes)

    print("Generated brand assets in", IMAGES)


if __name__ == "__main__":
    main()
