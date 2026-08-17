"""
Увеличенные версии оригинального логотипа для печати баннеров —
без искажений (Lanczos-интерполяция, ничего не «дорисовывается»,
только честное увеличение уже существующих пикселей).

См. _archive/brand_vector_logo_attempt/README.md — почему это
увеличение оригинала, а не векторная перерисовка (заказчик сравнил
оба варианта и выбрал первый: важно «точь-в-точь», а не стилизация).

Запуск (из Site/Brand/):
    python3 generate_banner_sizes.py
Результат — banner-sizes/logo-{size}px.png
"""
import os
from PIL import Image

SRC = "logo-shou-balashova.jpg"
OUT_DIR = "banner-sizes"

# ~50-100 DPI достаточно для баннера, который смотрят с нескольких метров
TARGETS = {
    "logo-2000px.png": 2000,   # ~50×50см при 100dpi / ~1×1м при 50dpi
    "logo-4000px.png": 4000,   # ~1×1м при 100dpi / ~2×2м при 50dpi
    "logo-8000px.png": 8000,   # ~2×2м при 100dpi / ~4×4м при 50dpi
}

os.makedirs(OUT_DIR, exist_ok=True)
src = Image.open(SRC).convert("RGB")
print("source:", src.size)

for name, size in TARGETS.items():
    up = src.resize((size, size), Image.LANCZOS)
    up.save(os.path.join(OUT_DIR, name), optimize=True)
    print(name, up.size)
