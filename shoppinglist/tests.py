from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShoppingList


class ShoppingListCreateViewTests(TestCase):
    def setUp(self):
        self.user = User(username='friend')
        self.user.save()
        self.client.force_login(self.user)

    def test_get_create_view(self):
        status = self.client.get(reverse('create_shopping_list')).status_code
        self.assertEqual(status, 200)

    def test_create_view_has_form(self):
        response = self.client.get(reverse('create_shopping_list'))
        self.assertContains(response, '</form>')
        self.assertContains(response, 'method="POST"')

    def test_get_create_view_logged_out_redirects(self):
        self.client.logout()
        status = self.client.get(reverse('create_shopping_list')).status_code
        self.assertEqual(status, 302)

    def test_post_creates_list(self):
        count = ShoppingList.objects.count()
        self.client.post(reverse('create_shopping_list'), dict(title='title'))
        self.assertEqual(ShoppingList.objects.count(), count + 1)


class ShoppingListDetailView(TestCase):
    def setUp(self):
        self.user = User(username='friend')
        self.user.save()
        self.client.force_login(self.user)
        lst = ShoppingList(user=self.user, title='this is a list')
        lst.save()
        url = reverse('view_shopping_list', args=[lst.id])
        self.response = self.client.get(url)

    def test_shopping_response_has_titles(self):
        title = self.user.shoppinglists.first().title
        self.assertContains(self.response, title)
