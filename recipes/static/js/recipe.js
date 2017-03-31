(() => {
  function makeModal(query, label, focus) {
    var elem = $(query),
        modalButton = $('<h4><button>' + label + '</button></h4>');
    modalButton.find('button').on('click', () => {
      recipes.dialog(elem.css('display', 'block'));
      elem.find(query + ' ' + focus).focus();
    })
    elem.after(modalButton);
    elem.css('display', 'none');
  }

  function addOption(title, id) {
    var option = $('<option>' + title + '</option>')
    option.attr('value', id);
    $('#recipebook-form').find('select').append(option);
  }

  function ajaxSubmitForm(form) {
    var title = form.find('input[name="title"]').val(),
        desc = form.find('textarea[name="description"]').val(),
        csrf = form.find('input[name="csrfmiddlewaretoken"]').val();
    if (title && desc) {
      $.post(form.attr('action'), {
        title: title,
        description: desc,
        csrfmiddlewaretoken: csrf
      }, (data) => addOption(title, data.id));
    }
  }

  function initializeRecipeBookForm() {
    makeModal('.recipe-recipebooks', 'Recipe Books', 'select');
    var form = $('#new-recipebook-form');
    form.css('display', 'block');
    form.find('input[type="submit"]').on('click', (e) => {
      e.preventDefault();
      ajaxSubmitForm(form);
    });
  }

  function initializeReviewsForm() {
    makeModal('.recipe-reviews form', 'Write Review', '#id_title');
  }

  function initializeUpdateForm() {
    recipes.initializeEditLink('#edit-recipe-form', '.recipe-edit-link');
  }

  function initializeDeleteForm() {
    recipes.initializeEditLink('#delete-recipe-form', '.recipe-delete-link');
  }

  $(() => {
    initializeRecipeBookForm();
    initializeReviewsForm();
    initializeUpdateForm();
    initializeDeleteForm();
  });
})();
