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

  function initializeRecipeBookForm() {
    makeModal('.recipe-recipebooks', 'Recipe Books', 'select');
    $('#new-recipebook-form').css('display', 'block');
  }

  function initializeReviewsForm() {
    makeModal('.recipe-reviews form', 'Write Review', '#id_title');
  }

  function initializeRecipeEditForm(formQuery, linkQuery) {
    var form = $(formQuery),
        link = $(linkQuery);
    link.on('click', () => recipes.dialog(form));
    link.attr('href', '#');
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
