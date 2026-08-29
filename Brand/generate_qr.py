"""
Пересборка QR-кодов на группу VK — по одному файлу на каждое место
размещения, с собственной UTM-меткой, чтобы отличать источник перехода
(визитка vs листовка vs что угодно добавится позже).

Раньше был один общий qr-vk.png на все носители — теперь каждый
физический материал получает свою ссылку и свою картинку:
  • qr-vk-businesscard.png — визитка (Documents/Print/)
  • qr-vk-leaflet.png       — раздаточная листовка A6 (Documents/Print/)

Схема UTM — та же, что уже используется в analytics.js и в Яндекс.Директ
кампании (utm_source / utm_medium / utm_campaign):
  utm_source=qr, utm_medium=print, utm_campaign=<название носителя>

ЧЕСТНО ПРО ОГРАНИЧЕНИЕ: ссылка ведёт на страницу сообщества VK, а не на
наш сайт — VK не показывает входящие utm-параметры в своей статистике
сообщества (это не Яндекс.Метрика). Метка полезна как минимум для
ручной сверки (например, если человек, который написал в сообщество,
пришлёт скриншот с адресной строки — по utm сразу видно, с визитки он
или с листовки), но АВТОМАТИЧЕСКОГО дашборда «сколько заявок с визитки»
это не даёт. Если понадобится настоящая автоматическая аналитика по
QR — логичный следующий шаг: увести QR на короткий редирект на своём
домене (например, balashov-show.ru/qr/card), который сначала
логируется через уже существующий Site/analytics.js (он умеет читать
utm_* — см. код там), а потом уводит на VK. Это отдельная задача, здесь
не делается.

Если ссылка на группу или список носителей изменится — поменять здесь
и перезапустить.

Запуск (из Site/Brand/):
    python3 generate_qr.py
"""
import qrcode

BASE_URL = "https://vk.ru/show_balashov"

# место размещения -> имя файла
PLACEMENTS = {
    "businesscard": "qr-vk-businesscard.png",
    "leaflet": "qr-vk-leaflet.png",
}

for campaign, filename in PLACEMENTS.items():
    url = f"{BASE_URL}?utm_source=qr&utm_medium=print&utm_campaign={campaign}"
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0A0705", back_color="#FBF3E4")
    img.save(filename)
    print(f"{filename}: done ({url})")
