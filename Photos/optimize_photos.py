"""
Пересборка отобранных и оптимизированных фото для сайта/презентации.

Оригиналы (28 фото от заказчика, pack-v33) лежат рядом, рассортированные
по номерам: lestnitsa/, truba-transformer/, shesty/, turnik-01.jpg.
Этот скрипт — не просто пережатие: конкретный выбор ИМЕННО ЭТИХ файлов
из каждой папки — редакторское решение (лучший ракурс/свет/композиция),
сделанное один раз и здесь задокументированное. Если позже появятся
новые фото или нужно заменить выбор — редактировать список SELECTIONS.

Запуск (из Site/Photos/):
    python3 optimize_photos.py
Результат — web/*.jpg (максимум 900px по ширине, JPEG quality 82).
"""
import os
from PIL import Image

MAXW = 900
QUALITY = 82

# (путь к оригиналу, имя на выходе)
SELECTIONS = [
    ("lestnitsa/lestnitsa-07.jpg", "lestnitsa-1.jpg"),  # артист на лестнице, толпа детей аплодирует
    ("lestnitsa/lestnitsa-01.jpg", "lestnitsa-2.jpg"),  # зимнее выступление, сетка на фоне
    ("lestnitsa/lestnitsa-06.jpg", "lestnitsa-3.jpg"),  # студийное фото, синий фон, костюм-солнце
    ("truba-transformer/truba-09.jpg", "truba-1.jpg"),  # девочка с шаром и труба на театральной сцене
    ("truba-transformer/truba-01.jpg", "truba-2.jpg"),  # два артиста в костюмах на сцене
    ("truba-transformer/truba-03.jpg", "truba-3.jpg"),  # человек-пружинка, серебряный костюм, крыша
    ("shesty/shesty-01.jpg", "shesty-1.jpg"),           # парный номер на шестах
    ("shesty/shesty-02.jpg", "shesty-2.jpg"),           # гибкие шесты на фестивале
    ("shesty/shesty-10.jpg", "shesty-3.jpg"),           # групповой номер с ходулистами и шестами
    ("turnik-01.jpg", "turnik-1.jpg"),                  # турник, зима, номерок на груди
]

os.makedirs("web", exist_ok=True)

for src, out in SELECTIONS:
    if not os.path.exists(src):
        print(f"ПРОПУЩЕНО (нет файла): {src}")
        continue
    im = Image.open(src).convert("RGB")
    if im.width > MAXW:
        ratio = MAXW / im.width
        im = im.resize((MAXW, int(im.height * ratio)), Image.LANCZOS)
    out_path = os.path.join("web", out)
    im.save(out_path, quality=QUALITY, optimize=True)
    print(out, im.size, f"{os.path.getsize(out_path)//1024} KB")
