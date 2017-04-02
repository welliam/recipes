(() => {
  function initializeDeleteLink() {
    recipes.initializeEditLink(
      '#delete-review-form', '.delete-review-link', (form, link) => {
        var title = link.parent().parent().find('h4').html();
        form.find('#delete-review-title').html(title);
        form.attr('action', link.attr('data-old-href'));
      });
  }

  $(function() {
    initializeDeleteLink();
  });
})();
