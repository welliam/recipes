(() => {
  function initializeUpdateLink() {
    recipes.initializeEditLink(
      '#edit-recipebook-form', '.edit-recipebook-link', (form, link) => {
        var title = link.parent().find('h2 a').html();
        form.find('#id_title').val(title);
        form.find('#id_description').val(link.parent().find('.recipebook-description').html());
        form.find('#edit-recipebook-title').html(title);
        form.attr('action', link.attr('data-old-href'));
      });
  }

  function initializeDeleteLink() {
    recipes.initializeEditLink(
      '#delete-recipebook-form', '.delete-recipebook-link', (form, link) => {
        var title = link.parent().find('h2 a').html();
        form.find('#delete-recipebook-title').html(title);
        form.attr('action', link.attr('data-old-href'));
      });
  }

  $(() => {
    initializeDeleteLink();
    initializeUpdateLink();
  });
})();
