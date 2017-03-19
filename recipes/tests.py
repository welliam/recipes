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

    def testHomePageHasSearch(self):
        """Home page has search form."""
        self.assertContains(self.response, 'input')

    def testHomePageHasRecipes(self):
        """Home page has most recent recipes."""
        for recipe in Recipe.objects.reverse()[:5]:
            self.assertContains(self.response, recipe.title)


class AboutPageTests(TestCase):
    """Tests for about page."""

    def setUp(self):
        """Initialize a response to be tested."""
        self.response = self.client.get(reverse('about'))
