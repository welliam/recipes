import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from recipe.models import Recipe
from .models import RecipeBook


class RecipeBookCreateViewTests(TestCase):
    """Tests for view for creating new recipe books."""

    def setUp(self):
        """Create a user, log the test client as them."""
        self.user = User(username='h')
        self.user.save()
        self.client.force_login(self.user)

    def test_create_recipe_book_increments_count(self):
        """Test posting to view increments number of recipebooks."""
        count = RecipeBook.objects.count()
        self.client.post(reverse('new_recipebook'), dict(
            title='bakes',
            description='lotsa bakes',
        ))
        self.assertEqual(RecipeBook.objects.count(), count + 1)

    def test_create_recipe_book_unauthenticated(self):
        """Test posting to recipebook view unauthenticated does nothing."""
        self.client.logout()
        count = RecipeBook.objects.count()
        self.client.post(reverse('new_recipebook'), dict(
            title='bakes',
            description='lotsa bakes',
        ))
        self.assertEqual(RecipeBook.objects.count(), count)


class RecipeBookTestCase(TestCase):
    """Test case for RecipeBook tests.

    self.client is logged into a test user `self.user`, who owns five
    recipes which belong to self.recipebook."""

    def setUp(self):
        """Create data to be tested.

        create user, recipes, and recipebook which contains those
        recipes."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(self.user)
        self.recipes = [
            Recipe(title=str(title),
                   user=self.user,
                   description='t',
                   ingredients='t',
                   directions='t')
            for title in range(5)
        ]
        self.recipebook = RecipeBook(
            title='book',
            description='recipes',
            user=self.user
        )
        for recipe in self.recipes:
            recipe.save()
            self.recipebook.recipes.add(recipe)
        self.recipebook.save()


class RecipeBookDetailViewTests(RecipeBookTestCase):
    """Tests for view for viewing recipe books."""

    def setUp(self):
        """Get response of view for recipe book."""
        super(RecipeBookDetailViewTests, self).setUp()
        url = reverse('view_recipebook', args=[self.recipebook.id])
        self.response = self.client.get(url)

    def test_response_has_title(self):
        """Test response has title of recipe book."""
        self.assertContains(self.response, self.recipebook.title)

    def test_response_has_description(self):
        """Test response has description of recipe book."""
        self.assertContains(self.response, self.recipebook.description)

    def test_response_has_recipes(self):
        """Test response has recipes attached to recipebook."""
        for recipe in self.recipes:
            self.assertContains(self.response, recipe.title)

    def test_response_has_edit_link(self):
        """Test response has link for editing this recipe book."""
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertContains(self.response, url)

    def test_response_from_other_user_has_no_edit_link(self):
        """Test view only shows edit link if recipe book is owned by user."""
        user = User(username='other_friend')
        user.save()
        self.client.force_login(user)
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        edit_url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), edit_url)

    def test_response_from_logged_out_has_no_edit_link(self):
        """Test view only shows edit link if recipe book is owned by user."""
        self.client.logout()
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        edit_url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), edit_url)

    def test_response_has_delete_link(self):
        """Test view shows delete link for this recipe book."""
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.assertContains(self.response, url)

    def test_response_from_other_user_has_no_delete_link(self):
        """Test view only shows delete link if recipe book is owned by user."""
        user = User(username='other_friend')
        user.save()
        self.client.force_login(user)
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        delete_url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), delete_url)

    def test_response_logged_out_has_no_delete_link(self):
        """Test view only shows delete link if recipe book is owned by user."""
        self.client.logout()
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        delete_url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), delete_url)

    def test_paginated_recipebook(self):
        """Test recipe book paginates recipes."""
        title = 'this is a title'
        for _ in range(50):
            recipe = Recipe(
                title=title,
                user=self.user,
                description='t',
                ingredients='t',
                directions='t'
            )
            recipe.save()
            self.recipebook.recipes.add(recipe)
        p2 = reverse('view_recipebook', args=[self.recipebook.id]) + '?p=2'
        self.assertContains(self.client.get(p2), title, 10)
        p3 = reverse('view_recipebook', args=[self.recipebook.id]) + '?p=3'
        self.assertContains(self.client.get(p3), title, 10)


class RecipeBookUpdateViewTests(RecipeBookTestCase):
    """Tests for view for updating recipe book."""

    def test_update_title(self):
        """Test posting new title updates recipe book."""
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        new_title = 'new'
        self.client.post(url, dict(
            title=new_title,
            description=self.recipebook.description)
        )
        self.assertEqual(RecipeBook.objects.last().title, new_title)

    def test_logged_out_cannot_update(self):
        """Test logged out users cannot update recipebooks."""
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        new_title = 'new'
        self.client.logout()
        self.client.post(url, dict(
            title=new_title,
            description=self.recipebook.description)
        )
        self.assertEqual(
            RecipeBook.objects.last().title,
            self.recipebook.title
        )

    def test_other_user_cannot_update(self):
        """Test other users cannot update recipe books."""
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        new_title = 'new'
        other_user = User(username='other_friend')
        other_user.save()
        self.client.force_login(other_user)
        self.client.post(url, dict(
            title=new_title,
            description=self.recipebook.description)
        )
        self.assertEqual(
            RecipeBook.objects.last().title,
            self.recipebook.title
        )


class RecipeBookDeleteViewTests(RecipeBookTestCase):
    """Test view for deleting recipe books."""

    def test_delete_decrements_count(self):
        """Test posting to delete view decrements number of recipebooks."""
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count - 1)

    def test_delete_redirects_to_recipebook_list(self):
        """Test deleting book redirects to user's list of recipe books."""
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        response = self.client.post(url)
        redirect_url = reverse(
            'profile_recipebooks', args=[self.user.username]
        )
        self.assertEqual(response.url, redirect_url)

    def test_get_delete_view_response_code(self):
        """Test user can GET delete view."""
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_get_delete_view_has_form(self):
        """Test delete view has form for deleting recipe books."""
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        response = self.client.get(url)
        self.assertContains(response, 'method="POST"')
        self.assertContains(response, '</form>')

    def test_other_user_delete_maintains_count(self):
        """Test other users cannot delete recipe books."""
        other_user = User(username='other_friend')
        other_user.save()
        self.client.force_login(other_user)
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count)

    def test_logged_out_delete_maintains_count(self):
        """Test recipe books cannot be deleted by a logged out user."""
        self.client.logout()
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count)


class RecipeBookAjaxCreateTests(TestCase):
    """Test view for creating recipe books by ajax."""

    def setUp(self):
        """Get user and url."""
        self.user = User(username='h')
        self.user.save()
        self.client.force_login(self.user)
        self.url = reverse('ajax_create_recipebook')

    def test_post_creates_recipebook(self):
        """Test posting to view increments number of books."""
        count = RecipeBook.objects.count()
        self.client.post(self.url, dict(title='hi', description='there'))
        self.assertEqual(RecipeBook.objects.count(), count + 1)

    def test_post_returns_json_id(self):
        """Test posting to view returns id of newest recipebook."""
        response = self.client.post(
            self.url, dict(title='hi', description='there')
        )
        new_id = int(json.loads(response.content.decode())['id'])
        new_recipebook = RecipeBook.objects.order_by('date_created').last()
        self.assertEqual(new_id, new_recipebook.id)

    def test_logged_out_maintains_count(self):
        """Test posting to view while logged out does nothing."""
        self.client.logout()
        count = RecipeBook.objects.count()
        self.client.post(self.url, dict(title='hi', description='there'))
        self.assertEqual(RecipeBook.objects.count(), count)
