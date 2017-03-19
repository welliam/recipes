from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe


class ProfileViewTestCase(TestCase):
    """Test case for the profile view."""

    def setUp(self):
        self.username = 'friend'
        user = User(username=self.username)
        user.save()
        self.recipe = Recipe(
            user = user,
            title='food',
            description='meal',
            ingredients='food',
            directions='prepare food'
        )
        self.recipe.save()
        self.response = self.client.get(reverse('profile', args=[user.username]))

    def testProfileHasUsername(self):
        self.assertContains(self.response, self.username)

    def testProfileHasRecipeTitle(self):
        self.assertContains(self.response, self.recipe.title)
