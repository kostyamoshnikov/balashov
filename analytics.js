// ШОУ БАЛАШОВА — собственная статистика сайта (клиентская часть).
// Подключается одним <script src> на каждой странице вместо
// дублирования инлайн-сниппета по всем файлам (было так до pack-v69,
// правка требовала находить и менять 24 копии одного и того же кода).
//
// Адаптировано по духу из _tools/Analytics/Site/assets/
// analytics-events.js пака AELITA (референс) — батчинг событий и
// sendBeacon перенесены, полная модель событий Аэлиты (десятки
// категорий кликов под их сайт) не переносилась — незачем при
// масштабе Балашова, здесь только то, что реально нужно.
//
// ⚠️ ЗАПОЛНИТЬ после деплоя _tools/StatsBot/worker.js — см.
// _tools/StatsBot/README.md. Пока пусто — событие копится в памяти
// и тихо теряется при уходе со страницы, ошибок нет, сайт не ломается.
(function () {
  var STATS_ENDPOINT = "https://balashov-stats.YOUR-SUBDOMAIN.workers.dev"; // TODO: заменить после деплоя

  // Session ID — случайная строка в sessionStorage, НЕ localStorage:
  // сбрасывается сама, когда закрывается вкладка/браузер. Не переживает
  // между визитами, не связывает разные дни или устройства одного
  // человека — только группирует события ОДНОГО открытого визита
  // (например: "зашёл на страницу труба-трансформер, потом открыл
  // фото в лайтбоксе, потом ушёл в booking" — это один session, а не
  // три разных посетителя). Site/privacy.html описывает это точно
  // такими словами — при изменении логики здесь обнови и текст там.
  function sessionId() {
    try {
      var id = sessionStorage.getItem("balashov_sid");
      if (!id) {
        id = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
        sessionStorage.setItem("balashov_sid", id);
      }
      return id;
    } catch (e) {
      return "";
    }
  }

  function deviceType() {
    return window.innerWidth < 768 ? "mobile" : "desktop";
  }

  function pageLang() {
    return document.documentElement.lang === "en" ? "en" : "ru";
  }

  function refHost() {
    if (!document.referrer) return "";
    try {
      return new URL(document.referrer).hostname;
    } catch (e) {
      return "";
    }
  }

  var buffer = [];
  var flushTimer = null;

  function track(type, detail) {
    buffer.push({
      type: type, // "pageview" | "click"
      page: location.pathname,
      detail: detail || "",
      referrer: refHost(),
      device: deviceType(),
      lang: pageLang(),
      session: sessionId(),
    });
    if (!flushTimer) {
      flushTimer = setTimeout(function () { flush(false); }, 8000);
    }
  }

  function flush(useBeacon) {
    if (flushTimer) { clearTimeout(flushTimer); flushTimer = null; }
    if (!buffer.length) return;
    var payload = JSON.stringify({ events: buffer });
    buffer = [];
    try {
      if (useBeacon && navigator.sendBeacon) {
        navigator.sendBeacon(STATS_ENDPOINT, new Blob([payload], { type: "application/json" }));
        return;
      }
      fetch(STATS_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        keepalive: true,
      }).catch(function () {});
    } catch (e) {}
  }

  // sendBeacon переживает закрытие вкладки — обычный fetch может не
  // успеть отправиться, если вкладка закрывается прямо во время запроса.
  document.addEventListener("pagehide", function () { flush(true); });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") flush(true);
  });

  track("pageview");

  // Клики — по data-track атрибуту (явно расставлен на ключевых CTA:
  // booking-кнопки, карточки номеров) плюс отдельный вызов из лайтбокса
  // страниц номеров (см. window.__balashovTrack ниже, вызывается из
  // openLightbox() в Site/_generators/build_nomer_pages.py).
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (el) track("click", el.getAttribute("data-track"));
  });

  window.__balashovTrack = track;
})();
