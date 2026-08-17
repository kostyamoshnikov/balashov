"""
Пересборка всех производных изображений из оригинального логотипа.

Раньше эти файлы собирались разовыми командами прямо в чате — без
сохранённого скрипта их нельзя было пересобрать без просьбы к Клоду
начать заново. Теперь это переиспользуемый скрипт.

Запуск (из Site/Brand/):
    python3 generate_brand_assets.py

Пересобирает:
  favicon-16/32/48.png, apple-touch-icon.png,
  avatar-200/320/512/1080.png, maskable-icon-192/512.png, og-image.png

Источник — logo-shou-balashova.jpg (оригинал, не трогаем).
"""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = "logo-shou-balashova.jpg"
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


def build_favicons_and_avatars():
    im = Image.open(SRC).convert("RGB")

    for size, name in [(16, "favicon-16"), (32, "favicon-32"), (48, "favicon-48"), (180, "apple-touch-icon")]:
        im.resize((size, size), Image.LANCZOS).save(f"{name}.png")

    for size, name in [(200, "avatar-200"), (320, "avatar-320"), (512, "avatar-512"), (1080, "avatar-1080")]:
        im.resize((size, size), Image.LANCZOS).save(f"{name}.png")

    for size, name in [(192, "maskable-icon-192"), (512, "maskable-icon-512")]:
        pad = int(size * 0.14)
        inner = size - pad * 2
        bg = Image.new("RGB", (size, size), (10, 6, 4))
        icon = im.resize((inner, inner), Image.LANCZOS)
        bg.paste(icon, (pad, pad))
        bg.save(f"{name}.png")

    print("favicons/avatars/maskable-icons: done")


def build_og_image():
    W, H = 1200, 630
    bg = Image.new("RGB", (W, H), (10, 6, 4))
    logo = Image.open(SRC).convert("RGB").resize((470, 470), Image.LANCZOS)
    bg.paste(logo, (60, 80))

    draw = ImageDraw.Draw(bg)
    f_title = ImageFont.truetype(FONTS + "DejaVuSerif-Bold.ttf", 44)
    f_sub = ImageFont.truetype(FONTS + "DejaVuSerif-Italic.ttf", 28)
    f_tag = ImageFont.truetype(FONTS + "DejaVuSansMono.ttf", 19)

    x = 570
    draw.text((x, 150), "ЦИРКОВЫЕ ШОУ", font=f_title, fill=(248, 220, 150))
    draw.text((x, 205), "В САНКТ-ПЕТЕРБУРГЕ", font=f_title, fill=(248, 220, 150))
    draw.text((x, 280), "Гибкие шесты · Ходулисты", font=f_sub, fill=(230, 180, 120))
    draw.text((x, 318), "Слинг · Экстрим · Лестница", font=f_sub, fill=(230, 180, 120))
    draw.text((x, 400), "VK.RU/SHOU_SPB", font=f_tag, fill=(200, 150, 100))

    bg.save("og-image.png")
    print("og-image.png: done")


if __name__ == "__main__":
    build_favicons_and_avatars()
    build_og_image()
