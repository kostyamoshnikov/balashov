// ШОУ БАЛАШОВА — пиксель VK Рекламы (заготовка, по умолчанию НЕ АКТИВЕН).
//
// Та же техническая основа, что и счётчик top.mail.ru: после перехода
// на новый рекламный кабинет VK Реклама (28 января 2026 года) старый
// VK.Retargeting.Init/JS API ретаргетинга больше не работает — пиксель
// нового кабинета выдаётся именно в виде кода top.mail.ru, id пикселя
// = id счётчика top.mail.ru. Перенесено по образцу пака AELITA
// (референс, Site/assets/main.js) — тот же код, адаптирован под то,
// что у Балашова один файл на одну задачу (см. Site/analytics.js —
// та же схема), не общий файл виджетов на весь сайт.
//
// ЗАПОЛНИТЬ после создания пикселя в кабинете ads.vk.com (раздел
// «Сайты» → «Добавить пиксель»). Пока VK_PIXEL_ID = 0 — пиксель
// намеренно не грузится вообще (см. loadVkPixel ниже): пустой ID
// давал бы нерабочую заглушку, которая выглядит как готовность, но
// ничего не отслеживает — честнее совсем не грузить счётчик, чем
// грузить нерабочий.
//
// ⚠️ ВАЖНО перед заполнением реального ID — то, чего здесь СОЗНАТЕЛЬНО
// нет: gating согласием на cookies. У AELITA пиксель грузится только
// после явного принятия cookie-баннера (localStorage
// 'cookies_accepted') — у сайта Балашова такого баннера пока нет
// вообще (ни для этого пикселя, ни для уже присутствующей на сайте
// закомментированной Яндекс.Метрики, у которой та же ситуация — см.
// Site/index.html, комментарий над её кодом). Это существующая на
// сайте практика, не новая, но при активации VK-пикселя стоит либо:
//   (а) синхронно завести общий cookie-баннер для обоих счётчиков
//       (Метрика + этот пиксель) — правильное решение по духу
//       Site/privacy.html, но отдельная, более крупная задача, или
//   (б) как минимум явно описать оба счётчика в Site/privacy.html
//       (сейчас там про них ничего нет, ни про Метрику, ни про этот
//       пиксель — пока оба неактивны, описывать нечего).
// Не делать активацию тихо — privacy.html должна остаться правдой.
var VK_PIXEL_ID = 0;
var vkPixelLoaded = false;

function loadVkPixel() {
  if (vkPixelLoaded) return;
  if (!VK_PIXEL_ID) return; // id ещё не заполнен — см. комментарий выше
  vkPixelLoaded = true;
  var _tmr = window._tmr = window._tmr || [];
  _tmr.push({ id: VK_PIXEL_ID, type: "pageView", start: (new Date()).getTime() });
  (function (d, w, id) {
    if (d.getElementById(id)) return;
    var ts = d.createElement("script"); ts.type = "text/javascript"; ts.async = true; ts.id = id;
    ts.src = "https://top-fwz1.mail.ru/js/code.js";
    var f = function () { var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ts, s); };
    if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); }
  })(document, window, "topmailru-code");
}

loadVkPixel(); // пока VK_PIXEL_ID = 0 — эта строка ничего не делает
