"""
Пересборка QR-кода на группу VK.

Используется на визитке (Documents/Print/) и в раздаточной листовке A6.
Если ссылка на группу когда-нибудь изменится — поменять URL здесь и
перезапустить, оба места (визитка, листовка) сами подхватят новый файл
при следующей пересборке (они просто ссылаются на qr-vk.png по пути).

Запуск (из Site/Brand/):
    python3 generate_qr.py
"""
import qrcode

URL = "https://vk.ru/shou_spb"

qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="#0A0705", back_color="#FBF3E4")
img.save("qr-vk.png")
print(f"qr-vk.png: done ({URL})")
