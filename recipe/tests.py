from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe


class RecipeDetailTestCase(TestCase):
    """Test viewing a recipe."""

    def setUp(self):
        """Initialize a recipe to be tested."""
        user = User()
        user.save()
        self.recipe = Recipe(
            user=user,
            title="test recipe",
            description="this is a test recipe",
            ingredients="food",
            directions="make it"
        )
        self.recipe.save()
        self.response = self.client.get(
            reverse('view_recipe', args=[self.recipe.id])
        )

    def testRecipeShowsTitle(self):
        """Test response has title."""
        self.assertContains(self.response, self.recipe.title)

    def testRecipeShowsDescription(self):
        """Test response has description."""
        self.assertContains(self.response, self.recipe.description)

    def testRecipeShowsIngredients(self):
        """Test response has ingredients."""
        self.assertContains(self.response, self.recipe.ingredients)

    def testRecipeShowsDirections(self):
        """Test response has directions."""
        self.assertContains(self.response, self.recipe.directions)


class RecipeCreateTestCase(TestCase):
    """Test creating a recipe."""

    def setUp(self):
        user = User()
        user.save()
        self.client.force_login(user)
        self.data = dict(
            title="test recipe",
            description="this is a test recipe",
            ingredients="food",
            directions="make it"
        )
        self.get = self.client.get(reverse('new_recipe'))
        self.post = self.client.post(reverse('new_recipe'), self.data)

    def testGetCreateRecipe(self):
        """Get the create recipe page."""
        self.assertEquals(self.get.status_code, 200)

    def testGetCreateRecipeHasForm(self):
        """Test the create recipe page has a form."""
        self.assertContains(self.get, '</form>')

    def testFormMethodPost(self):
        """Test the create recipe page has a form with method=POST."""
        self.assertContains(self.get, 'method="POST"')

    def testFormHasInputs(self):
        """Test the create recipe page has a form with method=POST."""
        for name in ['title', 'description', 'ingredients', 'directions']:
            self.assertContains(self.get, 'name="{}"'.format(name))

    def testPostCreateRecipeRedirects(self):
        """Posts a recipe using the create view."""
        self.assertEquals(self.post.status_code, 302)

    def testPostCreateRecipe(self):
        """Posts a recipe using the create view."""
        count = Recipe.objects.count()
        self.client.post(reverse('new_recipe'), self.data)
        self.assertEquals(Recipe.objects.count(), count + 1)
