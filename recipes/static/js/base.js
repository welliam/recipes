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

  recipes.dialog = dialog;
  recipes.closeDialog = closeDialogElements;

  $(() => {
    initDialog();
  });
})();
