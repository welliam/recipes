from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipe.models import Recipe


class HomePageTests(TestCase):
    """Tests for home page."""

    def setUp(self):
        """Initialize a response to be tested."""
        user = User(username='testuser')
        user.save()
        for i in range(10):
            Recipe(
                user=user,
                title='title {}'.format(i),
                description='desc',
                ingredients='ing',
                directions='dir'
            ).save()
        self.response = self.client.get(reverse('home'))

    def test_home_page_has_search(self):
        """Home page has search form."""
        self.assertContains(self.response, 'input')

    def test_home_page_has_recipes(self):
        """Home page has most recent recipes."""
        for recipe in Recipe.objects.reverse()[:5]:
            self.assertContains(self.response, recipe.title)

    def test_home_page_search_goes_to_search_results(self):
        self.assertContains(self.response, reverse('recipe_search'))


class AboutPageTests(TestCase):
    """Tests for about page."""

    def setUp(self):
        """Initialize a response to be tested."""
        self.response = self.client.get(reverse('about'))


def recipe_with_user(username, title):
    user = User(username=username)
    user.save()
    recipe = Recipe(
        user=user,
        title=title,
        description='a recipe',
        ingredients='food',
        directions='make it'
    )
    recipe.save()
    return recipe


class RecipeStreamTests(TestCase):
    """Tests for recipes on front page."""

    def setUp(self):
        """Initialize three users with recipes."""
        self.my_recipe = recipe_with_user('user1', 'recipe1')
        self.followed_recipe = recipe_with_user('user2', 'recipe2')
        self.not_followed_recipe = recipe_with_user('user3', 'recipe3')
        me = self.my_recipe.user
        self.client.force_login(me)
        me.profile.follows.add(self.followed_recipe.user)
        self.response = self.client.get(reverse('home'))

    def assert_has_recipe(self, recipe):
        self.assertContains(self.response, recipe.title)
        recipe_url = reverse('view_recipe', args=[recipe.id])
        self.assertContains(self.response, 'href="{}"'.format(recipe_url))
        user_url = reverse('profile', args=[recipe.user.username])
        self.assertContains(self.response, 'href="{}"'.format(user_url))

    def test_home_page_has_own_recipe(self):
        self.assert_has_recipe(self.my_recipe)

    def test_home_page_has_followed_recipe(self):
        self.assert_has_recipe(self.followed_recipe)

    def test_home_page_hasnt_other_recipe(self):
        self.assertNotContains(self.response, self.not_followed_recipe.title)
        url = reverse('view_recipe', args=[self.not_followed_recipe.id])
        self.assertNotContains(self.response, 'href="{}"'.format(url))
