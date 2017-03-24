from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe
from .models import Review

def get_user_and_recipe(username='chef'):
        user = User(username='chef')
        user.save()
        recipe = Recipe(
            user=user,
            title='food',
            description='food',
            ingredients='food',
            directions='food'
        )
        recipe.save()
        return user, recipe


class ReviewTestCase(TestCase):
    def setUp(self):
        self.user, self.recipe = get_user_and_recipe()
        self.client.force_login(self.user)
        url = reverse('view_recipe', args=[self.recipe.id])
        self.response = self.client.get(url)


class CreateReviewTestCase(ReviewTestCase):
    def post_review(self):
        self.client.post(reverse('new_review', args=[self.recipe.id]), dict(
            title='good review',
            score=3,
            body='very good',
        ))

    def testPostingUpdatesCount(self):
        """Test viewing recipe has form for review."""
        count = Review.objects.count()
        self.post_review()
        self.assertEqual(Review.objects.count(), count + 1)

    def testLoggedOutUserCannotPost(self):
        count = Review.objects.count()
        self.client.logout()
        self.post_review()
        self.assertEqual(Review.objects.count(), count)


class DeleteReviewTestCase(ReviewTestCase):
    def setUp(self):
        super(DeleteReviewTestCase, self).setUp()
        self.review = Review(
            user=self.user,
            recipe=self.recipe,
            title='review',
            body='body',
            score=3
        )
        self.review.save()

    def delete_review(self):
        self.client.post(reverse('delete_review', args=[self.review.id]))

    def testDeleteReview(self):
        count = Review.objects.count()
        self.delete_review()
        self.assertEqual(Review.objects.count(), count - 1)

    def testOtherUserCannotDeleteReview(self):
        other_user = User(username='other')
        other_user.save()
        self.client.force_login(other_user)
        count = Review.objects.count()
        self.delete_review()
        self.assertEqual(Review.objects.count(), count)

    def testLoggedOutCannotDeleteReview(self):
        self.client.logout()
        count = Review.objects.count()
        self.delete_review()
        self.assertEqual(Review.objects.count(), count)

    def testDeleteViewFormMethod(self):
        url = reverse('delete_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertContains(response, 'method="POST"')
