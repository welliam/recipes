from django.test import TestCase
from django.urls import reverse


class StaticPageTests(TestCase):
    """Tests for static pages."""

    def setUp(self):
        """Initialize a response to be tested."""
        self.home = self.client.get(reverse('home'))
        self.about = self.client.get(reverse('about'))

    def testHomePageHasSearch(self):
        """Home page has search form."""
        self.assertContains(self.home, 'input')
