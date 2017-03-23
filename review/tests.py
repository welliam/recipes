from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe
from .models import Review


class CreateReviewTestCase(TestCase):
    def setUp(self):
        self.user = User(username='chef')
        self.user.save()
        self.client.force_login(self.user)
        self.recipe = Recipe(
            user=self.user,
            title='food',
            description='food',
            ingredients='food',
            directions='food'
        )
        self.recipe.save()
        url = reverse('view_recipe', args=[self.recipe.id])
        self.response = self.client.get(url)

    def testPostingDataUpdatesCount(self):
        """Test viewing recipe has form for review."""
        count = Review.objects.count()
        self.client.post(reverse('new_review', args=[self.recipe.id]), dict(
            title='good review',
            score=3,
            body='very good',
        ))
        self.assertEqual(Review.objects.count(), count + 1)
