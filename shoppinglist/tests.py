from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ShoppingListDetailView(TestCase):
    def setUp(self):
        self.user = User(username='friend')
        self.user.save()
        self.client.force_login(self.user)
        url = reverse('view_shopping_list')
        self.response = self.client.get(url)

    def test_shopping_response_has_titles(self):
        self.assertEqual(self.response.status_code, 200)
