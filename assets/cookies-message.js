/* Cookie notice logic extracted to keep CSP strict without inline scripts. */
(function () {
  var container = document.getElementById('cookies-message');
  if (!container || !window.localStorage) {
    return;
  }

  var hide = function () {
    container.style.display = 'none';
  };

  if (window.localStorage.getItem('cookies-accepted')) {
    hide();
    return;
  }

  var acceptButton = document.getElementById('accept-cookies');
  if (!acceptButton) {
    return;
  }

  acceptButton.addEventListener('click', function () {
    hide();
    window.localStorage.setItem('cookies-accepted', 'true');
  });
})();
