import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notification
from review.models import Review
from recipe.models import Recipe


class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test')
        self.user.save()
        self.recipe = Recipe(
            user=self.user,
            title='food',
            description='test',
            ingredients='foods',
            directions='make'
        )
        self.recipe.save()
        self.review = Review(
            title='good review',
            body="it's good",
            user=self.user,
            score=5,
            recipe=self.recipe
        )
        self.review.save()
        self.notification = Notification(
            user=self.user,
            type='review',
            object_key=self.review.id
        )
        self.notification.save()


class NotificationsViewTests(NotificationTestCase):
    def setUp(self):
        super(NotificationsViewTests, self).setUp()

    def test_notification_links_review(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('view_notifications'))
        self.assertContains(response, self.review.id)

    def test_logged_out_redirects(self):
        response = self.client.get(reverse('view_notifications'))
        self.assertEqual(response.status_code, 302)


class ReadNotificationsTests(NotificationTestCase):
    def setUp(self):
        super(ReadNotificationsTests, self).setUp()
        self.client.force_login(self.user)

    def test_reading_notifications(self):
        unread = self.user.notifications.filter(read=False).count()
        self.client.get(reverse('view_notifications'))
        read_count = self.user.notifications.filter(read=False).count()
        self.assertTrue(unread > 0)
        self.assertEqual(read_count, 0)


class NotificationCountView(NotificationTestCase):
    def setUp(self):
        super(NotificationCountView, self).setUp()

    def test_notification_count_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('notification_count_view'))
        count = json.loads(response.content.decode())['count']
        self.assertEqual(count, 1)

    def test_logged_out_disallowed(self):
        response = self.client.get(reverse('notification_count_view'))
        self.assertEqual(response.status_code, 403)


class ReviewNotificationTests(NotificationTestCase):
    def setUp(self):
        """Set up a recipe and review."""
        super(ReviewNotificationTests, self).setUp()

    def test_review_notification_can_get_review(self):
        self.assertEqual(self.notification.get_object(), self.review)

    def test_formatted_review_notification_has_username(self):
        self.assertIn(
            self.review.user.username,
            self.notification.render()
        )

    def test_formatted_review_notification_has_review_pk(self):
        self.assertIn(str(self.review.pk), self.notification.render())

    def test_post_review_adds_notification(self):
        count = self.user.notifications.count()
        url = reverse('new_review', args=[self.recipe.id])
        self.client.force_login(self.user)
        amount = 5
        for i in range(amount):
            self.client.post(url, dict(
                title='review',
                body="it's good",
                score=5
            ))
        self.assertEqual(self.user.notifications.count(), count + amount)

    def test_post_review_adds_notification_to_other_user(self):
        reviewer = User(username="critic")
        reviewer.save()
        self.client.force_login(reviewer)
        count = self.user.notifications.count()
        url = reverse('new_review', args=[self.recipe.id])
        amount = 5
        self.assertEqual(reviewer.notifications.count(), 0)
        for i in range(amount):
            self.client.post(url, dict(
                title='review',
                body="it's good",
                score=5
            ))
        self.assertEqual(self.user.notifications.count(), count + amount)
        self.assertEqual(reviewer.notifications.count(), 0)


class FollowNotificationTests(NotificationTestCase):
    def setUp(self):
        """Set up two users."""
        super(FollowNotificationTests, self).setUp()
        self.followed_user = User(username='friend')
        self.followed_user.save()

    def test_following_adds_notification(self):
        count = self.followed_user.notifications.count()
        self.client.force_login(self.user)
        url = reverse('follow', args=[self.followed_user])
        self.client.post(url, dict(follow='follow'))
        self.assertEqual(self.followed_user.notifications.count(), count + 1)


class RecipeDerivationTests(NotificationTestCase):
    def setUp(self):
        """Set up two users."""
        super(RecipeDerivationTests, self).setUp()
        self.deriving_user = User(username='friend')
        self.deriving_user.save()
        self.client.force_login(self.deriving_user)

    def test_deriving_notifies_original_user(self):
        count = self.user.notifications.count()
        self.client.post(reverse('new_recipe'), dict(
            title='derived recipe',
            description='this recipe is derived from another',
            ingredients='food',
            directions='etc',
            origin_recipe=self.recipe.id,
        ))
        self.assertEqual(self.user.notifications.count(), count + 1)
