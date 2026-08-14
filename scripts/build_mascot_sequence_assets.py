"""Normalize transparent mascot source art into aligned 512px WebP frames."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artwork" / "mascots" / "source"
PUBLIC = ROOT / "public" / "mascots"
CANVAS = 512


SEQUENCES = {
    "hunt": [
        "kit-hunt-crouch",
        "kit-hunt-liftoff",
        "kit-dive-leap",
        "kit-hunt-arc",
        "kit-hunt-reach",
        "kit-hunt-half-entry",
        "kit-hunt-entry",
        "kit-hunt-tail-up",
    ],
    "sleep": [
        "kit-chibi",
        "kit-sleep-drowsy",
        "kit-sleep-nod",
        "kit-sleep-settle-right",
        "kit-sleep-lower",
        "kit-sleep-nestle",
        "kit-sleep-tuck",
        "kit-sleep-curled",
    ],
    "happy": [
        "kit-happy-ready",
        "kit-happy-squash",
        "kit-happy-liftoff",
        "kit-happy-hop",
        "kit-happy-descent",
        "kit-happy-land",
        "kit-happy-settle",
    ],
    "wake": [
        "kit-wake-stir",
        "kit-wake-rise",
    ],
}

# Curl silhouettes are much wider than the seated poses. Treating every
# frame's largest dimension as the same body size made Kit grow and shrink.
# These registrations lock the curled half to one 360px-tall pose box while
# preserving the shared 484px ground line.
SLEEP_TARGET_HEIGHTS = {
    "kit-chibi": 360,
    "kit-sleep-drowsy": 360,
    "kit-sleep-nod": 360,
    "kit-sleep-settle-right": 360,
    "kit-sleep-lower": 360,
    "kit-sleep-nestle": 360,
    "kit-sleep-tuck": 360,
    "kit-sleep-curled": 360,
}
SLEEP_OFFSETS = {
    # After normalizing curl height, these small intentional offsets keep the
    # head/body mass in one stable region without allowing the changing tail
    # silhouette to recenter the fox unpredictably.
    "kit-chibi": (0, 0),
    "kit-sleep-drowsy": (0, 0),
    "kit-sleep-nod": (0, 0),
    "kit-sleep-settle-right": (5, 0),
    "kit-sleep-lower": (25, 0),
    "kit-sleep-nestle": (-25, 0),
    "kit-sleep-tuck": (5, 0),
    "kit-sleep-curled": (-3, 0),
}


def source_for(stem: str) -> Path:
    png = SOURCE / f"{stem}.png"
    if png.exists():
        return png
    webp = PUBLIC / f"{stem}.webp"
    if webp.exists():
        return webp
    raise FileNotFoundError(stem)


def normalized(stem: str) -> Image.Image:
    image = Image.open(source_for(stem)).convert("RGBA")
    alpha = image.getchannel("A")
    # Ignore barely visible generated/chroma-removal residue when measuring a
    # pose. A stray low-alpha pixel must not shrink the actual fox to fit it.
    visible_alpha = alpha.point(lambda value: 255 if value >= 32 else 0)
    bbox = visible_alpha.getbbox()
    if bbox is None:
        raise ValueError(f"{stem} has no visible subject")
    subject = image.crop(bbox)
    clean_alpha = subject.getchannel("A").point(
        lambda value: 0 if value < 32 else value,
    )
    subject.putalpha(clean_alpha)
    # Consistent padding and a bottom anchor prevent apparent scale/position
    # jumps between separately illustrated poses.
    maximum = 448
    target_height = SLEEP_TARGET_HEIGHTS.get(stem)
    scale = (
        target_height / subject.height
        if target_height is not None
        else min(maximum / subject.width, maximum / subject.height)
    )
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS, CANVAS))
    offset = SLEEP_OFFSETS.get(stem, (0, 0))
    x = round((CANVAS - size[0]) / 2 + offset[0])
    y = CANVAS - 28 - size[1] + offset[1]
    canvas.alpha_composite(subject, (x, y))
    return canvas


def main() -> None:
    for sequence, stems in SEQUENCES.items():
        for index, stem in enumerate(stems, start=1):
            output = PUBLIC / f"kit-{sequence}-{index:02d}.webp"
            image = normalized(stem)
            image.save(output, "WEBP", quality=92, method=4, exact=True)
            print(f"{output.relative_to(ROOT)} {output.stat().st_size}")


if __name__ == "__main__":
    main()
