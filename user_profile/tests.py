from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe


class UserProfileTestCase(TestCase):
    """Test case for profile mode."""

    def setUp(self):
        self.user = User(username='friend')
        self.user.save()

    def testUserHasProfile(self):
        self.assertTrue(hasattr(self.user, 'profile'))

    def testProfileHasBio(self):
        self.assertTrue(hasattr(self.user.profile, 'bio'))


class ProfileViewTestCase(TestCase):
    """Test case for the profile view."""

    def setUp(self):
        self.username = 'friend'
        user = User(username=self.username)
        user.save()
        self.bio = 'this is a bio'
        user.profile.bio = self.bio
        user.profile.save()
        self.recipe = Recipe(
            user=user,
            title='food',
            description='meal',
            ingredients='food',
            directions='prepare food'
        )
        self.recipe.save()
        url = reverse('profile', args=[user.username])
        self.response = self.client.get(url)

    def testProfileHasUsername(self):
        self.assertContains(self.response, self.username)

    def testProfileHasRecipeTitle(self):
        self.assertContains(self.response, self.recipe.title)

    def testProfileShowsBio(self):
        self.assertContains(self.response, self.bio)


class ProfileEditTestCase(TestCase):
    """Test case for editing profiles."""

    def setUp(self):
        self.username = 'friend'
        self.user = User(username=self.username)
        self.user.save()
        self.client.force_login(self.user)

    def testEditProfileBiography(self):
        bio = 'chef'
        self.client.post(reverse('edit_profile'), dict(bio=bio))
        self.assertEqual(User.objects.last().profile.bio, bio)
