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


class NotificationsViewTests(NotificationTestCase):
    def setUp(self):
        super(NotificationsViewTests, self).setUp()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('view_notifications'))

    def test_notification_links_review(self):
        self.assertContains(self.response, self.review.id)


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
        self.client.force_login(self.user)

    def test_notification_count_view(self):
        response = self.client.get(reverse('notification_count_view'))
        count = json.loads(response.content.decode())['count']
        self.assertEqual(count, 1)
