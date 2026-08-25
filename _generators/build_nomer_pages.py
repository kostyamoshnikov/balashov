#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ШОУ БАЛАШОВА — генератор страниц номеров (Site/nomera/*.html,
Site/en/nomera/*.html).

До pack-v53 этих 10 файлов не было сохранённого генератора — они были
сделаны одноразовым скриптом вне пака (pack-v49), а сам скрипт никуда
не попал. Значит, поправить факт во всех 10 страницах разом можно было
только руками, по одной. Этот файл закрывает пробел — по образцу
Site/_generators/build_show_page.py пака AELITA (референс, там
аналогичный паттерн: шаблон + данные о конкретном объекте → страница),
адаптированного под масштаб Балашова (5 номеров вместо десятков
спектаклей, один язык-пара RU/EN вместо словаря переводов).

Важное отличие от простого шаблонизатора: <head> каждой страницы не
хранится как отдельный шаблон-файл, а извлекается ПРЯМО ИЗ Site/gallery.html
и Site/en/gallery.html в момент запуска (см. extract_head()) — так он
физически не может разойтись с реальным сайтом (шрифты, палитра, meta
теги и т.п. общие для всех страниц сайта живут в одном месте — gallery.html
— и растаскиваются оттуда, а не дублируются копипастой в этом скрипте).

Правка факта в номере — правка словаря ACTS/ACTS_EN ниже, затем:
    python3 build_nomer_pages.py
(запускать из Site/_generators/ — пути к Site/gallery.html и
Site/nomera/ посчитаны относительно расположения этого файла, не CWD).
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(HERE, ".."))
SITE = "https://balashov-show.ru"


def extract_head(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    idx = content.index("</head>")
    return content[:idx + len("</head>")]


# ═══════════════════════════════════════════════════════════════════
# ДАННЫЕ — RU
# ═══════════════════════════════════════════════════════════════════

ACTS = [
  {
    "slug":"lestnitsa","en_slug":"ladder","num":"01",
    "title":"Жонглёр на вольностоящей лестнице","kind":"Эквилибристика",
    "desc_meta":"Жонглёр на вольностоящей лестнице — классика и комический вариант с интерактивом. Без страховки и опоры.",
    "tag":"Только баланс артиста — без страховки и опоры",
    "photos":["lestnitsa-1.jpg","lestnitsa-2.jpg","lestnitsa-3.jpg"],
    "photo_alts":["Жонглёр на вольностоящей лестнице — выступление перед зрителями","Жонглёр на вольностоящей лестнице зимой","Жонглёр на вольностоящей лестнице, студийное фото"],
    "body":[
      "Классический вариант — чистая эквилибристика на вольностоящей лестнице без страховки и опоры, 6 минут.",
      "Комический вариант — тот же баланс, но в костюме джокера, с интерактивом и призами для зрителей, 12 минут.",
      "Формат подходит и для сцены, и для открытой площадки: свадьбы, корпоративы, городские праздники."
    ],
    "stats":[("6 мин","классика"),("12 мин","комический")],
    "rider":"Свободная площадка под вольностоящую лестницу — высота потолка/навеса от 4,5 м, ровное твёрдое покрытие."
  },
  {
    "slug":"hodulist","en_slug":"stilt-walker","num":"02",
    "title":"Ходулист","kind":"В любом образе",
    "desc_meta":"Артист на ходулях — сказочные, скоморошьи и тематические костюмы под любой праздник, живой интерактив с гостями.",
    "tag":"Сказочные, скоморошьи и тематические костюмы под любой праздник",
    "photos":[],
    "photo_alts":[],
    "body":[
      "Разные образы под тематику события: сказочные и скоморошьи костюмы, тематические персонажи — для детского праздника, свадьбы, открытия ТЦ или городского события.",
      "Живой интерактив с гостями прямо в толпе — фотографии, шутки, вовлечение зрителей любого возраста.",
      "Для номера на ходулях с элементами открытого огня требуется отдельное согласование с площадкой."
    ],
    "stats":[("∞","вариантов образа"),("дети/взрослые","формат")],
    "rider":"Высота потолка/навеса от 4,5 м. Для варианта с открытым огнём — разрешение и место, согласуется отдельно с площадкой."
  },
  {
    "slug":"truba-transformer","en_slug":"transforming-tube","num":"03",
    "title":"Труба-трансформер и Человек-пружинка","kind":"Интерактив с залом",
    "desc_meta":"Труба-трансформер — 6 разных цветов трубы, 6 минут интерактива: «съедает» и «выплёвывает» гостя вечера. Хит на свадьбах и корпоративах.",
    "tag":"6 разных цветов трубы — «съедает» и «выплёвывает» гостя вечера",
    "photos":["truba-1.jpg","truba-2.jpg","truba-3.jpg"],
    "photo_alts":["Труба-трансформер на театральной сцене","Два артиста в костюмах труба-трансформер на сцене","Человек-пружинка, серебряный костюм"],
    "body":[
      "Труба-трансформер — реквизит сшит в 6 разных цветах, номер идёт 6 минут с интерактивом: труба «съедает» и «выплёвывает» героя вечера под общий смех зала. Хит на свадьбах и корпоративах.",
      "Номер увиден у американского артиста на фестивале в Дубае и куплен там же; когда реквизит истёрся, Николай сшил новый сам — тяжёлая ручная работа.",
      "Есть и сольный вариант «Космическая фантазия» на три трубы, 8 минут, а также парный «дрессированная труба» — дрессировщица в белом и чёрная труба разыгрывают сцену противостояния.",
      "Для детской аудитории — версия «Человек-пружинка»: яркий космический пришелец, интерактивный номер для детских и городских праздников. Есть и отдельная «гибкая труба» — артист в слинге играет с детьми и «глотает» мячики."
    ],
    "stats":[("6","цветов трубы"),("6 мин","с интерактивом"),("8 мин","соло, 3 трубы")],
    "rider":"Требуется своё оборудование для труб — привозим сами. Зона безопасности вокруг номера — уточняется отдельно."
  },
  {
    "slug":"shesty","en_slug":"flexible-poles","num":"04",
    "title":"Гибкие шесты","kind":"Редкий жанр",
    "desc_meta":"Гибкие шесты — редкий жанр, всего 3–4 театра в мире. Высота 6 м, гибкость до 2,5 м, работает круглый год в помещении и на улице.",
    "tag":"Редкий жанр — всего 3–4 театра в мире исполняют его сегодня",
    "photos":["shesty-1.jpg","shesty-2.jpg","shesty-3.jpg"],
    "photo_alts":["Артисты на гибких шестах, парный номер","Гибкие шесты на фестивале","Гибкие шесты, групповой номер с ходулистами"],
    "body":[
      "Два шеста высотой 6 метров, гибкость до 2,5 м в каждую сторону, вращение вокруг оси — необычный для России аттракцион.",
      "Жанр придуман самим Николаем с партнёром за год работы, во вдохновении канадским и австралийским уличным цирком на Дворцовой площади — сегодня его исполняют всего 3–4 театра в мире.",
      "Работает круглый год, в помещении и на улице, с интерактивным шоу для гостей."
    ],
    "stats":[("6 м","высота шеста"),("2,5 м","гибкость на сторону"),("3–4","театра в мире")],
    "rider":"Требуется своё оборудование — привозим сами. Работает круглый год, в помещении и на улице."
  },
  {
    "slug":"turnik","en_slug":"pull-up-bar","num":"05",
    "title":"Турник на приз","kind":"Дополнение к номеру",
    "desc_meta":"Турник на приз — интерактив с залом: кто дольше провисит, получает приз. Добавляется к любому формату программы.",
    "tag":"Кто дольше провисит — получает приз",
    "photos":["turnik-1.jpg"],
    "photo_alts":["Турник на приз — интерактив с залом"],
    "body":[
      "Простой и азартный интерактив с залом: гости по очереди виснут на турнике, кто продержится дольше всех — получает приз.",
      "Добавляется к любому формату программы — детскому празднику, свадьбе, корпоративу или городскому событию — и работает как разогрев перед основными номерами."
    ],
    "stats":[("+", "к любому номеру")],
    "rider":"Дополнение к основному номеру — отдельных технических требований не предъявляет."
  },
]

FOOTER_RU = '''<footer>
  <div class="inner">
    <div class="badge-glow"><img src="../Brand/logo-shou-balashova.jpg" alt="Шоу Балашова"></div>
    <span class="ribbon">Booking</span>
    <h2 class="serif">Позвать Николая на площадку</h2>
    <p class="tag">Дни рождения, свадьбы, корпоративы, городские праздники — выступления по всей России.</p>
    <div class="cta-row">
      <a class="cta primary" href="mailto:balashov.show.ru@gmail.com">Написать по booking</a>
      <a class="cta ghost" href="../booking.html">Условия и заявка</a>
    </div>
    <!-- Бот Telegram — раскомментировать и вписать @username после
         деплоя _tools/BookingBot (см. README.md, раздел 5)
    <a class="cta ghost" href="https://t.me/YOUR_BOT_USERNAME">Бот в Telegram</a>
    -->
    <p class="foot-note"><a href="tel:+79119138374">+7 911 913-83-74</a></p>
    <p class="foot-note"><a href="../privacy.html">Политика конфиденциальности</a></p>
    <p class="foot-note">© Николай Балашов</p>
  </div>
</footer>

</body>
</html>
'''


def make_head_ru(head_raw, title, desc, slug, en_slug):
    h = head_raw
    h = h.replace(
        "<title>Галерея — Николай Балашов, «Шоу Балашова»</title>",
        f"<title>{title} — Николай Балашов, «Шоу Балашова»</title>"
    )
    h = h.replace(
        '<meta name="description" content="Номера Николая Балашова: жонглёр на лестнице, ходулист, труба-трансформер, гибкие шесты.">',
        f'<meta name="description" content="{desc}">'
    )
    h = h.replace(
        '<link rel="canonical" href="https://balashov-show.ru/gallery.html">',
        f'<link rel="canonical" href="{SITE}/nomera/{slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="ru" href="https://balashov-show.ru/gallery.html">',
        f'<link rel="alternate" hreflang="ru" href="{SITE}/nomera/{slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="en" href="https://balashov-show.ru/en/gallery.html">',
        f'<link rel="alternate" hreflang="en" href="{SITE}/en/nomera/{en_slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="x-default" href="https://balashov-show.ru/gallery.html">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/nomera/{slug}.html">'
    )
    h = h.replace('<meta property="og:title" content="Галерея — Николай Балашов">', f'<meta property="og:title" content="{title} — Николай Балашов">')
    h = h.replace(
        '<meta property="og:description" content="Номера: лестница, ходулист, труба-трансформер, гибкие шесты.">',
        f'<meta property="og:description" content="{desc}">'
    )
    h = h.replace('<meta property="og:url" content="https://balashov-show.ru/gallery.html">', f'<meta property="og:url" content="{SITE}/nomera/{slug}.html">')
    h = h.replace('<meta name="twitter:title" content="Галерея — Николай Балашов">', f'<meta name="twitter:title" content="{title} — Николай Балашов">')
    h = h.replace(
        '<meta name="twitter:description" content="Номера: лестница, ходулист, труба-трансформер, гибкие шесты.">',
        f'<meta name="twitter:description" content="{desc}">'
    )
    # страница на уровень глубже gallery.html -> нужен дополнительный ../
    h = h.replace('href="Brand/favicon-32.png"', 'href="../Brand/favicon-32.png"')
    h = h.replace('href="site.webmanifest"', 'href="../site.webmanifest"')
    h = h.replace('href="Brand/apple-touch-icon.png"', 'href="../Brand/apple-touch-icon.png"')
    return h


def photos_block(act):
    photos = act["photos"]
    if not photos:
        return '''<div class="g-art" style="padding:40px 0 10px">
              <svg viewBox="0 0 120 140" fill="none" style="width:130px;height:130px;margin:0 auto">
                <circle cx="60" cy="24" r="12" fill="#FBF3E4"/>
                <rect x="48" y="38" width="24" height="34" rx="8" fill="#FBF3E4"/>
                <rect x="40" y="72" width="10" height="46" rx="5" fill="#C81E1E"/>
                <rect x="70" y="72" width="10" height="46" rx="5" fill="#C81E1E"/>
                <rect x="36" y="118" width="18" height="6" rx="3" fill="#8A1210"/>
                <rect x="66" y="118" width="18" height="6" rx="3" fill="#8A1210"/>
                <circle cx="30" cy="30" r="5" fill="#FDD945"/>
                <circle cx="90" cy="30" r="5" fill="#FDD945"/>
                <circle cx="60" cy="6" r="5" fill="#FDD945"/>
              </svg>
            </div>
            <p class="note" style="margin-top:12px">Фото номера скоро появится в галерее.</p>'''
    cls = "single" if len(photos) == 1 else ""
    imgs = "\n".join(
        f'            <img src="../Photos/web/{p}" alt="{a}" loading="lazy" onclick="openLightbox({idx})">'
        for idx, (p, a) in enumerate(zip(photos, act["photo_alts"]))
    )
    return f'''<div class="g-photos {cls}" style="height:320px;border-radius:16px;overflow:hidden">
{imgs}
            </div>'''


def stats_block(act):
    items = "\n".join(
        f'      <div class="stat"><b>{v}</b><span>{label}</span></div>'
        for v, label in act["stats"]
    )
    return f'<div class="stat-row">\n{items}\n    </div>'


def prevnext(acts, i):
    n = len(acts)
    return acts[(i - 1) % n], acts[(i + 1) % n]


LIGHTBOX_CSS = '''<style>
.g-photos img{cursor:zoom-in}
.lightbox{display:none;position:fixed;inset:0;background:rgba(10,7,5,.94);z-index:999;align-items:center;justify-content:center;padding:20px}
.lightbox.active{display:flex}
.lightbox img{max-width:100%;max-height:85vh;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.6)}
.lightbox-close{position:absolute;top:18px;right:24px;font-size:34px;color:var(--cream);cursor:pointer;line-height:1;background:rgba(0,0,0,.35);width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.lightbox-close:hover{color:var(--gold)}
.lightbox-nav{position:absolute;top:50%;transform:translateY(-50%);font-size:38px;color:var(--cream);cursor:pointer;background:rgba(0,0,0,.35);width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;user-select:none}
.lightbox-nav:hover{color:var(--gold)}
.lightbox-prev{left:16px}
.lightbox-next{right:16px}
.lightbox-counter{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);font-family:'Space Mono',monospace;font-size:12px;color:var(--cream-soft);letter-spacing:.1em}
@media (max-width:600px){.lightbox-nav{width:42px;height:42px;font-size:28px}.lightbox-close{width:38px;height:38px;font-size:26px;top:10px;right:10px}}
</style>'''


def lightbox_markup(photos_urls):
    if not photos_urls:
        return ""
    urls_js = ", ".join(f'"{u}"' for u in photos_urls)
    return f'''<div class="lightbox" id="lightbox" onclick="if(event.target===this)closeLightbox()">
  <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
  <span class="lightbox-nav lightbox-prev" onclick="event.stopPropagation();navLightbox(-1)">&#8249;</span>
  <img id="lightboxImg" src="" alt="">
  <span class="lightbox-nav lightbox-next" onclick="event.stopPropagation();navLightbox(1)">&#8250;</span>
  <span class="lightbox-counter" id="lightboxCounter"></span>
</div>
<script>
const lbPhotos = [{urls_js}];
let lbIndex = 0;
function openLightbox(i) {{
  lbIndex = i;
  document.getElementById('lightboxImg').src = lbPhotos[lbIndex];
  document.getElementById('lightboxCounter').textContent = (lbIndex+1) + ' / ' + lbPhotos.length;
  document.getElementById('lightbox').classList.add('active');
  if (window.__balashovTrack) window.__balashovTrack('click', 'lightbox_open:' + (lbIndex+1));
}}
function closeLightbox() {{ document.getElementById('lightbox').classList.remove('active'); }}
function navLightbox(d) {{
  lbIndex = (lbIndex + d + lbPhotos.length) % lbPhotos.length;
  document.getElementById('lightboxImg').src = lbPhotos[lbIndex];
  document.getElementById('lightboxCounter').textContent = (lbIndex+1) + ' / ' + lbPhotos.length;
}}
document.addEventListener('keydown', function(e) {{
  if (!document.getElementById('lightbox').classList.contains('active')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') navLightbox(-1);
  if (e.key === 'ArrowRight') navLightbox(1);
}});
</script>'''


STATS_SNIPPET_RU = '<script src="../analytics.js" defer></script>\n<script src="../vk-pixel.js" defer></script>\n</body>'
STATS_SNIPPET_EN = '<script src="../../analytics.js" defer></script>\n<script src="../../vk-pixel.js" defer></script>\n</body>'


def build_ru(head_raw, i, act):
    prev_act, next_act = prevnext(ACTS, i)
    head = make_head_ru(head_raw, act["title"], act["desc_meta"], act["slug"], act["en_slug"])
    head = head.replace("</head>", LIGHTBOX_CSS + "\n</head>")
    nav = f'''<nav class="site-nav">
  <a href="../index.html">Главная</a>
  <a href="../about.html">О нём</a>
  <a href="../gallery.html">Галерея</a>
  <a href="../media.html">Медиа</a>
  <a href="../reviews.html">Отзывы</a>
    <a href="../booking.html">Booking</a>
  <a href="../en/nomera/{act["en_slug"]}.html" class="lang-switch">EN</a>
</nav>'''

    body_paras = "\n".join(f'      <p>{p}</p>' for p in act["body"])

    return f'''{head}
<body>

{nav}

<div class="page-hero">
  <div class="badge-glow"><img src="../Brand/logo-shou-balashova.jpg" alt="Шоу Балашова"></div>
  <p class="mono" style="color:var(--gold);letter-spacing:.2em;font-size:11px;margin-bottom:6px">НОМЕР {act["num"]} · {act["kind"].upper()}</p>
  <h1>{act["title"]}</h1>
  <p class="tag">{act["tag"]}</p>
</div>

<div class="marquee"></div>

<section>
  <div class="wrap">
    <div class="g-card" style="margin-bottom:28px">
{photos_block(act)}
    </div>

    {stats_block(act)}

    <div class="body-copy">
{body_paras}
    </div>

    <div class="note" style="margin-top:26px;text-align:left">
      <b style="color:var(--cream);display:block;margin-bottom:6px;font-family:'Public Sans'">Технический райдер · кратко</b>
      {act["rider"]}
    </div>

    <div class="cta-row" style="margin-top:26px">
      <a class="cta primary" href="../booking.html">Заказать номер</a>
      <a class="cta ghost" href="../gallery.html">Все номера</a>
    </div>
  </div>
</section>

<div class="marquee"></div>

<section class="tinted">
  <div class="wrap">
    <div class="section-head">
      <span class="ribbon">Другие номера</span>
    </div>
    <div class="acts" style="flex-direction:row;flex-wrap:wrap">
      <a href="{prev_act["slug"]}.html" style="text-decoration:none;flex:1 1 45%">
        <div class="act c2">
          <div class="num">{prev_act["num"]}</div>
          <p class="kind">← Предыдущий</p>
          <h3>{prev_act["title"]}</h3>
        </div>
      </a>
      <a href="{next_act["slug"]}.html" style="text-decoration:none;flex:1 1 45%">
        <div class="act c3">
          <div class="num">{next_act["num"]}</div>
          <p class="kind">Следующий →</p>
          <h3>{next_act["title"]}</h3>
        </div>
      </a>
    </div>
  </div>
</section>

{lightbox_markup([f"../Photos/web/{p}" for p in act["photos"]])}

{FOOTER_RU}'''


# ═══════════════════════════════════════════════════════════════════
# ДАННЫЕ — EN
# ═══════════════════════════════════════════════════════════════════

ACTS_EN = [
  {
    "slug":"ladder","ru_slug":"lestnitsa","num":"01",
    "title":"Juggler on a free-standing ladder","kind":"Equilibristics",
    "desc_meta":"Juggler on a free-standing ladder — a classic act and a comic version with audience interaction. No safety rig, no support.",
    "tag":"Just the artiste's own balance — no safety rig, no support",
    "photos":["lestnitsa-1.jpg","lestnitsa-2.jpg","lestnitsa-3.jpg"],
    "photo_alts":["Juggler on a free-standing ladder performing for an audience","Juggler on a free-standing ladder in winter","Juggler on a free-standing ladder, studio photo"],
    "body":[
      "The classic version — pure equilibristics on a free-standing ladder, no safety rig, no support, 6 minutes.",
      "The comic version — the same balance act, but in a jester's costume, with audience interaction and prizes, 12 minutes.",
      "Works both on stage and outdoors: weddings, corporate events, city festivals."
    ],
    "stats":[("6 min","classic"),("12 min","comic")],
    "rider":"Free space for a free-standing ladder — ceiling/canopy height from 4.5 m, flat firm surface."
  },
  {
    "slug":"stilt-walker","ru_slug":"hodulist","num":"02",
    "title":"Stilt-walker","kind":"Any character",
    "desc_meta":"Stilt-walker — fairy-tale, jester and themed costumes for any event, with live audience interaction.",
    "tag":"Fairy-tale, jester and themed costumes for any event",
    "photos":[],
    "photo_alts":[],
    "body":[
      "Different characters to match the event: fairy-tale and jester costumes, themed personas — for a children's party, wedding, mall opening or city event.",
      "Live interaction with guests right in the crowd — photos, jokes, engagement for all ages.",
      "For the fire-element version of the stilt act, a separate approval with the venue is required."
    ],
    "stats":[("many","costume options"),("kids/adults","format")],
    "rider":"Ceiling/canopy height from 4.5 m. For the fire-element version — a permit and space, arranged separately with the venue."
  },
  {
    "slug":"transforming-tube","ru_slug":"truba-transformer","num":"03",
    "title":"Transforming Tube and Spring-man","kind":"Crowd interaction",
    "desc_meta":"Transforming Tube — 6 different colours of tube, 6 minutes of interaction: it \u201cswallows\u201d and \u201cspits out\u201d the guest of honour. A hit at weddings and corporate events.",
    "tag":"6 different colours of tube — \u201cswallows\u201d and \u201cspits out\u201d the guest of honour",
    "photos":["truba-1.jpg","truba-2.jpg","truba-3.jpg"],
    "photo_alts":["Transforming Tube on a theatre stage","Two artistes in Transforming Tube costumes on stage","Spring-man, silver costume"],
    "body":[
      "The Transforming Tube — the prop is made in 6 different colours, the act runs 6 minutes with interaction: the tube \"swallows\" and \"spits out\" the guest of honour to general laughter. A hit at weddings and corporate events.",
      "Nikolai first saw the act performed by an American artiste at a festival in Dubai and bought it there; when the prop wore out, he sewed a new one himself — heavy manual work.",
      "There's also a solo version, \"Cosmic Fantasy\", using three tubes over 8 minutes, and a paired version, \"the trained tube\", where a dompteuse in white and a black tube act out a scene of confrontation.",
      "For younger audiences there's the \"Spring-man\" version: a bright cosmic alien, an interactive act for children's and city events. There's also a separate \"flexible tube\" act — the artiste in a sling plays with children and \"swallows\" balls."
    ],
    "stats":[("6","tube colours"),("6 min","with interaction"),("8 min","solo, 3 tubes")],
    "rider":"Requires its own equipment for the tubes — we bring it ourselves. Safety zone around the act — confirmed separately."
  },
  {
    "slug":"flexible-poles","ru_slug":"shesty","num":"04",
    "title":"Flexible poles","kind":"Rare genre",
    "desc_meta":"Flexible poles — a rare genre, performed by only 3–4 theatres worldwide. 6 m tall, bends up to 2.5 m, works year-round indoors and outdoors.",
    "tag":"A rare genre — performed by only 3–4 theatres worldwide today",
    "photos":["shesty-1.jpg","shesty-2.jpg","shesty-3.jpg"],
    "photo_alts":["Artistes on flexible poles, a paired act","Flexible poles at a festival","Flexible poles, a group act with stilt-walkers"],
    "body":[
      "Two 6-metre poles, bending up to 2.5 m to each side, rotating on their axis — an act rarely seen in Russia.",
      "The genre was devised by Nikolai and a partner over a year of work, inspired by Canadian and Australian street circus on Palace Square — today only 3–4 theatres in the world perform it.",
      "Works year-round, indoors and outdoors, with interactive audience moments."
    ],
    "stats":[("6 m","pole height"),("2.5 m","bend per side"),("3–4","theatres worldwide")],
    "rider":"Requires its own equipment — we bring it ourselves. Works year-round, indoors and outdoors."
  },
  {
    "slug":"pull-up-bar","ru_slug":"turnik","num":"05",
    "title":"Pull-up bar for a prize","kind":"Add-on to any act",
    "desc_meta":"Pull-up bar for a prize — crowd interaction: whoever hangs on longest wins a prize. Can be added to any programme format.",
    "tag":"Whoever hangs on longest wins the prize",
    "photos":["turnik-1.jpg"],
    "photo_alts":["Pull-up bar for a prize — crowd interaction"],
    "body":[
      "A simple, exciting bit of crowd interaction: guests take turns hanging from the bar, and whoever lasts the longest wins a prize.",
      "Can be added to any programme format — a children's party, wedding, corporate event or city festival — and works well as a warm-up before the main acts."
    ],
    "stats":[("+", "to any act")],
    "rider":"An add-on to a main act — no separate technical requirements."
  },
]

FOOTER_EN = '''<footer>
  <div class="inner">
    <div class="badge-glow"><img src="../../Brand/logo-shou-balashova.jpg" alt="Shou Balashova"></div>
    <span class="ribbon">Booking</span>
    <h2 class="serif">Book Nikolai for your event</h2>
    <p class="tag">Birthdays, weddings, corporate events, city festivals — performing across Russia.</p>
    <div class="cta-row">
      <a class="cta primary" href="mailto:balashov.show.ru@gmail.com">Email booking</a>
      <a class="cta ghost" href="../booking.html">Terms and request form</a>
    </div>
    <!-- Telegram bot — uncomment and fill in @username after
         deploying _tools/BookingBot (see README.md, section 5)
    <a class="cta ghost" href="https://t.me/YOUR_BOT_USERNAME">Telegram bot</a>
    -->
    <p class="foot-note"><a href="tel:+79119138374">+7 911 913-83-74</a></p>
    <p class="foot-note"><a href="../privacy.html">Privacy policy</a></p>
    <p class="foot-note">© Nikolai Balashov</p>
  </div>
</footer>

</body>
</html>
'''


def make_head_en(head_raw, title, desc, slug, ru_slug):
    h = head_raw
    h = h.replace(
        '<title>Gallery — Nikolai Balashov, "Shou Balashova"</title>',
        f'<title>{title} — Nikolai Balashov, "Shou Balashova"</title>'
    )
    h = h.replace(
        '<meta name="description" content="Nikolai Balashov\'s acts: ladder juggling, stilts, the transforming tube, flexible poles.">',
        f'<meta name="description" content="{desc}">'
    )
    h = h.replace(
        '<link rel="canonical" href="https://balashov-show.ru/en/gallery.html">',
        f'<link rel="canonical" href="{SITE}/en/nomera/{slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="ru" href="https://balashov-show.ru/gallery.html">',
        f'<link rel="alternate" hreflang="ru" href="{SITE}/nomera/{ru_slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="en" href="https://balashov-show.ru/en/gallery.html">',
        f'<link rel="alternate" hreflang="en" href="{SITE}/en/nomera/{slug}.html">'
    )
    h = h.replace(
        '<link rel="alternate" hreflang="x-default" href="https://balashov-show.ru/gallery.html">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/nomera/{ru_slug}.html">'
    )
    h = h.replace('<meta property="og:title" content="Gallery — Nikolai Balashov">', f'<meta property="og:title" content="{title} — Nikolai Balashov">')
    h = h.replace(
        '<meta property="og:description" content="Acts: ladder, stilt-walker, transforming tube, flexible poles.">',
        f'<meta property="og:description" content="{desc}">'
    )
    h = h.replace('<meta property="og:url" content="https://balashov-show.ru/en/gallery.html">', f'<meta property="og:url" content="{SITE}/en/nomera/{slug}.html">')
    h = h.replace('<meta name="twitter:title" content="Gallery — Nikolai Balashov">', f'<meta name="twitter:title" content="{title} — Nikolai Balashov">')
    h = h.replace(
        '<meta name="twitter:description" content="Acts: ladder, stilt-walker, transforming tube, flexible poles.">',
        f'<meta name="twitter:description" content="{desc}">'
    )
    # en/gallery.html уже на 1 уровень глубже (Site/en/), наша страница на 2 -> ещё один ../
    h = h.replace('href="../Brand/', 'href="../../Brand/')
    h = h.replace('href="../site.webmanifest"', 'href="../../site.webmanifest"')
    return h


def photos_block_en(act):
    photos = act["photos"]
    if not photos:
        return '''<div class="g-art" style="padding:40px 0 10px">
              <svg viewBox="0 0 120 140" fill="none" style="width:130px;height:130px;margin:0 auto">
                <circle cx="60" cy="24" r="12" fill="#FBF3E4"/>
                <rect x="48" y="38" width="24" height="34" rx="8" fill="#FBF3E4"/>
                <rect x="40" y="72" width="10" height="46" rx="5" fill="#C81E1E"/>
                <rect x="70" y="72" width="10" height="46" rx="5" fill="#C81E1E"/>
                <rect x="36" y="118" width="18" height="6" rx="3" fill="#8A1210"/>
                <rect x="66" y="118" width="18" height="6" rx="3" fill="#8A1210"/>
                <circle cx="30" cy="30" r="5" fill="#FDD945"/>
                <circle cx="90" cy="30" r="5" fill="#FDD945"/>
                <circle cx="60" cy="6" r="5" fill="#FDD945"/>
              </svg>
            </div>
            <p class="note" style="margin-top:12px">Photo of this act coming soon to the gallery.</p>'''
    cls = "single" if len(photos) == 1 else ""
    imgs = "\n".join(
        f'            <img src="../../Photos/web/{p}" alt="{a}" loading="lazy" onclick="openLightbox({idx})">'
        for idx, (p, a) in enumerate(zip(photos, act["photo_alts"]))
    )
    return f'''<div class="g-photos {cls}" style="height:320px;border-radius:16px;overflow:hidden">
{imgs}
            </div>'''


def stats_block_en(act):
    items = "\n".join(
        f'      <div class="stat"><b>{v}</b><span>{label}</span></div>'
        for v, label in act["stats"]
    )
    return f'<div class="stat-row">\n{items}\n    </div>'


def build_en(head_raw, i, act):
    prev_act, next_act = prevnext(ACTS_EN, i)
    head = make_head_en(head_raw, act["title"], act["desc_meta"], act["slug"], act["ru_slug"])
    head = head.replace("</head>", LIGHTBOX_CSS + "\n</head>")
    nav = f'''<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="../about.html">About</a>
  <a href="../gallery.html">Gallery</a>
  <a href="../media.html">Media</a>
  <a href="../reviews.html">Reviews</a>
    <a href="../booking.html">Booking</a>
  <a href="../../nomera/{act["ru_slug"]}.html" class="lang-switch">RU</a>
</nav>'''
    body_paras = "\n".join(f'      <p>{p}</p>' for p in act["body"])

    return f'''{head}
<body>

{nav}

<div class="page-hero">
  <div class="badge-glow"><img src="../../Brand/logo-shou-balashova.jpg" alt="Shou Balashova"></div>
  <p class="mono" style="color:var(--gold);letter-spacing:.2em;font-size:11px;margin-bottom:6px">ACT {act["num"]} · {act["kind"].upper()}</p>
  <h1>{act["title"]}</h1>
  <p class="tag">{act["tag"]}</p>
</div>

<div class="marquee"></div>

<section>
  <div class="wrap">
    <div class="g-card" style="margin-bottom:28px">
{photos_block_en(act)}
    </div>

    {stats_block_en(act)}

    <div class="body-copy">
{body_paras}
    </div>

    <div class="note" style="margin-top:26px;text-align:left">
      <b style="color:var(--cream);display:block;margin-bottom:6px;font-family:'Public Sans'">Technical rider · brief</b>
      {act["rider"]}
    </div>

    <div class="cta-row" style="margin-top:26px">
      <a class="cta primary" href="../booking.html">Book this act</a>
      <a class="cta ghost" href="../gallery.html">All acts</a>
    </div>
  </div>
</section>

<div class="marquee"></div>

<section class="tinted">
  <div class="wrap">
    <div class="section-head">
      <span class="ribbon">Other acts</span>
    </div>
    <div class="acts" style="flex-direction:row;flex-wrap:wrap">
      <a href="{prev_act["slug"]}.html" style="text-decoration:none;flex:1 1 45%">
        <div class="act c2">
          <div class="num">{prev_act["num"]}</div>
          <p class="kind">← Previous</p>
          <h3>{prev_act["title"]}</h3>
        </div>
      </a>
      <a href="{next_act["slug"]}.html" style="text-decoration:none;flex:1 1 45%">
        <div class="act c3">
          <div class="num">{next_act["num"]}</div>
          <p class="kind">Next →</p>
          <h3>{next_act["title"]}</h3>
        </div>
      </a>
    </div>
  </div>
</section>

{lightbox_markup([f"../../Photos/web/{p}" for p in act["photos"]])}

{FOOTER_EN}'''


def main():
    head_ru_raw = extract_head(os.path.join(SITE_DIR, "gallery.html"))
    head_en_raw = extract_head(os.path.join(SITE_DIR, "en", "gallery.html"))

    outdir_ru = os.path.join(SITE_DIR, "nomera")
    os.makedirs(outdir_ru, exist_ok=True)
    for i, act in enumerate(ACTS):
        html = build_ru(head_ru_raw, i, act)
        html = html.replace("</body>", STATS_SNIPPET_RU, 1)
        with open(os.path.join(outdir_ru, f'{act["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", "nomera/" + act["slug"] + ".html")

    outdir_en = os.path.join(SITE_DIR, "en", "nomera")
    os.makedirs(outdir_en, exist_ok=True)
    for i, act in enumerate(ACTS_EN):
        html = build_en(head_en_raw, i, act)
        html = html.replace("</body>", STATS_SNIPPET_EN, 1)
        with open(os.path.join(outdir_en, f'{act["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", "en/nomera/" + act["slug"] + ".html")


if __name__ == "__main__":
    main()
