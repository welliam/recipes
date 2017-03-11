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

    def testPostRecipe(self):
        """Posts a recipe using the create view."""
        response = self.client.post(reverse('create_recipe'), self.data)
        self.assertEquals(response.status_code, 302)
