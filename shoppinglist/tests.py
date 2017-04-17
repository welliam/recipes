from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


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
