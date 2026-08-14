"""Render review GIFs from the exact KitCode mascot assets and timings."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "public" / "mascots"
OUT_DIR = ROOT / "artwork" / "mascots" / "previews"
SIZE = 360
ART_SIZE = 330


def load(name: str) -> Image.Image:
    return Image.open(ASSET_DIR / name).convert("RGBA")


def card() -> Image.Image:
    image = Image.new("RGB", (SIZE, SIZE))
    pixels = image.load()
    for y in range(SIZE):
        blend = y / (SIZE - 1)
        for x in range(SIZE):
            glow = max(0.0, 1.0 - math.dist((x, y), (SIZE * 0.55, SIZE * 0.54)) / 260)
            pixels[x, y] = (
                int(9 + 4 * glow - 3 * blend),
                int(20 + 8 * glow - 5 * blend),
                int(35 + 13 * glow - 7 * blend),
            )
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, SIZE - 2, SIZE - 2), 20, outline=(42, 61, 82), width=2)
    return image


BACKGROUND = card()


def subject_frame(
    sprite: Image.Image,
    *,
    scale: float = 1.0,
    angle: float = 0.0,
    dx: float = 0.0,
    dy: float = 0.0,
    opacity: float = 1.0,
) -> Image.Image:
    frame = BACKGROUND.convert("RGBA")
    side = max(1, round(ART_SIZE * scale))
    art = sprite.resize((side, side), Image.Resampling.LANCZOS)
    if angle:
        art = art.rotate(-angle, Image.Resampling.BICUBIC, expand=True)
    if opacity < 1:
        alpha = art.getchannel("A").point(lambda value: round(value * opacity))
        art.putalpha(alpha)
    x = round((SIZE - art.width) / 2 + dx)
    y = round((SIZE - art.height) / 2 + dy)

    layer = Image.new("RGBA", frame.size)
    layer.alpha_composite(art, (x, y))
    shadow_alpha = layer.getchannel("A").filter(ImageFilter.GaussianBlur(3))
    shadow = Image.new("RGBA", frame.size, (1, 7, 17, 0))
    shadow.putalpha(shadow_alpha.point(lambda value: round(value * 0.28)))
    shifted_shadow = Image.new("RGBA", frame.size)
    shifted_shadow.alpha_composite(shadow, (0, 4))
    frame.alpha_composite(shifted_shadow)
    frame.alpha_composite(layer)
    return frame.convert("RGB")


def quantize(frames: list[Image.Image]) -> list[Image.Image]:
    # A reaction can begin on a nearly empty/transparent-looking frame. Build
    # one palette from the whole sequence so later frames keep Kit's colors.
    strip = Image.new("RGB", (frames[0].width * len(frames), frames[0].height))
    for index, frame in enumerate(frames):
        strip.paste(frame, (index * frame.width, 0))
    palette = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    return [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]


def save(name: str, frames: list[Image.Image], durations: int | list[int]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ready = quantize(frames)
    ready[0].save(
        OUT_DIR / name,
        save_all=True,
        append_images=ready[1:],
        duration=durations,
        loop=0,
        disposal=1,
        optimize=True,
    )


def save_contact_sheet(name: str, asset_names: list[str]) -> None:
    columns = 4
    tile = 240
    rows = math.ceil(len(asset_names) / columns)
    sheet = Image.new("RGB", (columns * tile, rows * tile), (7, 17, 30))
    draw = ImageDraw.Draw(sheet)
    for index, asset_name in enumerate(asset_names):
        sprite = load(asset_name)
        rendered = subject_frame(sprite).resize((tile, tile), Image.Resampling.LANCZOS)
        x = (index % columns) * tile
        y = (index // columns) * tile
        sheet.paste(rendered, (x, y))
        draw.rounded_rectangle((x + 8, y + 8, x + 70, y + 36), 8, fill=(7, 17, 30))
        draw.text((x + 21, y + 15), f"F{index + 1}", fill=(242, 247, 252))
    sheet.save(OUT_DIR / name, optimize=True)


def add_hole_and_dirt(frame: Image.Image, time_ms: int) -> Image.Image:
    image = frame.convert("RGBA")
    overlay = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(overlay)
    phase = (time_ms % 840) / 840
    mound_phase = (time_ms % 840) / 420
    mound_triangle = mound_phase if mound_phase <= 1 else 2 - mound_phase
    mound_scale = 0.72 + 0.28 * mound_triangle
    mound_width = round(274 * mound_scale)
    left = round(198 - mound_width / 2)
    draw.ellipse((left, 307, left + mound_width, 351), fill=(80, 39, 25, 255))
    draw.ellipse((left, 301, left + mound_width, 345), fill=(145, 73, 42, 255))
    draw.ellipse((left + 8, 303, left + mound_width - 8, 335), fill=(207, 123, 67, 255))

    for x, delay, direction in ((76, 0.0, -1), (308, 0.38, 1)):
        particle_phase = (phase - delay) % 1.0
        if particle_phase < 0.18:
            alpha = particle_phase / 0.18
        else:
            alpha = 1 - (particle_phase - 0.18) / 0.82
        radius = 5 + 7 * particle_phase
        px = x + direction * 11 * particle_phase
        py = 305 - 22 * particle_phase
        draw.ellipse(
            (px - radius, py - radius, px + radius, py + radius),
            fill=(217, 145, 85, round(255 * max(0, alpha))),
        )
    image.alpha_composite(overlay)
    return image.convert("RGB")


def hunting_preview() -> None:
    sprites = [load(f"kit-hunt-{index:02d}.webp") for index in range(1, 9)]
    durations = [160, 140, 140, 140, 140, 140, 160]

    def state_index(time_ms: int) -> int:
        elapsed = 0
        for index, duration in enumerate(durations):
            elapsed += duration
            if time_ms < elapsed:
                return index
        return 7

    frames = []
    for index in range(28):
        time_ms = index * 100
        sprite_index = state_index(time_ms)
        # Once Kit is underground, the same right-facing pose gets a tiny
        # searching wiggle. Reusing one drawing avoids a tail-side flip.
        rest_angle = math.sin((time_ms - 1020) / 260 * math.pi) * 0.8 if sprite_index == 7 else 0
        frame = subject_frame(sprites[sprite_index], angle=rest_angle)
        frames.append(add_hole_and_dirt(frame, time_ms))
    save("kit-finding-answer.gif", frames, 100)


def interpolate(points: list[tuple[float, tuple[float, ...]]], progress: float) -> tuple[float, ...]:
    for index, (position, values) in enumerate(points):
        if progress <= position:
            if index == 0:
                return values
            previous_position, previous_values = points[index - 1]
            local = (progress - previous_position) / (position - previous_position)
            return tuple(a + (b - a) * local for a, b in zip(previous_values, values))
    return points[-1][1]


def complete_preview() -> None:
    sprite = load("kit-chibi.webp")
    points = [
        (0.00, (3, 0, 0.96)),
        (0.22, (-5, -4, 1.03)),
        (0.40, (0, 4, 1.00)),
        (0.58, (0, -3, 1.00)),
        (0.76, (0, 2, 1.00)),
        (1.00, (0, 0, 1.00)),
    ]
    frames: list[Image.Image] = []
    durations: list[int] = []
    for index in range(10):
        progress = index / 9
        dy, angle, scale = interpolate(points, progress)
        frame = subject_frame(sprite, dy=dy, angle=angle, scale=scale)
        draw = ImageDraw.Draw(frame)
        if 0.12 < progress < 0.9:
            alpha_color = (241, 157, 91)
            draw.arc((295, 103, 350, 180), 292, 42, fill=alpha_color, width=4)
            draw.arc((307, 161, 354, 225), 296, 39, fill=alpha_color, width=3)
        frames.append(frame)
        durations.append(90)
    frames.append(subject_frame(sprite))
    durations.append(900)
    save("kit-answer-complete.gif", frames, durations)


def correct_answer_preview() -> None:
    sequence = [
        # name, duration, horizontal travel, vertical travel, scale
        ("kit-happy-01.webp", 180, -0.04, 0.00, 1.00),
        ("kit-happy-02.webp", 120, -0.04, 0.04, 1.06),
        ("kit-happy-03.webp", 130, -0.02, -0.10, 0.99),
        ("kit-happy-04.webp", 250, 0.02, -0.30, 0.96),
        ("kit-happy-05.webp", 130, 0.05, -0.18, 0.99),
        ("kit-happy-06.webp", 220, 0.07, 0.04, 1.07),
        ("kit-happy-07.webp", 1370, 0.00, 0.00, 1.00),
    ]
    frames = [
        subject_frame(
            load(name),
            dx=ART_SIZE * translate_x,
            dy=ART_SIZE * translate_y,
            scale=scale,
        )
        for name, _, translate_x, translate_y, scale in sequence
    ]
    save(
        "kit-correct-answer.gif",
        frames,
        [duration for _, duration, _, _, _ in sequence],
    )


def sleep_preview() -> None:
    sequence = [
        ("kit-sleep-01.webp", 420, 1.00, 0.00),
        ("kit-sleep-02.webp", 400, 1.00, 0.00),
        ("kit-sleep-03.webp", 400, 0.93, 0.74),
        ("kit-sleep-04.webp", 400, 0.76, 2.53),
        ("kit-sleep-05.webp", 400, 0.78, 2.32),
        ("kit-sleep-06.webp", 400, 0.75, 2.64),
        ("kit-sleep-07.webp", 450, 0.72, 2.95),
        ("kit-sleep-08.webp", 2330, 0.82, 1.90),
    ]
    frames = [
        subject_frame(load(name), scale=scale, dy=ART_SIZE * translate_y / 100)
        for name, _, scale, translate_y in sequence
    ]
    save(
        "kit-sleeping.gif",
        frames,
        [duration for _, duration, _, _ in sequence],
    )


def wake_preview() -> None:
    sequence = [
        ("kit-wake-01.webp", 320, 1.000, 0.00),
        ("kit-wake-02.webp", 380, 1.134, -1.42),
        ("kit-chibi.webp", 260, 0.896, -1.90),
    ]
    frames = [
        subject_frame(load(name), scale=scale, dy=ART_SIZE * translate_y / 100)
        for name, _, scale, translate_y in sequence
    ]
    save(
        "kit-waking-up.gif",
        frames,
        [duration for _, duration, _, _ in sequence],
    )


def surprise_preview() -> None:
    sprite = load("kit-surprised.webp")
    points = [
        (0.00, (8, 0, 0.88, 0.0)),
        (0.34, (-7, -2, 1.05, 1.0)),
        (0.58, (1, 1, 0.99, 1.0)),
        (0.76, (-2, 0, 1.01, 1.0)),
        (1.00, (0, 0, 1.00, 1.0)),
    ]
    animation_frames: list[Image.Image] = []
    durations: list[int] = []
    for index in range(8):
        progress = index / 7
        dy, angle, scale, opacity = interpolate(points, progress)
        animation_frames.append(
            subject_frame(
                sprite,
                dy=dy,
                angle=angle,
                scale=scale,
                opacity=opacity,
            )
        )
        durations.append(90)
    animation_frames.append(subject_frame(sprite))
    durations.append(1480)
    # Put the fully colored hold frame first in the GIF stream, then rotate the
    # duration list with it. Some chat renderers otherwise fail to composite a
    # mostly-background first reaction frame even with a shared palette.
    frames = [animation_frames[-1], *animation_frames[:-1]]
    rotated_durations = [durations[-1], *durations[:-1]]
    save("kit-script-error.gif", frames, rotated_durations)


if __name__ == "__main__":
    hunting_preview()
    complete_preview()
    correct_answer_preview()
    sleep_preview()
    wake_preview()
    surprise_preview()
    save_contact_sheet(
        "kit-hunting-frames.png",
        [f"kit-hunt-{index:02d}.webp" for index in range(1, 9)],
    )
    save_contact_sheet(
        "kit-sleep-frames.png",
        [f"kit-sleep-{index:02d}.webp" for index in range(1, 9)],
    )
    save_contact_sheet(
        "kit-happy-frames.png",
        [f"kit-happy-{index:02d}.webp" for index in range(1, 8)],
    )
    save_contact_sheet(
        "kit-wake-frames.png",
        [f"kit-wake-{index:02d}.webp" for index in range(1, 3)],
    )
    for output in sorted(OUT_DIR.glob("*.gif")):
        print(f"{output.relative_to(ROOT)}: {output.stat().st_size} bytes")
