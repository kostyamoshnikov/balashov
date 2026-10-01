// ШОУ БАЛАШОВА — подмена заголовков живым текстом из редактора
// (_tools/AdminPanel). Сайт статический, поэтому дефолтный текст,
// зашитый прямо в HTML, — это самостоятельная, полностью рабочая
// версия страницы. Этот скрипт — необязательное улучшение поверх неё:
// если редактор доступен и в нём что-то сохранено, подменяет текст;
// если недоступен (не задеплоен, сеть легла, эндпоинт ещё пуст) —
// молча ничего не делает, посетитель просто видит исходный текст.
// Тот же принцип честного отката, что уже применён в Site/reviews.html.
//
// Как это находит нужные элементы: на элементе стоит атрибут
// data-editable="ключ", ключ — тот же, что в списке FIELDS в
// _tools/AdminPanel/worker.js. Если ключа для этой страницы нет в
// ответе редактора (ещё не сохраняли то поле) — элемент не трогается.
(function () {
  var CONTENT_ENDPOINT = "https://balashov-admin.YOUR-SUBDOMAIN.workers.dev/content"; // TODO: заменить после деплоя (см. _tools/AdminPanel/README.md)

  // pack-v124: неразрывные пробелы в русских текстах из редактора.
  // Статический текст страниц их получает при выкладке
  // (_tools/SiteDeploy/prepare_release.py → typography.py), а текст из
  // AdminPanel приходит уже в браузере, мимо выкладки. Здесь — только
  // главное правило: короткий предлог/союз не остаётся в конце строки.
  var ru = (document.documentElement.lang || "").toLowerCase().indexOf("ru") === 0;
  var SHORT = /(^|[\s(«"])(в|к|с|о|у|и|а|я|на|по|за|от|до|из|не|ни|об|во|со|ко|но) (?=\S)/gi;
  function nbsp(t) { return t.replace(SHORT, function (m) { return m.slice(0, -1) + "\u00a0"; }).replace(SHORT, function (m) { return m.slice(0, -1) + "\u00a0"; }); }

  fetch(CONTENT_ENDPOINT)
    .then(function (r) { return r.json(); })
    .then(function (content) {
      document.querySelectorAll("[data-editable]").forEach(function (el) {
        var key = el.getAttribute("data-editable");
        var value = content[key];
        // Пустая строка — не то же самое, что «поле не задано»: если
        // кто-то в редакторе намеренно стёр текст и сохранил пусто,
        // это уважаемое решение, а не сигнал откатиться на дефолт.
        if (typeof value === "string") {
          el.textContent = ru ? nbsp(value) : value;
        }
      });
    })
    .catch(function () {
      // Редактор недоступен — молча остаёмся на статическом тексте.
      // Ни ошибки в консоль пользователю, ни визуальных последствий.
    });
})();
