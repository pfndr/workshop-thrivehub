#!/usr/bin/env python3
"""Build the two in-room printables for Test-Drive Entrepreneurship.

1. worksheet.pdf   - Fears (individual) + Hypothesis mad-lib (team of three).
                     US Letter portrait, one per person.
2. role-cards.pdf  - US Letter LANDSCAPE, three columns (Guide / Scribe / Fresh Eyes)
                     with dashed cut guides. Print 10, cut into 3 cards each.

Print-friendly: white background, dark ink, PF Yellow accents.
Text stays emoji-free in Helvetica (no glyphs). Role-card emojis are rendered
to PNG via a color-emoji font and embedded as images, which prints fine.
"""

import os
from pathlib import Path

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

PW, PH = letter  # portrait 612 x 792

YELLOW = HexColor("#FFCC64")
YELLOW_TINT = HexColor("#FFF4DC")
DARK = HexColor("#272727")
GRAY = HexColor("#7a7a7a")
LIGHT_LINE = HexColor("#c9c9c9")
RED = HexColor("#c0392b")
RED_TINT = HexColor("#fdecea")

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "printables"
ICON_DIR = OUT_DIR / "icons"

FOOTER_LEFT = "Test-Drive Entrepreneurship  ·  Lubica Lutz & Marc Krejci  ·  ThriveHub · Pathfinder Foundry"


# ------------------------------------------------------------ emoji icons
def emoji_font_path():
    candidates = [
        "/System/Library/Fonts/Apple Color Emoji.ttc",          # macOS
        "/tmp/NotoColorEmoji.ttf",                              # sandbox download
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",    # linux package
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None


def render_emoji_png(ch, out_path, target=256):
    """Rasterize one emoji to a transparent PNG. Returns True on success."""
    from PIL import Image, ImageDraw, ImageFont

    fp = emoji_font_path()
    if not fp:
        return False
    for size in (137, 109, 160, 96, 64):  # bitmap emoji fonts accept fixed strikes
        try:
            f = ImageFont.truetype(fp, size)
            img = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((size // 2, size // 2), ch, font=f, embedded_color=True)
            bbox = img.getbbox()
            if not bbox:
                continue
            img = img.crop(bbox)
            img.thumbnail((target, target), Image.LANCZOS)
            img.save(out_path)
            return True
        except Exception:
            continue
    return False


# ------------------------------------------------------------ shared bits
def accent_bar(c, x, y, h=12):
    c.setFillColor(YELLOW)
    c.rect(x, y - 2, 4, h + 2, stroke=0, fill=1)


def ruled_line(c, x1, x2, y):
    c.setStrokeColor(LIGHT_LINE)
    c.setLineWidth(0.8)
    c.line(x1, y, x2, y)


def wrap_text(c, text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- worksheet
def build_worksheet(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    MX = 54
    width = PW - 2 * MX

    # Header
    y = PH - 56
    c.setFillColor(YELLOW)
    c.rect(MX, y + 14, 28, 5, stroke=0, fill=1)
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MX, y, "TEST-DRIVE ENTREPRENEURSHIP  ·  THRIVEHUB  ·  JUNE 13, 2026")
    y -= 26
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MX, y, "Fears & Hypothesis")
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(GRAY)
    c.drawRightString(PW - MX, y, "Name: ______________________")

    # ---- FEARS (individual) ----
    y -= 44
    accent_bar(c, MX, y)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MX + 12, y, "FEARS")
    c.setFont("Helvetica-Oblique", 9.5)
    c.setFillColor(GRAY)
    c.drawString(MX + 66, y, "yours alone, no sharing required")
    y -= 28
    for _ in range(4):
        ruled_line(c, MX, PW - MX, y)
        y -= 26

    # ---- HYPOTHESIS (team) ----
    y -= 16
    accent_bar(c, MX, y)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MX + 12, y, "HYPOTHESIS")
    c.setFont("Helvetica-Oblique", 9.5)
    c.setFillColor(GRAY)
    c.drawString(MX + 100, y, "one per team of three  ·  small wedge, one customer type, one test")
    y -= 30

    rows = [
        ("If we help", "customer", "the specific person experiencing the problem"),
        ("solve", "problem", "what they are facing, described in detail"),
        ("with", "solution", "the approach you will use to solve it"),
        ("they will choose it over", "competitors", "who or what else they could choose"),
        ("because our solution is", "differentiation", "what makes your approach unique"),
    ]
    for lead, slot, definition in rows:
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MX, y, lead)
        lead_w = c.stringWidth(lead, "Helvetica-Bold", 11)
        line_x1 = MX + lead_w + 8
        ruled_line(c, line_x1, PW - MX, y - 2)
        c.setFillColor(GRAY)
        c.setFont("Helvetica-Oblique", 8.5)
        c.drawString(line_x1, y - 13, f"[ {slot} ]  {definition}")
        y -= 40

    # The test: highlighted box, two write-in lines
    box_h = 86
    y_box_top = y + 8
    c.setFillColor(YELLOW_TINT)
    c.setStrokeColor(YELLOW)
    c.setLineWidth(1.4)
    c.roundRect(MX - 8, y_box_top - box_h, width + 16, box_h, 8, stroke=1, fill=1)
    yy = y_box_top - 20
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MX, yy, "and we will prove it by")
    lead_w = c.stringWidth("and we will prove it by", "Helvetica-Bold", 11)
    ruled_line(c, MX + lead_w + 8, PW - MX, yy - 2)
    yy -= 26
    ruled_line(c, MX, PW - MX, yy - 2)
    yy -= 16
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(MX, yy, "[ the test ]  measurable and falsifiable, e.g. \"3 of 5 testers finish the flow unprompted\"")

    # Keep-it note, centered under the hypothesis box
    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(PW / 2, y_box_top - box_h - 24, "Keep this sheet. We come back to it at the end.")

    # Footer
    c.setFillColor(YELLOW)
    c.rect(MX, 46, 4, 10, stroke=0, fill=1)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(MX + 10, 48, FOOTER_LEFT)

    c.showPage()
    c.save()


# ---------------------------------------------------------------- role cards
CARDS = [
    {
        "name": "GUIDE",
        "aka": "aka Director",
        "emoji": "\U0001F9ED",  # compass
        "tagline": "Set the scene, then go quiet.",
        "job": [
            "Welcome your Fresh Eyes tester.",
            "Words only: who they are, where they are, what they are doing.",
            "Keep all artifacts hidden while you set the scene.",
            "Reveal the prototype. Then silence.",
        ],
        "keep": '"There are no wrong answers. If you\'re stuck, that\'s on us, not you."',
        "pause": "pause the test, quickly adjust the prototype, then resume. Never direct them.",
        "dont": ["Defend (pitch)", "Direct", "Design", "Research"],
    },
    {
        "name": "SCRIBE",
        "aka": "aka Note Taker",
        "emoji": "\U0001F4DD",  # memo
        "tagline": "Capture every signal.",
        "job": [
            "Paper and pen ready before the test starts.",
            "Watch the face: surprise, confusion, delight.",
            "Write quotes down word for word.",
            "Note where they get stuck. Stuck is data.",
        ],
        "keep": None,
        "dont": ["Help", "Explain", "Interrupt"],
    },
    {
        "name": "FRESH EYES",
        "aka": "aka Deep Diver",
        "emoji": "\U0001F440",  # eyes
        "tagline": "Walk in fresh. React out loud.",
        "job": [
            "Leave your group. Join one you haven't visited.",
            "Become the person the Guide describes.",
            "Verbalize everything: stuck, excited, confused.",
            "Act naturally. Don't be nice. Be honest.",
        ],
        "keep": None,
        "dont": ["Pretend to understand", "Stay polite and silent"],
        "after": "After the timer: return to your home group.",
    },
]


def build_role_cards(path):
    # LANDSCAPE letter: 792 x 612. Three columns of 264pt (3.67 in), full height.
    W, H = landscape(letter)
    c = canvas.Canvas(str(path), pagesize=landscape(letter))
    col_w = W / 3.0
    pad = 24

    # Pre-render emoji icons
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    icons = {}
    for card in CARDS:
        p = ICON_DIR / f"{card['name'].lower().replace(' ', '-')}.png"
        if render_emoji_png(card["emoji"], p):
            icons[card["name"]] = str(p)

    # Dashed cut guides
    c.setStrokeColor(LIGHT_LINE)
    c.setLineWidth(0.7)
    c.setDash(4, 5)
    for x in (col_w, 2 * col_w):
        c.line(x, 14, x, H - 14)
    c.setDash()

    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(W / 2, H - 10, "cut along the dashed lines  ·  one card per person  ·  pass left when the loop ends")

    for i, card in enumerate(CARDS):
        x0 = i * col_w
        inner_w = col_w - 2 * pad
        tx = x0 + pad

        # Top band with big emoji + name
        band_h = 92
        band_top = H - 22
        c.setFillColor(YELLOW)
        c.rect(x0 + 10, band_top - band_h, col_w - 20, band_h, stroke=0, fill=1)
        icon = icons.get(card["name"])
        icon_size = 60
        if icon:
            c.drawImage(icon, x0 + 22, band_top - band_h + (band_h - icon_size) / 2,
                        width=icon_size, height=icon_size, mask="auto")
        name_x = x0 + 22 + (icon_size + 14 if icon else 0)
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 19)
        c.drawString(name_x, band_top - band_h / 2 + 2, card["name"])
        c.setFont("Helvetica", 9)
        c.drawString(name_x, band_top - band_h / 2 - 14, card["aka"])

        y = band_top - band_h - 26
        c.setFillColor(DARK)
        c.setFont("Helvetica-Oblique", 11.5)
        for ln in wrap_text(c, card["tagline"], "Helvetica-Oblique", 11.5, inner_w):
            c.drawString(tx, y, ln)
            y -= 15
        y -= 12

        # YOUR JOB
        accent_bar(c, tx, y, h=9)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(tx + 10, y, "YOUR JOB")
        y -= 19
        for item in card["job"]:
            c.setFillColor(YELLOW)
            c.rect(tx, y - 1, 3, 9, stroke=0, fill=1)
            c.setFillColor(DARK)
            c.setFont("Helvetica", 9.5)
            for ln in wrap_text(c, item, "Helvetica", 9.5, inner_w - 12):
                c.drawString(tx + 10, y, ln)
                y -= 13
            y -= 7

        # Keep ready quote + escape-hatch (Guide only)
        if card.get("keep") or card.get("pause"):
            y -= 4
            sections = []
            if card.get("keep"):
                sections.append(wrap_text(c, "Keep ready: " + card["keep"], "Helvetica-Oblique", 9, inner_w - 16))
            if card.get("pause"):
                sections.append(wrap_text(c, "If they truly can't move: " + card["pause"], "Helvetica-Oblique", 9, inner_w - 16))
            total_lines = sum(len(s) for s in sections)
            section_gap = 6
            box_h = total_lines * 12 + 16 + section_gap * (len(sections) - 1)
            c.setFillColor(YELLOW_TINT)
            c.roundRect(tx - 2, y - box_h + 10, inner_w + 4, box_h, 6, stroke=0, fill=1)
            c.setFillColor(DARK)
            c.setFont("Helvetica-Oblique", 9)
            yy = y - 4
            for idx, section in enumerate(sections):
                if idx > 0:
                    yy -= section_gap
                for ln in section:
                    c.drawString(tx + 6, yy, ln)
                    yy -= 12
            y = yy - 14

        # DO NOT box
        y -= 6
        items = card["dont"]
        box_h = 26 + len(items) * 15
        c.setFillColor(RED_TINT)
        c.setStrokeColor(RED)
        c.setLineWidth(1)
        c.roundRect(tx - 2, y - box_h + 10, inner_w + 4, box_h, 6, stroke=1, fill=1)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(tx + 6, y - 6, "DO NOT")
        yy = y - 23
        for item in items:
            c.setFillColor(RED)
            c.setFont("Helvetica", 9.5)
            c.drawString(tx + 6, yy, "x")
            c.setFillColor(DARK)
            c.drawString(tx + 18, yy, item)
            yy -= 15
        y = y - box_h - 8

        # After-the-timer note (Fresh Eyes)
        if card.get("after"):
            c.setFillColor(GRAY)
            c.setFont("Helvetica-Oblique", 9)
            for ln in wrap_text(c, card["after"], "Helvetica-Oblique", 9, inner_w):
                c.drawString(tx, y, ln)
                y -= 12

        # Bottom pass note
        c.setFillColor(YELLOW)
        c.rect(tx, 26, 3, 9, stroke=0, fill=1)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 7.5)
        c.drawString(tx + 9, 28, "Next loop: hand this card to the next person.")

    c.showPage()
    c.save()


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_worksheet(OUT_DIR / "worksheet.pdf")
    build_role_cards(OUT_DIR / "role-cards.pdf")
    print("built printables/worksheet.pdf and printables/role-cards.pdf (landscape)")
