from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from recipe.models import Recipe
from .models import RecipeBook


class RecipeBookCreateViewTests(TestCase):
    def setUp(self):
        self.user = User(username='h')
        self.user.save()
        self.client.force_login(self.user)

    def testCreateRecipeBookIncrementsCount(self):
        count = RecipeBook.objects.count()
        self.client.post(reverse('new_recipebook'), dict(
            title='bakes',
            description='lotsa bakes',
        ))
        self.assertEqual(RecipeBook.objects.count(), count + 1)

    def testCreateRecipeBookUnauthenticated(self):
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
    def setUp(self):
        super(RecipeBookDetailViewTests, self).setUp()
        url = reverse('view_recipebook', args=[self.recipebook.id])
        self.response = self.client.get(url)

    def testResponseHasTitle(self):
        self.assertContains(self.response, self.recipebook.title)

    def testResponseHasDescription(self):
        self.assertContains(self.response, self.recipebook.description)

    def testResponseHasContainedRecipes(self):
        for recipe in self.recipes:
            self.assertContains(self.response, recipe.title)

    def testResponseHasEditLink(self):
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertContains(self.response, url)

    def testResponseFromOtherUserHasNoEditLink(self):
        user = User(username='other_friend')
        user.save()
        self.client.force_login(user)
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        edit_url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), edit_url)

    def testResponseFromLoggedOutHasNoEditLink(self):
        self.client.logout()
        view_url = reverse('view_recipebook', args=[self.recipebook.id])
        edit_url = reverse('edit_recipebook', args=[self.recipebook.id])
        self.assertNotContains(self.client.get(view_url), edit_url)


class RecipeBookUpdateViewTests(RecipeBookTestCase):
    def testUpdateTitle(self):
        url = reverse('edit_recipebook', args=[self.recipebook.id])
        new_title = 'new'
        self.client.post(url, dict(
            title=new_title,
            description=self.recipebook.description)
        )
        self.assertEqual(RecipeBook.objects.last().title, new_title)

    def testLoggedOutCannotUpdate(self):
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

    def testOtherUserCannotUpdate(self):
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
    def testDeleteDecrementsCount(self):
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count - 1)

    def testDeleteRedirectsToProfile(self):
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        response = self.client.post(url)
        redirect_url = reverse('profile', args=[self.user.username])
        self.assertEqual(response.url, redirect_url)

    def testGetDeleteViewResponseCode(self):
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.assertEqual(self.client.get(url).status_code, 200)

    def testGetDeleteViewHasForm(self):
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        response = self.client.get(url)
        self.assertContains(response, 'method="POST"')
        self.assertContains(response, '</form>')

    def testOtherUserDeleteMaintainsCount(self):
        other_user = User(username='other_friend')
        other_user.save()
        self.client.force_login(other_user)
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count)

    def testLoggedOutDeleteMaintainsCount(self):
        self.client.logout()
        count = RecipeBook.objects.count()
        url = reverse('delete_recipebook', args=[self.recipebook.id])
        self.client.post(url)
        self.assertEqual(RecipeBook.objects.count(), count)
