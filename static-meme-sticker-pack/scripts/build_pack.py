from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    raise SystemExit("Pillow is required. Install it with: python -m pip install Pillow")


PLATFORMS = {
    "generic": {"size": 512, "max_bytes": None},
    "wechat": {"size": 240, "max_bytes": 500 * 1024},
    "telegram": {"size": 512, "max_bytes": 512 * 1024},
    "whatsapp": {"size": 512, "max_bytes": 100 * 1024},
    "discord": {"size": 128, "max_bytes": 256 * 1024},
}


def alpha_bbox(image: Image.Image):
    return image.getchannel("A").getbbox()


def audit(image: Image.Image, source: Path) -> list[str]:
    issues = []
    if image.mode != "RGBA":
        issues.append("missing RGBA mode")
    alpha = image.getchannel("A")
    extrema = alpha.getextrema()
    if extrema == (255, 255):
        issues.append("no transparent pixels")
    bbox = alpha.getbbox()
    if not bbox:
        issues.append("fully transparent")
    elif bbox[0] == 0 or bbox[1] == 0 or bbox[2] == image.width or bbox[3] == image.height:
        issues.append("subject touches canvas edge")
    if image.width != image.height:
        issues.append("source canvas is not square")
    return [f"{source.name}: {issue}" for issue in issues]


def fit_sticker(image: Image.Image, size: int, padding: int, outline: int) -> Image.Image:
    image = image.convert("RGBA")
    bbox = alpha_bbox(image)
    if not bbox:
        return Image.new("RGBA", (size, size))
    subject = image.crop(bbox)
    target = max(1, size - 2 * (padding + outline))
    subject.thumbnail((target, target), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", (size, size))
    x = (size - subject.width) // 2
    y = (size - subject.height) // 2
    if outline:
        mask = Image.new("L", (size, size))
        mask.paste(subject.getchannel("A"), (x, y))
        kernel = max(3, outline * 2 + 1)
        if kernel % 2 == 0:
            kernel += 1
        expanded = mask.filter(ImageFilter.MaxFilter(kernel))
        white = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        white.putalpha(expanded)
        layer.alpha_composite(white)
    layer.alpha_composite(subject, (x, y))
    return layer


def add_caption(image: Image.Image, text: str, font_path: str | None) -> Image.Image:
    if not text:
        return image
    draw = ImageDraw.Draw(image)
    font_size = max(18, image.width // 12)
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.truetype("msyh.ttc", font_size)
    except OSError:
        font = ImageFont.load_default()
    box = draw.textbbox((0, 0), text, font=font, stroke_width=3)
    x = (image.width - (box[2] - box[0])) // 2
    y = image.height - (box[3] - box[1]) - max(10, image.height // 30)
    draw.text((x, y), text, font=font, fill="white", stroke_width=3, stroke_fill="black")
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize transparent sticker PNGs and compose a preview sheet")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--platform", choices=PLATFORMS, default="generic")
    parser.add_argument("--columns", type=int)
    parser.add_argument("--padding", type=int, default=32)
    parser.add_argument("--gap", type=int, default=24)
    parser.add_argument("--outline", type=int, default=6)
    parser.add_argument("--captions", type=Path, help="JSON object mapping filename stem to caption text")
    parser.add_argument("--font", help="TTF/TTC font path for captions")
    parser.add_argument("--strict-alpha", action="store_true", help="fail when transparency or edge checks fail")
    args = parser.parse_args()

    sources = sorted(args.input_dir.glob("*.png"))
    if not sources:
        parser.error("input directory contains no PNG files")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sticker_dir = args.output_dir / "stickers"
    sticker_dir.mkdir(exist_ok=True)
    captions = json.loads(args.captions.read_text(encoding="utf-8")) if args.captions else {}
    size = PLATFORMS[args.platform]["size"]
    processed = []
    issues = []
    for source in sources:
        image = Image.open(source).convert("RGBA")
        issues.extend(audit(image, source))
        sticker = fit_sticker(image, size, args.padding, args.outline)
        sticker = add_caption(sticker, captions.get(source.stem, ""), args.font)
        destination = sticker_dir / source.name
        sticker.save(destination, optimize=True)
        processed.append(destination)

    columns = args.columns or math.ceil(math.sqrt(len(processed)))
    rows = math.ceil(len(processed) / columns)
    sheet = Image.new("RGBA", (columns * size + (columns + 1) * args.gap, rows * size + (rows + 1) * args.gap))
    for index, path in enumerate(processed):
        sticker = Image.open(path).convert("RGBA")
        x = args.gap + (index % columns) * (size + args.gap)
        y = args.gap + (index // columns) * (size + args.gap)
        sheet.alpha_composite(sticker, (x, y))
    sheet.save(args.output_dir / "preview.png", optimize=True)

    manifest = {
        "platform": args.platform,
        "count": len(processed),
        "canvas_size": size,
        "columns": columns,
        "rows": rows,
        "files": [path.name for path in processed],
        "quality_issues": issues,
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if args.strict_alpha and issues:
        sys.exit(2)


if __name__ == "__main__":
    main()
