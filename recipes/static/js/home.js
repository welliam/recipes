(() => {
  function initializeNewRecipeForm() {
    recipes.initializeEditLink('#create-recipe-form', '.new-recipe-link');
  }

  $(() => {
    initializeNewRecipeForm();
  });
})();
