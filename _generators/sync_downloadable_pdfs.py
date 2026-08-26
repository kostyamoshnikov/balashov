"""
Копирует публичные PDF-материалы из Documents/ в Site/files/, откуда
их реально скачивают посетители сайта (about.html, booking.html —
ссылки «Пресс-кит» / «Коммерческое предложение», + их en/-зеркала).

Зачем отдельная копия, а не прямая ссылка на Documents/*.pdf: сайт
деплоится только из Site/* (см. DEPLOY.md — «Brand/ физически лежит
ВНУТРИ Site/, копировать Site/* значит копировать вообще всё, что
нужно сайту, за один раз») — Documents/ на живой сайт не попадает
вообще, ссылка на файл вне Site/ была бы битой на реальном хостинге.

Источник правды — Documents/*.pdf (собираются генераторами в
Documents/_sources/: build_presskit.js/build_commercial_offer.js —
RU, build_presskit_en.js/build_commercial_offer_en.js — EN, отдельные
файлы с переведённым содержимым, не автосборка из словаря). После
пересборки любого из них — перезапустить и этот скрипт, иначе на
сайте будет скачиваться устаревшая версия. verify_pack.py сверяет
md5 копий в Site/files/ с оригиналами в Documents/ и упадёт, если
забыть пересинхронизировать.

Технический райдер (Rider_template.pdf) сюда сознательно НЕ включён —
это шаблон с плейсхолдерами-подстановками («[уточнить]» и т.п.) под
конкретную площадку, публиковать его как есть непрофессионально;
полный райдер уходит организатору отдельным файлом после согласования
формата — см. note в booking.html.

Запуск (из Site/_generators/):
    python3 sync_downloadable_pdfs.py
"""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
DOCUMENTS = HERE / ".." / ".." / "Documents"
SITE_FILES = HERE / ".." / "files"

# имя файла в Documents/ -> публикуется под тем же именем в Site/files/
PUBLIC_PDFS = [
    "Nikolai_Balashov_PressKit.pdf",
    "Nikolai_Balashov_PressKit_EN.pdf",
    "Nikolai_Balashov_CommercialOffer.pdf",
    "Nikolai_Balashov_CommercialOffer_EN.pdf",
]

SITE_FILES.mkdir(exist_ok=True)

for name in PUBLIC_PDFS:
    src = DOCUMENTS / name
    dst = SITE_FILES / name
    if not src.exists():
        print(f"ПРОПУСК: {src} не найден")
        continue
    shutil.copy2(src, dst)
    print(f"{name}: скопирован ({dst.stat().st_size} байт)")
