from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe
from recipebook.models import RecipeBook


class UserProfileTestCase(TestCase):
    """Test case for profile mode."""

    def setUp(self):
        self.user = User(username='friend')
        self.user.save()

    def test_user_has_profile(self):
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_profile_has_bio(self):
        self.assertTrue(hasattr(self.user.profile, 'bio'))


class ProfileViewTestCase(TestCase):
    """Test case for the profile view."""

    def setUp(self):
        self.username = 'friend'
        self.user = User(username=self.username)
        self.user.save()
        self.bio = 'this is a bio'
        self.user.profile.bio = self.bio
        self.user.profile.save()
        self.recipe = Recipe(
            user=self.user,
            title='food',
            description='meal',
            ingredients='food',
            directions='prepare food'
        )
        self.recipe.save()
        self.recipebook = RecipeBook(
            user=self.user,
            title='foods',
            description='lots of them'
        )
        self.recipebook.save()
        url = reverse('profile', args=[self.user.username])
        self.response = self.client.get(url)

    def test_profile_has_username(self):
        self.assertContains(self.response, self.username)

    def test_profile_has_recipe_title(self):
        self.assertContains(self.response, self.recipe.title)

    def test_profile_shows_bio(self):
        self.assertContains(self.response, self.bio)

    def test_profile_has_edit_logged_in(self):
        self.client.force_login(self.user)
        url = reverse('profile', args=[self.user.username])
        self.assertContains(self.client.get(url), reverse('edit_profile'))

    def test_profile_has_no_edit_logged_out(self):
        self.assertNotContains(self.response, reverse('edit_profile'))

    def test_profile_has_no_edit_wrong_user(self):
        user = User(username='someone_else')
        user.save()
        self.client.force_login(user)
        url = reverse('profile', args=[self.user.username])
        self.assertNotContains(self.client.get(url), reverse('edit_profile'))

    def test_profile_shows_recipebooks(self):
        self.assertContains(self.response, self.recipebook.title)

    def test_profile_links_recipebooks(self):
        url = reverse('view_recipebook', args=[self.recipebook.id])
        self.assertContains(self.response, url)


class ProfileEditTestCase(TestCase):
    """Test case for editing profiles."""

    def setUp(self):
        self.username = 'friend'
        self.user = User(username=self.username)
        self.user.save()
        self.client.force_login(self.user)

    def test_edit_profile_biography(self):
        bio = 'chef'
        self.client.post(reverse('edit_profile'), dict(bio=bio))
        self.assertEqual(User.objects.last().profile.bio, bio)
