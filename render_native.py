"""
render_native.py
-----------------

Render a vertical quiz video from a JSONL file of questions using
MoviePy. Each question is displayed for a fixed amount of time defined
in ``config/brand.yml``. The total runtime is padded to ensure the
video length falls within the configured minimum and maximum duration.

Usage:

    python render_native.py --in deduped.jsonl --out out/video.mp4

Dependencies:
    pip install moviepy

Configuration files:
    config/brand.yml

Note: This implementation is simplified and uses basic text clips on
a static background. It is intended as a starting point for building
a fully featured renderer.
"""

import argparse
import json
from pathlib import Path

import yaml
from moviepy.editor import (ColorClip, CompositeVideoClip, TextClip,
                            concatenate_videoclips)


def load_brand_config(base: Path) -> dict:
    with (base / 'config' / 'brand.yml').open() as f:
        return yaml.safe_load(f)


def render_video(questions_file: Path, output_file: Path, config: dict) -> None:
    # Extract settings
    timer_seconds = config['short']['timer_seconds']
    min_duration = config['short']['min_duration_sec']
    max_duration = config['short']['max_duration_sec']
    question_font_size = config['typography']['question_font_size']
    option_font_size = config['typography']['option_font_size']
    bg_color = config['colors']['background']
    text_color = config['colors']['text_primary']

    # Read questions
    questions = []
    with questions_file.open() as f:
        for line in f:
            questions.append(json.loads(line))

    clips = []
    # Video dimensions for vertical (9:16 ratio)
    width, height = 1080, 1920
    for q in questions:
        question_text = q['question']
        options = q['options']
        content = question_text + '\n' + '\n'.join(f"{chr(65+i)}. {opt}" for i, opt in enumerate(options))
        # Create text clip
        txt = TextClip(content, fontsize=question_font_size, color=text_color, font='Liberation-Sans', align='Center', method='caption', size=(width*0.9, None))
        # Create background clip
        bg = ColorClip(size=(width, height), color=tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))).set_duration(timer_seconds)
        # Position text in the center
        txt = txt.set_position(('center', 'center')).set_duration(timer_seconds)
        clip = CompositeVideoClip([bg, txt])
        clips.append(clip)

    # Concatenate clips
    video = concatenate_videoclips(clips)

    # Pad video to minimum duration with a blank slide if needed
    if video.duration < min_duration:
        pad_time = min_duration - video.duration
        pad_clip = ColorClip(size=(width, height), color=tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))).set_duration(pad_time)
        video = concatenate_videoclips([video, pad_clip])
    # Trim if exceeds max duration
    if video.duration > max_duration:
        video = video.subclip(0, max_duration)

    # Write video file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    video.write_videofile(str(output_file), fps=24, audio=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a quiz video using MoviePy.")
    parser.add_argument('--in', dest='inp', required=True, help='Input deduped JSONL file')
    parser.add_argument('--out', dest='outp', required=True, help='Output MP4 file')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent.parent
    brand_config = load_brand_config(base)
    render_video(Path(args.inp), Path(args.outp), brand_config)

if __name__ == '__main__':
    main()
