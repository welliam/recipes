recipes = {};

(() => {
  DIALOG_ELEMENTS = ['#dialog-background', '#dialog']

  function closeDialogElements() {
    DIALOG_ELEMENTS.forEach(e => $(e).css('display', 'none'));
  }

  function dialog(elem) {
    $('#dialog').html(elem);
    DIALOG_ELEMENTS.forEach(e => $(e).css('display', 'block'));
  }

  function initDialog() {
    $('#dialog-background').on('click', closeDialogElements)
    $(window).on('keypress', function (e) {
      if (e.keyCode == 27) {  // escape
        closeDialogElements();
      }
    });
  }

  function initializeEditLink(formQuery, linkQuery, f) {
    var form = $(formQuery);
    $(linkQuery).each(function (i) {
      var link = $(this);
      link.on('click', () => {
        f && f(form, link);
        recipes.dialog(form);
      });
      link.attr('data-old-href', link.attr('href'));
      link.attr('href', '#');
    });
  }

  function checkNotifications() {
    $.get('/notifications/count', (data) => {
      var n = data['count']
      $('.notifications-count').html(n ? ' (' + n + ')' : '');
    });
  }

  function initNotificationsCheck() {
    checkNotifications();
    setInterval(checkNotifications, 5000);
  }

  recipes.dialog = dialog;
  recipes.closeDialog = closeDialogElements;
  recipes.initializeEditLink = initializeEditLink;

  $(() => {
    initDialog();
    initNotificationsCheck();
  });
})();

