"""
make_thumbnail.py
------------------

Generate a simple thumbnail image for a quiz video using Pillow. The
thumbnail includes the topic name and a hook line. For a production
system, this script would use more sophisticated layouts and images.

Usage:

    python make_thumbnail.py --topic "World Capitals" --hook "Can you guess them all?" --out out/thumb.png

Dependencies:
    pip install pillow

Configuration files:
    config/brand.yml
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import yaml


def make_thumbnail(topic: str, hook: str, out_path: Path, config: dict) -> None:
    width, height = 1080, 1920
    bg_color = config['colors']['background']
    text_color = config['colors']['text_primary']
    # Create blank image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Load a basic font; Pillow's default is limited, so fallback to DejaVuSans
    try:
        font_topic = ImageFont.truetype('DejaVuSans-Bold.ttf', 80)
        font_hook = ImageFont.truetype('DejaVuSans.ttf', 60)
    except IOError:
        font_topic = ImageFont.load_default()
        font_hook = ImageFont.load_default()
    # Center topic text
    topic_w, topic_h = draw.textsize(topic, font=font_topic)
    hook_w, hook_h = draw.textsize(hook, font=font_hook)
    draw.text(((width - topic_w) / 2, height / 3), topic, font=font_topic, fill=text_color)
    draw.text(((width - hook_w) / 2, height / 3 + topic_h + 40), hook, font=font_hook, fill=text_color)
    img.save(out_path)


def load_brand_config(base: Path) -> dict:
    with (base / 'config' / 'brand.yml').open() as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a thumbnail for a quiz video.")
    parser.add_argument('--topic', required=True, help='Quiz topic')
    parser.add_argument('--hook', required=True, help='Hook line to entice viewers')
    parser.add_argument('--out', required=True, help='Output PNG file')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent.parent
    config = load_brand_config(base)
    make_thumbnail(args.topic, args.hook, Path(args.out), config)
    print(f"Thumbnail saved to {args.out}")

if __name__ == '__main__':
    main()
