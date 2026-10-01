/*
 * Меню на телефоне — pack-v123 (ТЗ, задача 6). Пара — Site/site-mobile.css.
 *
 * Подключается СРАЗУ ПОСЛЕ </nav> и без defer: скрипт крошечный, а так
 * меню сворачивается до первой отрисовки — без мигания раскрытого списка.
 * Без JS (или если скрипт не загрузился) меню остаётся раскрытым, как до
 * pack-v123: свёрнутое состояние включается только классом .js на <html>.
 */
(function () {
  var nav = document.querySelector('.site-nav');
  if (!nav || nav.querySelector('.nav-toggle')) return;
  document.documentElement.classList.add('js');
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  if (!nav.id) nav.id = 'site-nav';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'nav-toggle';
  btn.setAttribute('aria-controls', nav.id);
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = '<span class="nav-toggle-icon" aria-hidden="true"></span><span>' + (en ? 'Menu' : 'Меню') + '</span>';
  nav.insertBefore(btn, nav.firstChild);
  function setOpen(open) {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); btn.focus(); }
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a')) setOpen(false);
  });
})();
