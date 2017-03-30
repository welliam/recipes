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
  }

  function initializeReviewsForm() {
    makeModal('.recipe-reviews form', 'Write Review', '#id_title');
  }

  $(() => {
    initializeRecipeBookForm();
    initializeReviewsForm()
  });
})();
