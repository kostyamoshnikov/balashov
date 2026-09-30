#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR-коды для печатных материалов «Шоу Балашова» + страницы-редиректы
на сайте, на которые эти QR ведут.

КАК УСТРОЕНО С pack-v120
  QR на бумаге  →  https://show-balashov.ru/qr/<слаг>/   (своя страница)
                →  https://vk.ru/show_balashov?utm_source=qr&utm_medium=print&utm_campaign=<носитель>

Раньше QR вёл прямо в группу VK. Когда группу переименовали
(vk.ru/shou_spb → vk.ru/show_balashov, pack-v84), все напечатанные QR
стали вести в никуда, и починить это можно было только перепечаткой.
Теперь на бумаге — адрес на своём домене, а куда он ведёт, решает
маленькая HTML-страница в Site/qr/<слаг>/index.html. Следующее
переименование группы или переезд — правка одной строки здесь и
перевыкладка сайта, без перепечатки. Приём — из AELITA pack-v304 (свой
редирект для QR), без облачного сервиса: хватает статической страницы.

Плюс учёт: страница подключает Site/analytics.js, поэтому переход с
визитки/листовки виден в собственной статистике (StatsBot) — по пути
страницы /qr/card/ или /qr/leaflet/. VK входящие UTM никому не
показывает, так что раньше «сколько людей пришло с визитки» узнать
было нельзя вовсе.

Имена файлов qr-vk-*.png сохранены (на них ссылаются генератор визитки,
листовки и проверки), хотя QR теперь ведёт на свой сайт, а уже оттуда
в VK.

ГЕНЕРАТОР БЕЗ СЕТИ. QR строит _tools/DesignSystem/qr_gen.py (перенесён
из AELITA): reportlab → SVG → wkhtmltoimage → PNG, с проверкой
декодированием. Прежний `import qrcode` требовал pip и сеть — из-за
этого QR не перегенерировались с pack-v84 по pack-v119.

Запуск (из Site/Brand/):
    python3 generate_qr.py
После запуска пересобрать визитку и листовку:
    python3 ../../Documents/Print/generate_business_card.py   (из Documents/Print/)
    node _tools/DesignSystem/build_leaflet.js                  (из корня пака)
"""
import html
import os
import sys

# Без __pycache__ рядом с исходниками: verify_pack.py считает его мусором
# в паке, а этот файл импортируют и аудит, и сам он импортирует qr_gen.
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_tools', 'DesignSystem')))

SITE_URL = 'https://show-balashov.ru'
VK_URL = 'https://vk.ru/show_balashov'

# Носитель → слаг страницы, файл картинки, подпись. Единственный
# источник правды: отсюда же берут ожидаемые адреса проверки
# (_tools/Audit/run_audit.py, категория qr) — не копировать руками.
# Значения utm_campaign ('businesscard', 'leaflet') — идентификаторы уже
# существующей печатной кампании, не менять: смена разорвала бы
# статистику напечатанного тиража надвое (правило AELITA pack-v422).
PLACEMENTS = {
    'businesscard': {'slug': 'card', 'png': 'qr-vk-businesscard.png', 'label': 'визитка'},
    'leaflet': {'slug': 'leaflet', 'png': 'qr-vk-leaflet.png', 'label': 'листовка A6'},
}

# Палитра — та же, что у прежних QR и у визитки: тёмный по кремовому.
INK = (10, 7, 5)
CREAM = (251, 243, 228)


def qr_url(campaign):
    """Адрес, который кодируется в QR (печатается на бумаге)."""
    return f"{SITE_URL}/qr/{PLACEMENTS[campaign]['slug']}/"


def target_url(campaign):
    """Куда страница-редирект отправляет человека."""
    return f"{VK_URL}?utm_source=qr&utm_medium=print&utm_campaign={campaign}"


def page_path(campaign):
    return os.path.join(SITE_DIR, 'qr', PLACEMENTS[campaign]['slug'], 'index.html')


def render_page(campaign):
    p = PLACEMENTS[campaign]
    target = target_url(campaign)
    t_attr = html.escape(target, quote=True)
    t_js = target.replace('\\', '\\\\').replace("'", "\\'")
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Шоу Балашова — переходим в группу VK</title>
<!-- Страница-редирект для QR-кода ({html.escape(p['label'])}). СОБРАНО
     Site/Brand/generate_qr.py — не править руками, правка сотрётся при
     следующем запуске. Зачем она нужна — см. шапку generate_qr.py.
     В sitemap.xml не входит, в поиске не показывается (noindex). -->
<meta name="robots" content="noindex, follow">
<link rel="icon" href="../../favicon.ico">
<meta http-equiv="refresh" content="2; url={t_attr}">
<style>
html,body{{margin:0;background:#0A0705;color:#FBF3E4;font-family:'Public Sans',-apple-system,'Segoe UI',Roboto,Arial,sans-serif}}
main{{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;box-sizing:border-box}}
h1{{font-size:20px;font-weight:600;margin:0 0 12px}}
p{{font-size:16px;line-height:1.6;margin:0 0 16px;color:#E8DCC4}}
a{{color:#FDD945}}
.go{{display:inline-block;padding:14px 24px;border:1.5px solid #FDD945;border-radius:999px;text-decoration:none;font-weight:600}}
.small{{font-size:14px}}
</style>
</head>
<body>
<main>
  <h1>Открываем группу «Шоу Балашова» во ВКонтакте…</h1>
  <p>Если ничего не произошло — нажмите кнопку.</p>
  <p><a class="go" href="{t_attr}">Перейти в группу VK</a></p>
  <p class="small">Сайт артиста: <a href="../../index.html">show-balashov.ru</a> · <span lang="en">Opening VK…</span></p>
</main>
<!-- Своя статистика: просмотр этой страницы = переход по QR с носителя
     «{html.escape(p['label'])}» (путь /qr/{p['slug']}/). Пока StatsBot не
     задеплоен, событие никуда не уходит — переход в VK работает всё равно. -->
<script src="../../analytics.js"></script>
<script>
(function () {{
  var target = '{t_js}';
  // PRESERVE_QUERY (приём AELITA pack-v422): если к адресу QR дописали
  // свои utm_* (например, для отдельного тиража), они заменяют метки по
  // умолчанию — иначе при переходе они бы потерялись.
  try {{
    var inc = new URLSearchParams(location.search), out = new URL(target);
    inc.forEach(function (v, k) {{ if (/^utm_/i.test(k)) out.searchParams.set(k, v); }});
    target = out.toString();
  }} catch (e) {{}}
  // Сначала отдаём событие статистике (sendBeacon переживает уход со
  // страницы), потом уходим. replace — чтобы кнопка «Назад» в VK не
  // возвращала на эту промежуточную страницу.
  try {{ if (window.__balashovFlush) window.__balashovFlush(); }} catch (e) {{}}
  location.replace(target);
}})();
</script>
</body>
</html>
"""


def recolor(path):
    """Чёрный по белому (qr_gen) → тёмный по кремовому, как прежние QR."""
    from PIL import Image
    im = Image.open(path).convert('L')
    rgb = Image.new('RGB', im.size, CREAM)
    mask = im.point(lambda v: 255 if v < 128 else 0)
    rgb.paste(Image.new('RGB', im.size, INK), (0, 0), mask)
    rgb.save(path)


def main():
    from qr_gen import make_qr_png, _verify
    for campaign, p in PLACEMENTS.items():
        url = qr_url(campaign)
        png = os.path.join(HERE, p['png'])
        make_qr_png(url, png, target_px='card')
        recolor(png)
        _verify(png, url)  # и после перекраски — палитра не должна мешать сканеру
        out = page_path(campaign)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(render_page(campaign))
        print(f"{p['png']}: {url} → {target_url(campaign)} (проверено декодированием)")
        print(f"  страница: {os.path.relpath(out, os.path.join(SITE_DIR, '..'))}")


if __name__ == '__main__':
    main()
