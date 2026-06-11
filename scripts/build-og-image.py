"""
Build og-image.png for the Test-Drive Entrepreneurship deck.

Output: 1200 x 630 PNG, suitable for Open Graph / Twitter card.

Composition (left to right):
  - bkg.png as the warm base layer, with a darkened gradient overlay so text
    stays readable.
  - Pathfinder Foundry lockup (top-left, white on dark).
  - Eyebrow: THRIVEHUB · HANDS-ON WORKSHOP (PF yellow accent).
  - Two-line headline: "Test-Drive / Entrepreneurship."
  - Marc Krejci byline (small, near the bottom-left).
  - Marc's circular avatar (right side, with a subtle PF yellow ring).
  - Faint PF dot motif behind the avatar.

Run from the deck folder:
  python3 scripts/build-og-image.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
# Canonical brand background lives in the repo asset library, not the deck copy.
# Falls back to the deck-local images/bkg.png if the deck has left the repo.
BRAND_BKG = ROOT.parent.parent / "_assets" / "brand" / "bkg.png"
if not BRAND_BKG.exists():
    BRAND_BKG = IMAGES / "bkg.png"
OUT = ROOT / "og-image.png"

WIDTH, HEIGHT = 1200, 630
ACCENT = (255, 204, 100, 255)   # PF Yellow
ACCENT_DIM = (255, 204, 100, 70)
TEXT = (245, 245, 245, 255)
TEXT_MUTED = (180, 178, 188, 255)
BG_DARK = (15, 13, 24, 255)


# ---------- Font helpers ----------
def find_font(*candidates):
    for path in candidates:
        if Path(path).exists():
            return path
    return None


SANS_BOLD = find_font(
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)
SANS_REG = find_font(
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
SERIF_ITALIC = find_font(
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
)


def font(path, size):
    return ImageFont.truetype(path, size) if path else ImageFont.load_default()


# ---------- Background composition ----------
def make_background():
    """Build the warm-to-dark background with bkg.png + overlays."""
    base = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 14))

    # Place bkg.png as a cover-fit centered layer.
    src = Image.open(BRAND_BKG).convert("RGB")
    sw, sh = src.size
    # Cover-fit scale
    scale = max(WIDTH / sw, HEIGHT / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - WIDTH) // 2
    top = (new_h - HEIGHT) // 2
    src = src.crop((left, top, left + WIDTH, top + HEIGHT))
    base.paste(src, (0, 0))

    # Vertical vignette overlay so text stays readable.
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Build the overlay row by row.
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        # Top: very dark band (chrome blend) fading by 18% of height.
        # Mid: dark vignette ~50%, Bottom: ~70%.
        if t < 0.18:
            a = int(220 - (220 - 80) * (t / 0.18))
        elif t < 0.55:
            a = int(80 + (140 - 80) * ((t - 0.18) / (0.55 - 0.18)))
        else:
            a = int(140 + (180 - 140) * ((t - 0.55) / (1 - 0.55)))
        od.line([(0, y), (WIDTH, y)], fill=(15, 13, 24, max(0, min(255, a))))
    composite = Image.alpha_composite(base.convert("RGBA"), overlay)

    # Warm peach radial highlight, top-right, behind the avatar area.
    warm = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    wd = ImageDraw.Draw(warm)
    cx, cy = int(WIDTH * 0.78), int(HEIGHT * 0.30)
    rmax = 360
    for r in range(rmax, 0, -2):
        a = int(38 * (1 - r / rmax) ** 1.6)
        wd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 200, 175, a))
    warm = warm.filter(ImageFilter.GaussianBlur(radius=12))
    composite = Image.alpha_composite(composite, warm)

    return composite


# ---------- Pathfinder lockup (top-left) ----------
def draw_pf_lockup(draw, x, y, scale=1.0):
    """PF dot grid + 'pathfinder / foundry' wordmark."""
    r = int(2.6 * scale)
    gap = int(8 * scale)
    rows = [
        [True, True, True, True],
        [True, True, True, True],
        [True, False, True, False],
    ]
    for ry, row in enumerate(rows):
        for cx, on in enumerate(row):
            if not on:
                continue
            dx = x + cx * gap
            dy = y + ry * gap
            draw.ellipse((dx - r, dy - r, dx + r, dy + r), fill=ACCENT)
    # Wordmark
    word_x = x + 4 * gap + int(10 * scale)
    f_word = font(SANS_REG, int(18 * scale))
    f_word_it = font(SERIF_ITALIC, int(15 * scale))
    draw.text((word_x, y - int(2 * scale)), "pathfinder", font=f_word, fill=TEXT)
    # Right-align 'foundry' under the wordmark
    try:
        wbbox = draw.textbbox((0, 0), "pathfinder", font=f_word)
        word_w = wbbox[2] - wbbox[0]
    except Exception:
        word_w = 96
    fbbox = draw.textbbox((0, 0), "foundry", font=f_word_it)
    f_w = fbbox[2] - fbbox[0]
    draw.text((word_x + word_w - f_w, y + int(15 * scale)), "foundry",
              font=f_word_it, fill=TEXT)


# ---------- Avatar with PF yellow ring ----------
def make_avatar(diameter):
    src = Image.open(IMAGES / "MKrejci - CircleAvatar - WhiteBorder.png").convert("RGBA")
    # Square + resize.
    sw, sh = src.size
    side = min(sw, sh)
    src = src.crop(((sw - side) // 2, (sh - side) // 2,
                    (sw - side) // 2 + side, (sh - side) // 2 + side))
    src = src.resize((diameter, diameter), Image.LANCZOS)

    # Mask to circle (in case source has white border that's not perfectly round).
    mask = Image.new("L", (diameter, diameter), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, diameter, diameter), fill=255)

    out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    out.paste(src, (0, 0), mask)

    # Add a soft PF-yellow accent ring behind the avatar.
    ring_pad = 14
    ring = Image.new(
        "RGBA",
        (diameter + ring_pad * 2, diameter + ring_pad * 2),
        (0, 0, 0, 0),
    )
    rd = ImageDraw.Draw(ring)
    for i in range(ring_pad, 0, -1):
        a = int(60 * (i / ring_pad) ** 2)
        rd.ellipse(
            (ring_pad - i, ring_pad - i,
             diameter + ring_pad + i, diameter + ring_pad + i),
            outline=(255, 204, 100, a),
            width=2,
        )
    rd.ellipse(
        (ring_pad - 1, ring_pad - 1, diameter + ring_pad + 1, diameter + ring_pad + 1),
        outline=(255, 204, 100, 220),
        width=2,
    )
    ring.paste(out, (ring_pad, ring_pad), out)
    return ring


# ---------- Compose ----------
def build():
    img = make_background()
    draw = ImageDraw.Draw(img)

    # Pathfinder lockup, top-left.
    draw_pf_lockup(draw, 56, 56, scale=1.4)

    # Top-right tag.
    f_tag = font(SANS_BOLD, 13)
    tag = "JUNE 13, 2026"
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text((WIDTH - 56 - tw, 64), tag, font=f_tag, fill=(245, 245, 245, 140))

    # Eyebrow.
    f_eyebrow = font(SANS_BOLD, 18)
    eyebrow = "THRIVEHUB  ·  HANDS-ON WORKSHOP"
    draw.text((56, 188), eyebrow, font=f_eyebrow, fill=ACCENT,
              spacing=4)

    # Headline (three lines, big).
    f_head = font(SANS_BOLD, 58)
    lines = [
        "Test-Drive",
        "Entrepreneurship.",
    ]
    y = 252
    for line in lines:
        draw.text((56, y), line, font=f_head, fill=TEXT)
        y += 78

    # Tagline under headline, italic serif accent.
    f_tagline = font(SERIF_ITALIC, 26)
    draw.text((56, y + 14),
              "One Saturday morning. Any idea.",
              font=f_tagline, fill=ACCENT)
    draw.text((56, y + 50),
              "A loop you can run for life.",
              font=f_tagline, fill=ACCENT)

    # Byline at bottom-left.
    f_name = font(SANS_BOLD, 22)
    f_role = font(SANS_REG, 16)
    draw.text((56, HEIGHT - 92), "Lubica Lutz  &  Marc Krejci", font=f_name, fill=TEXT)
    draw.text((56, HEIGHT - 62), "ThriveHub  ·  Pathfinder Foundry",
              font=f_role, fill=TEXT_MUTED)

    # Avatar on the right.
    av_size = 340
    av = make_avatar(av_size)
    aw, ah = av.size
    ax = WIDTH - aw - 56
    ay = (HEIGHT - ah) // 2 + 16
    img.alpha_composite(av, (ax, ay))

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    build()
