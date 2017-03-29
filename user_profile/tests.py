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
        self.followed_user = User(username='another')
        self.followed_user.save()
        self.user.profile.follows.add(self.followed_user)
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

    def test_profile_shows_followed_users(self):
        self.assertContains(self.response, self.followed_user.username)

    def test_other_profile_has_follow_button(self):
        self.client.force_login(self.user)
        another_user = User(username='one_more')
        another_user.save()
        profile_url = reverse('profile', args=[another_user.username])
        follow_url = format(reverse('follow', args=[another_user.username]))
        follow_action_url = 'action="{}"'.format(follow_url)
        self.assertContains(self.client.get(profile_url), follow_action_url)
        self.assertContains(self.client.get(profile_url), 'value="follow"')

    def test_post_follow(self):
        """Test posting to follow view adds user to follows list."""
        self.client.force_login(self.user)
        another_user = User(username='one_more')
        another_user.save()
        follow_url = format(reverse('follow', args=[another_user.username]))
        self.client.post(follow_url, dict(follow='follow'))
        self.assertEqual(self.user.profile.follows.last(), another_user)

    def test_followed_profile_has_unfollow_button(self):
        self.client.force_login(self.user)
        another_user = User(username='one_more')
        another_user.save()
        self.user.profile.follows.add(another_user)
        profile_url = reverse('profile', args=[another_user.username])
        follow_url = format(reverse('follow', args=[another_user.username]))
        follow_action_url = 'action="{}"'.format(follow_url)
        response = self.client.get(profile_url)
        self.assertContains(response, follow_action_url)
        self.assertContains(response, 'value="unfollow"')

    def test_post_unfollow(self):
        """Test posting to follow view adds user to follows list."""
        self.client.force_login(self.user)
        another_user = User(username='one_more')
        another_user.save()
        self.user.profile.follows.add(another_user)
        follow_url = format(reverse('follow', args=[another_user.username]))
        self.client.post(follow_url, dict(follow='unfollow'))
        self.assertNotEqual(self.user.profile.follows.last(), another_user)

    def test_logged_out_has_no_follow_button(self):
        profile_url = reverse('profile', args=[self.user.username])
        follow_url = format(reverse('follow', args=[self.user.username]))
        follow_action_url = 'action="{}"'.format(follow_url)
        response = self.client.get(profile_url)
        self.assertNotContains(response, follow_action_url)

    def test_post_follow_logged_out_redirects(self):
        follow_url = format(reverse('follow', args=[self.user]))
        response = self.client.post(follow_url, dict(follow='unfollow'))
        self.assertEqual(response.status_code, 302)

    def test_own_profile_has_no_follow_button(self):
        self.client.force_login(self.user)
        url = reverse('profile', args=[self.user.username])
        follow_url = format(reverse('follow', args=[self.user.username]))
        follow_action_url = 'action="{}"'.format(follow_url)
        response = self.client.get(url)
        self.assertNotContains(response, follow_action_url)

    def test_profile_paginates(self):
        title = 'this is some food'
        recipes = [
            Recipe(
                user=self.user,
                title=title,
                description='meal',
                ingredients='food',
                directions='prepare food'
            ) for i in range(50)
        ]
        for recipe in recipes:
            recipe.save()
        url = reverse('profile', args=[self.user.username])
        response = self.client.get(url)
        self.assertContains(response, title, 10)


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


class RecipeBooksTestCase(TestCase):
    """Test case for recipebooks list view."""

    def setUp(self):
        self.username = 'friend'
        self.user = User(username=self.username)
        self.user.save()
        self.client.force_login(self.user)
        self.recipebooks = [
            RecipeBook(
                user=self.user,
                title='this is a recipebook',
                description='recipesss'
            ) for _ in range(50)
        ]
        for book in self.recipebooks:
            book.save()

    def test_recipebooks_list_has_recipes(self):
        url = reverse('profile_recipebooks', args=[self.user.username])
        response = self.client.get(url)
        title = self.recipebooks[0].title
        self.assertContains(response, title, 10)
