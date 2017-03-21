from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from . import views


RECIPE_FIELDS = ['title', 'description', 'ingredients', 'directions']


class RecipeDetailTestCase(TestCase):
    """Test viewing a recipe."""

    def setUp(self):
        """Initialize a recipe to be tested."""
        user = User(username='lydia')
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
        user = User(username='lydia')
        user.save()
        self.client.force_login(user)
        self.data = dict(
            title='test recipe',
            description='this is a test recipe',
            ingredients='food',
            directions='make it'
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
        for name in RECIPE_FIELDS:
            self.assertContains(self.get, 'name="{}"'.format(name))

    def testPostCreateRecipeRedirects(self):
        """Posts a recipe using the create view."""
        self.assertEquals(self.post.status_code, 302)

    def testPostCreateRecipe(self):
        """Posts a recipe using the create view."""
        count = Recipe.objects.count()
        self.client.post(reverse('new_recipe'), self.data)
        self.assertEquals(Recipe.objects.count(), count + 1)

    def testCreateRecipeWithoutFieldDoesNothing(self):
        """Test POSTing a recipe without fields doesn't update DB."""
        count = Recipe.objects.count()
        for field in RECIPE_FIELDS:
            data = self.data.copy()
            del data[field]
            self.client.post(reverse('new_recipe'), data)
            self.assertEquals(Recipe.objects.count(), count)


class ViewLogicTests(TestCase):
    """Test helper functions behind view."""

    def testStructureDirections(self):
        structured = list(views.structureDirections("""Season
        Mix cubed tofu with lime juice, turmeric, salt, and black pepper.

        Fry
        Combine tofu and chopped onions in frying pan.

        Simmer
        Bring tofu, onions, coconut milk, and curry paste to simmer.
        """))
        self.assertEquals(structured[0]['summary'], 'Season')
        self.assertEquals(structured[1]['summary'], 'Fry')
        self.assertEquals(
            structured[1]['details'],
            'Combine tofu and chopped onions in frying pan.'
        )
        self.assertEquals(structured[2]['summary'], 'Simmer')


class SearchViewTests(TestCase):
    """Test search functionality."""

    def setUp(self):
        """Insert some recipes into the db"""
        self.title = 'good recipe'
        user = User(username="friend")
        user.save()
        Recipe(
            user=user,
            title=self.title,
            description='test',
            ingredients='test',
            directions='test'
        ).save()
        Recipe(
            user=user,
            title='bad recipe',
            description='test',
            ingredients='test',
            directions='test'
        ).save()
        self.response = self.client.get(reverse('recipe_search') + '?q=good')

    def testSearchForGoodRecipe(self):
        self.assertContains(self.response, self.title)

    def testSearchForGoodRecipeRetainsSearch(self):
        """Test that search bar contains query."""
        self.assertContains(self.response, 'value="good"')


class EditViewTests(TestCase):
    """Test editing recipes."""

    def setUp(self):
        """Create recipe to be edited."""
        self.user = User(username="friend")
        self.user.save()
        self.recipe = Recipe(
            user=self.user,
            title='test',
            description='test',
            ingredients='test',
            directions='test'
        )
        self.recipe.save()
        self.client.force_login(self.user)

    def editRecipeTitle(self, to):
        """Edit posted recipe's title using self.client."""
        data = dict(
            title=to,
            description='test',
            ingredients='test',
            directions='test'
        )
        url = reverse('edit_recipe', args=[self.recipe.id])
        self.client.post(url, data)

    def testEditTitle(self):
        """Test editing title."""
        new_title = 'new title'
        self.editRecipeTitle(new_title)
        recipe = Recipe.objects.filter(id=self.recipe.id).first()
        self.assertEqual(recipe.title, new_title)

    def testEditingRecipeMaintainsCount(self):
        """Test editing title."""
        new_title = 'new title'
        count = Recipe.objects.count()
        self.editRecipeTitle(new_title)
        self.assertEqual(count, Recipe.objects.count())

    def testWrongUserCannotEdit(self):
        """Test that a user who does not own a recipe cannot edit it."""
        evil_user = User(username="evil")
        evil_user.save()
        self.client.force_login(evil_user)
        self.editRecipeTitle('bad')
        recipe = Recipe.objects.filter(id=self.recipe.id).first()
        self.assertEqual(recipe.title, self.recipe.title)
