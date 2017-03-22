from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
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


class RecipeBookDetailViewTests(TestCase):
    def setUp(self):
        self.user = User(username='h')
        self.user.save()
        self.client.force_login(self.user)
        self.recipebook = RecipeBook(
            title='book',
            description='recipes',
            user=self.user
        )
        self.recipebook.save()
        url = reverse('view_recipebook', args=[self.recipebook.id])
        self.response = self.client.get(url)

    def testResponseHasTitle(self):
        self.assertContains(self.response, self.recipebook.title)

    def testResponseHasDescription(self):
        self.assertContains(self.response, self.recipebook.description)
