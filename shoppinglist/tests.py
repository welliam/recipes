from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShoppingListItem


class ShoppingListDetailView(TestCase):
    def setUp(self):
        self.user = User(username='friend')
        self.user.save()
        self.client.force_login(self.user)
        url = reverse('view_shopping_list')
        self.items = [
            ShoppingListItem(user=self.user, title='item#{}'.format(i))
            for i in range(50)
        ]
        for item in self.items:
            item.save()
        self.response = self.client.get(url)

    def test_shopping_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_shopping_response_has_titles(self):
        for item in self.items:
            self.assertContains(self.response, item.title)
