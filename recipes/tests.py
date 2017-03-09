from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    """Tests for the home page."""

    def setUp(self):
        """Initialize a response to be tested."""
        self.response = self.client.get(reverse('homepage'))

    def testHomePageHasSearch(self):
        """Home page has search form."""
        self.assertContains(self.response, 'input')
