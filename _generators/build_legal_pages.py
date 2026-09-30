#!/usr/bin/env python3
"""Генератор юридических страниц сайта (cookies.html, terms.html).

Страницы собираются из шаблона Site/privacy.html — берётся всё, кроме
содержательных секций: шапка, навигация, стили, футер, подключение
скриптов. Так новые документы гарантированно совпадают с остальным
сайтом по вёрстке и не разъезжаются при будущих правках шаблона —
достаточно перезапустить этот скрипт.

Запуск:  cd Site/_generators && python3 build_legal_pages.py

Почему генератор, а не руками: две страницы * две языковые версии =
четыре файла с одинаковой обвязкой. Руками это четыре места, где
можно забыть обновить навигацию или футер.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)


def shell(template_path, title, tag, body_html, current_file):
    """Берёт шаблон и подменяет заголовок, подзаголовок и секции."""
    with open(template_path, encoding="utf-8") as f:
        c = f.read()

    # 1. Заголовок и подзаголовок в hero
    c = re.sub(r"<h1>[^<]*</h1>", f"<h1>{title}</h1>", c, count=1)
    c = re.sub(r'<p class="tag">[^<]*</p>', f'<p class="tag">{tag}</p>', c, count=1)

    # 2. Заменяем содержательные секции целиком
    start = c.find("<section>")
    end = c.rfind("</section>") + len("</section>")
    c = c[:start] + body_html.strip() + c[end:]

    # 3. <title> и мета-описания — чтобы в выдаче и во вкладке было верно
    c = re.sub(r"<title>[^<]*</title>", f"<title>{title} — Николай Балашов</title>", c, count=1)
    c = re.sub(r'(<meta name="description" content=")[^"]*(")', rf"\1{tag}\2", c, count=1)
    c = re.sub(r'(<meta property="og:title" content=")[^"]*(")', rf"\1{title}\2", c, count=1)
    c = re.sub(r'(<meta property="og:description" content=")[^"]*(")', rf"\1{tag}\2", c, count=1)
    c = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', rf"\1{tag}\2", c, count=1)

    # 4. Перекрёстные ссылки в футере. У privacy.html (шаблона)
    # намеренно минимальный футер без ссылки на саму себя — новые
    # страницы это наследуют, и с них некуда перейти к двум соседним
    # документам. Подставляем ссылки на другие юридические страницы,
    # исключая текущую.
    # ⚠️ terms.html СОЗНАТЕЛЬНО отсутствует в списке: документ содержит
    # незаполненные прочерки (предоплата, отмена, перенос) и помечен
    # как черновик. Публично ссылаться на него нельзя — посетитель
    # наткнётся на «____». Сам файл в паке остаётся, чтобы было что
    # заполнять. Как только Николай даст условия и прочерки исчезнут —
    # вернуть строку ("terms.html", "Условия работы") сюда и в футеры
    # остальных страниц (см. TASKS.md).
    others = [
        ("privacy.html", "Политика конфиденциальности"),
        ("cookies.html", "Файлы cookie"),
    ]
    links = " · ".join(
        f'<a href="{href}">{name}</a>' for href, name in others if href != current_file
    )
    c = c.replace(
        '<p class="foot-note">© Николай Балашов</p>',
        f'<p class="foot-note">{links}</p>\n    <p class="foot-note">© Николай Балашов</p>',
        1,
    )
    # 5. canonical и og:url — унаследованные от шаблона указывали бы на
    # privacy.html, из-за чего поисковик считал бы новые страницы её
    # копиями и не индексировал. Поймано проверкой verify_pack.py.
    # Префикс en/ для английских версий — определяем по шаблону, из
    # которого страница собрана (Site/en/privacy.html -> en/).
    prefix = "en/" if "/en/" in template_path.replace(os.sep, "/") else ""
    c = re.sub(r'(<link rel="canonical" href="https://show-balashov\.ru/)[^"]*(")',
               rf"\1{prefix}{current_file}\2", c, count=1)
    c = re.sub(r'(<meta property="og:url" content="https://show-balashov\.ru/)[^"]*(")',
               rf"\1{prefix}{current_file}\2", c, count=1)

    # 6. hreflang и переключатель языка — в паке принято, что у каждой
    # страницы есть языковая пара (это проверяет verify_pack.py).
    # Подставляем ссылки на EN-версию этой же страницы.
    c = re.sub(r'(hreflang="ru" href="https://show-balashov\.ru/)[^"]*(")', rf"\1{current_file}\2", c, count=1)
    c = re.sub(r'(hreflang="en" href="https://show-balashov\.ru/en/)[^"]*(")', rf"\1{current_file}\2", c, count=1)
    c = re.sub(r'(hreflang="x-default" href="https://show-balashov\.ru/)[^"]*(")', rf"\1{current_file}\2", c, count=1)
    c = re.sub(r'(<a href=")[^"]*(" class="lang-switch">EN</a>)', rf"\1en/{current_file}\2", c, count=1)
    return c


def sec(title, paragraphs, tinted=False):
    cls = ' class="tinted"' if tinted else ""
    ps = "\n".join(f"      <p>{p}</p>" for p in paragraphs)
    return f"""<section{cls}>
  <div class="wrap">
    <div class="section-head">
      <h2 class="serif">{title}</h2>
    </div>
    <div class="body-copy">
{ps}
    </div>
  </div>
</section>
"""


# ── COOKIES (RU) ────────────────────────────────────────────────────
COOKIES_RU = "".join([
    sec("Коротко", [
        "Этот сайт не использует cookie для слежки за посетителями и не передаёт данные рекламным сетям. Ниже — что именно и зачем сохраняется в браузере.",
        "Документ описывает текущее состояние. Если что-то изменится — например, будет подключена внешняя аналитика — этот текст будет обновлён до её включения, а не после.",
    ]),
    sec("Что сайт сохраняет сейчас", [
        "<b>Техническая память вкладки (sessionStorage).</b> Собственный счётчик сайта записывает случайную строку — она нужна, чтобы отличить «один человек открыл три страницы» от «три разных человека открыли по одной». Строка не содержит никаких сведений о вас, живёт только пока открыта вкладка и исчезает при её закрытии. При следующем визите генерируется новая — связать между собой два ваших захода она не позволяет.",
        "<b>Метки рекламных кампаний.</b> Если вы пришли по рекламной ссылке, в адресе страницы могут быть метки вида <code>utm_source</code>. Они сохраняются там же, в памяти вкладки, чтобы понимать, какая реклама приводит людей. Метки — часть адреса, который и так виден вам в адресной строке браузера.",
        "<b>Настоящих cookie сайт сейчас не ставит вовсе</b> — ни своих, ни сторонних.",
    ], tinted=True),
    sec("Что может появиться позже", [
        "В коде сайта подготовлены, но <b>не активированы</b> два счётчика: Яндекс.Метрика и пиксель VK Рекламы. Оба, если их включить, ставят настоящие cookie и передают обезличенные сведения о посещении своим сервисам — соответственно Яндексу и VK.",
        "Пока они выключены, этот раздел носит справочный характер. Перед их включением на сайте появится баннер согласия на использование cookie, а этот документ будет дополнен описанием того, что именно они собирают.",
    ]),
    sec("Как отказаться", [
        "Поскольку настоящих cookie сейчас нет, отдельного отказа не требуется. Память вкладки очищается сама при её закрытии, а также вручную — через настройки браузера («Очистить данные сайта»).",
        "Если вы хотите заранее исключить любую аналитику, в большинстве браузеров работает режим инкогнито либо блокировщики скриптов — сайт полностью функционален и с ними: формы, галерея и страницы номеров работают без счётчиков.",
    ], tinted=True),
    sec("Вопросы", [
        'Если что-то в этом документе кажется неясным — напишите: <a href="mailto:balashov.show.ru@gmail.com">balashov.show.ru@gmail.com</a> или позвоните <a href="tel:+79119138374">+7 911 913-83-74</a>.',
        'Про обработку персональных данных из форм заявки и отзыва — в <a href="privacy.html">политике конфиденциальности</a>.',
    ]),
])

# ── TERMS / ОФЕРТА (RU) ─────────────────────────────────────────────
# ⚠️ Плейсхолдеры ____ намеренно оставлены там, где нет решения
# заказчика. Выдумывать проценты предоплаты и сроки отмены нельзя —
# это условия, по которым потом будут спорить о деньгах.
TERMS_RU = "".join([
    sec("О чём этот документ", [
        "Здесь описано, как строится работа: что входит в услугу, как согласуются детали, как считается стоимость и что происходит при изменении планов. Документ носит информационный характер и не заменяет договор — при работе с организациями оформляется отдельный договор оказания услуг.",
        "⚠️ <b>Черновик.</b> Несколько условий (предоплата, сроки отмены, перенос даты) отмечены прочерками — их нужно заполнить до публикации страницы на сайте. Пока они не определены, документ размещать не следует.",
    ]),
    sec("Что входит в услугу", [
        "Выступление артиста с одним или несколькими цирковыми номерами по согласованной программе. Артист приезжает со своим реквизитом и в своих костюмах.",
        "Конкретный номер, его продолжительность и порядок выступления согласовываются заранее — под сценарий вашего мероприятия. Хронометраж отдельных номеров: от 6 до 12 минут; несколько номеров могут быть объединены в программу.",
        'Технические требования к площадке (свободное место, высота потолка, покрытие) зависят от номера. Кратко они описаны на <a href="booking.html">странице заявки</a>, полный технический райдер под конкретную площадку высылается после согласования формата.',
    ], tinted=True),
    sec("Как согласуется заказ", [
        "1. Вы присылаете заявку: дата, город и площадка, формат мероприятия, пожелания к номеру.",
        "2. В течение 1–2 дней приходит ответ с предложением по номерам и расчётом стоимости.",
        "3. Согласовываются детали программы и технический райдер.",
        "4. Дата бронируется. Для организаций оформляется договор оказания услуг и счёт на оплату.",
    ]),
    sec("Стоимость", [
        "Фиксированного прайса нет: стоимость зависит от номера, продолжительности выступления, даты и города. Поэтому расчёт делается индивидуально под каждое обращение.",
        "Выезд за пределы Санкт-Петербурга и Ленинградской области рассчитывается отдельно. При выезде в другой город организатор обеспечивает проживание, питание и помещение для подготовки — это оговаривается заранее и входит в согласованные условия.",
        "Предоплата: ____ % от стоимости, вносится ____. Окончательный расчёт — ____.",
    ], tinted=True),
    sec("Отмена и перенос", [
        "Если мероприятие отменяется по вашей инициативе менее чем за ____ дней до даты выступления, предоплата ____.",
        "Перенос даты возможен ____ при условии, что новая дата свободна.",
        "Если выступление не может состояться по обстоятельствам, не зависящим ни от одной из сторон (погода на открытой площадке, официальные ограничения, болезнь артиста), стороны согласовывают перенос или возврат — конкретный порядок фиксируется в договоре.",
    ]),
    sec("Безопасность и участие зрителей", [
        "Часть номеров предполагает участие зрителей: подъём на гибкие шесты, соревнование на турнике, участие гостя в номере «Труба-трансформер». Участие всегда добровольное.",
        "Перед участием артист проводит инструктаж и не допускает к участию лиц с признаками опьянения. Организатор со своей стороны обеспечивает свободную безопасную зону и не допускает участия несовершеннолетних без сопровождения родителей.",
        "Номера с открытым огнём согласовываются с площадкой отдельно.",
    ], tinted=True),
    sec("Фото и видео", [
        "Артист вправе использовать фото и видео с мероприятия в своём портфолио — на сайте, в социальных сетях и в рекламных материалах — если иное не оговорено отдельно.",
        "Если вы не хотите, чтобы съёмка с вашего мероприятия публиковалась, сообщите об этом заранее: это нормальное условие, оно фиксируется письменно.",
    ]),
    sec("Контакты", [
        'Телефон: <a href="tel:+79119138374">+7 911 913-83-74</a>',
        'Почта: <a href="mailto:balashov.show.ru@gmail.com">balashov.show.ru@gmail.com</a>',
        'Обработка персональных данных описана в <a href="privacy.html">политике конфиденциальности</a>, использование cookie — в <a href="cookies.html">политике cookie</a>.',
    ], tinted=True),
])


# ── EN-версии ───────────────────────────────────────────────────────
# Собираются из Site/en/privacy.html тем же способом. Тексты не
# машинный перевод русских, а самостоятельные — короче, потому что
# англоязычная аудитория сайта это в основном зарубежные площадки и
# агентства, им нужна суть, а не разбор российского 152-ФЗ.
COOKIES_EN = "".join([
    sec("In short", [
        "This site does not use cookies to track visitors and does not share data with advertising networks. Below is what is actually stored in your browser and why.",
        "This describes the current state. If anything changes — for example, if external analytics are switched on — this page will be updated before that happens, not after.",
    ]),
    sec("What is stored now", [
        "<b>Tab memory (sessionStorage).</b> The site's own counter stores a random string so it can tell «one person opened three pages» from «three people opened one page each». It contains nothing about you, lives only while the tab is open and disappears when you close it.",
        "<b>Campaign tags.</b> If you arrived from an advertising link, the address may contain tags like <code>utm_source</code>. They are kept in the same tab memory to see which advertising brings people. These tags are part of the URL you can see in your address bar anyway.",
        "<b>No actual cookies are set at the moment</b> — neither our own nor third-party.",
    ], tinted=True),
    sec("What may be added later", [
        "Two counters are prepared in the site code but <b>not active</b>: Yandex.Metrica and the VK Ads pixel. Both, once enabled, set real cookies and send anonymised visit data to their respective services.",
        "While they are switched off, this section is informational. Before enabling them a cookie consent banner will appear on the site and this page will be extended.",
    ]),
    sec("Questions", [
        'Write to <a href="mailto:balashov.show.ru@gmail.com">balashov.show.ru@gmail.com</a> or call <a href="tel:+79119138374">+7 911 913-83-74</a>.',
        'How personal data from the enquiry and review forms is handled — see the <a href="privacy.html">privacy policy</a>.',
    ], tinted=True),
])

TERMS_EN = "".join([
    sec("About this page", [
        "This describes how the work is arranged: what the service includes, how details are agreed, how the fee is calculated and what happens if plans change. It is informational and does not replace a contract — a separate service agreement is signed when working with companies.",
        "⚠️ <b>Draft.</b> Several terms (prepayment, cancellation notice, rescheduling) are marked with blanks and need to be filled in before this page goes live.",
    ]),
    sec("What the service includes", [
        "A performance of one or more circus acts according to an agreed programme. The artiste brings his own props and costumes.",
        "The specific act, its length and the running order are agreed in advance to fit your event. Individual acts run from 6 to 12 minutes; several can be combined into a programme.",
        'Technical requirements (clear space, ceiling height, surface) depend on the act. A short summary is on the <a href="booking.html">enquiry page</a>; the full technical rider for your specific venue is sent once the format is agreed.',
    ], tinted=True),
    sec("How a booking is arranged", [
        "1. You send an enquiry: date, city and venue, event format, any wishes about the act.",
        "2. Within 1–2 days you receive suggested acts and a quote.",
        "3. The programme and technical rider are agreed.",
        "4. The date is booked. For companies a service agreement and an invoice are issued.",
    ]),
    sec("Fee", [
        "There is no fixed price list: the fee depends on the act, running time, date and city, so each quote is prepared individually.",
        "Travel outside St Petersburg and the Leningrad Region is calculated separately. For out-of-town engagements the organiser provides accommodation, meals and a room to prepare in — this is agreed in advance.",
        "Prepayment: ____ % of the fee, due ____. Final settlement — ____.",
    ], tinted=True),
    sec("Cancellation and rescheduling", [
        "If you cancel the event less than ____ days before the performance date, the prepayment ____.",
        "Rescheduling is possible ____, provided the new date is free.",
        "If the performance cannot take place for reasons beyond either party's control (weather at an open-air venue, official restrictions, the artiste's illness), the parties agree on rescheduling or a refund — the exact procedure is set out in the contract.",
    ]),
    sec("Safety and audience participation", [
        "Some acts involve the audience: climbing the flexible poles, competing on the pull-up bar, taking part in the «Transforming Tube» act. Participation is always voluntary.",
        "The artiste gives a safety briefing beforehand and does not allow participation by anyone showing signs of intoxication. The organiser provides a clear safe area and does not allow unaccompanied minors to take part.",
        "Acts involving open flame are agreed with the venue separately.",
    ], tinted=True),
    sec("Contacts", [
        'Phone: <a href="tel:+79119138374">+7 911 913-83-74</a>',
        'E-mail: <a href="mailto:balashov.show.ru@gmail.com">balashov.show.ru@gmail.com</a>',
        'Personal data handling — see the <a href="privacy.html">privacy policy</a>; cookies — see the <a href="cookies.html">cookie policy</a>.',
    ]),
])


def main():
    tpl = os.path.join(SITE, "privacy.html")

    tpl_en = os.path.join(SITE, "en", "privacy.html")

    pages = [
        (tpl, SITE, "cookies.html", "Файлы cookie", "Что сайт сохраняет в браузере и зачем", COOKIES_RU, "Site"),
        (tpl, SITE, "terms.html", "Условия работы", "Как строится работа: услуга, согласование, стоимость", TERMS_RU, "Site"),
        (tpl_en, os.path.join(SITE, "en"), "cookies.html", "Cookies", "What the site stores in your browser and why", COOKIES_EN, "Site/en"),
        (tpl_en, os.path.join(SITE, "en"), "terms.html", "Terms of work", "How the work is arranged: service, booking, fee", TERMS_EN, "Site/en"),
    ]
    for template, outdir, filename, title, tag, body, label in pages:
        html = shell(template, title, tag, body, filename)
        with open(os.path.join(outdir, filename), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK -> {label}/{filename}")


if __name__ == "__main__":
    main()
