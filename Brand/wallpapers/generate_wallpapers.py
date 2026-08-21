"""
Обои на телефон — «Шоу Балашова».
Два варианта: минимальный (безопасно под часы/иконки блокировки) и полный
(с именем и контактами, под домашний экран). Каждый — в двух популярных
разрешениях (Android 1080x2340, iPhone 1170x2532).

Запуск: python3 generate_wallpapers.py
Результат: файлы рядом, в Site/Brand/wallpapers/
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, os

def _find_dejavu_fonts():
    """Ищет папку со шрифтами DejaVu в типичных местах разных ОС —
    без этого скрипт был жёстко привязан к пути Debian/Ubuntu и падал
    на любой другой системе без объяснения причины."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/",  # Debian/Ubuntu
        "/usr/share/fonts/dejavu/",            # Fedora/RHEL
        "/usr/share/fonts/TTF/",               # Arch Linux
        "/opt/homebrew/share/fonts/",          # macOS, Homebrew cask font-dejavu
        "/Library/Fonts/",                     # macOS системные
        "C:/Windows/Fonts/",                   # Windows
    ]
    for c in candidates:
        if os.path.isdir(c) and any(f.startswith("DejaVu") for f in os.listdir(c)):
            return c
    raise FileNotFoundError(
        "Шрифты DejaVu не найдены. Установите: Ubuntu/Debian — `sudo apt install "
        "fonts-dejavu`; macOS — `brew install --cask font-dejavu`; Windows — "
        "скачайте с dejavu-fonts.github.io и пропишите путь вручную в переменной "
        "FONTS в начале этого скрипта."
    )


FONTS = _find_dejavu_fonts()
LOGO = "../logo-shou-balashova.jpg"

INK = (10, 7, 5)
GOLD = (253, 217, 69)
CREAM = (251, 243, 228)
GREY = (201, 187, 166)
CRIMSON = (200, 30, 30)

SIZES = {
    "android": (1080, 2340),
    "iphone": (1170, 2532),
}


def radial_glow(size, center, radius, color, max_opacity=90):
    w, h = size
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        alpha = int(max_opacity * (1 - i / steps) ** 1.6)
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        gd.ellipse(bbox, fill=color + (alpha,))
    return glow


def add_stars(img, n, seed, area, size_range=(2, 5)):
    random.seed(seed)
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = area
    for _ in range(n):
        x = random.randint(x0, x1)
        y = random.randint(y0, y1)
        s = random.randint(*size_range)
        op = random.randint(90, 220)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 240, 180, op))


def base_canvas(size):
    w, h = size
    img = Image.new("RGB", size, INK)
    glow = radial_glow(size, (w // 2, int(h * 0.62)), int(h * 0.5), (61, 34, 16), max_opacity=140)
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"))
    return img.convert("RGB")


def paste_logo(img, size_px, center):
    logo = Image.open(LOGO).convert("RGB").resize((size_px, size_px), Image.LANCZOS)
    mask = Image.new("L", (size_px, size_px), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, size_px, size_px], fill=255)
    glow = radial_glow(img.size, center, int(size_px * 0.72), GOLD, max_opacity=70)
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"))
    x = center[0] - size_px // 2
    y = center[1] - size_px // 2
    img.paste(logo, (x, y), mask)
    return img


def centered_text(draw, text, font, y, w, fill, tracking=0):
    if tracking:
        widths = [draw.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (w - total) / 2
        for ch, cw in zip(text, widths):
            draw.text((x, y), ch, font=font, fill=fill)
            x += cw + tracking
    else:
        tw = draw.textlength(text, font=font)
        draw.text(((w - tw) / 2, y), text, font=font, fill=fill)


def build_minimal(size, out):
    w, h = size
    img = base_canvas(size)
    add_stars(img, 26, seed=1, area=(0, 0, w, int(h * 0.45)))
    logo_d = int(w * 0.42)
    img = paste_logo(img, logo_d, (w // 2, int(h * 0.40)))
    d = ImageDraw.Draw(img)
    f_kicker = ImageFont.truetype(FONTS + "DejaVuSansMono.ttf", int(w * 0.032))
    centered_text(d, "АРТИСТ ЦИРКА", f_kicker, int(h * 0.565), w, GOLD, tracking=int(w * 0.02))
    img.save(out, quality=92)
    print("saved", out)


def build_full(size, out):
    w, h = size
    img = base_canvas(size)
    add_stars(img, 22, seed=2, area=(0, 0, w, int(h * 0.35)))
    logo_d = int(w * 0.30)
    img = paste_logo(img, logo_d, (w // 2, int(h * 0.24)))
    d = ImageDraw.Draw(img)

    f_name = ImageFont.truetype(FONTS + "DejaVuSerif-Bold.ttf", int(w * 0.105))
    f_show = ImageFont.truetype(FONTS + "DejaVuSerif-Italic.ttf", int(w * 0.05))
    f_kicker = ImageFont.truetype(FONTS + "DejaVuSansMono.ttf", int(w * 0.028))
    f_contact = ImageFont.truetype(FONTS + "DejaVuSansMono.ttf", int(w * 0.032))

    y = int(h * 0.40)
    centered_text(d, "НИКОЛАЙ", f_name, y, w, CREAM)
    y += int(w * 0.125)
    centered_text(d, "БАЛАШОВ", f_name, y, w, GOLD)
    y += int(w * 0.14)
    centered_text(d, "«Шоу Балашова»", f_show, y, w, GOLD)
    y += int(w * 0.09)
    centered_text(d, "АРТИСТ ЦИРКА · С 1984 ГОДА", f_kicker, y, w, GREY, tracking=int(w * 0.012))

    line_y = int(h * 0.78)
    d.line([(w * 0.32, line_y), (w * 0.68, line_y)], fill=GOLD, width=3)

    y2 = line_y + int(h * 0.025)
    for line in ["balashov-show.ru", "vk.ru/shou_spb"]:
        centered_text(d, line, f_contact, y2, w, GOLD)
        y2 += int(h * 0.032)

    img.save(out, quality=92)
    print("saved", out)


for name, size in SIZES.items():
    build_minimal(size, f"wallpaper-minimal-{name}.jpg")
    build_full(size, f"wallpaper-full-{name}.jpg")
