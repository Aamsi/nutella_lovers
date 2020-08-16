from django.test import TestCase
from django.urls import reverse


class WelcomeTest(TestCase):

    def test_page_is_displayed(self):
        response = self.client.get(reverse('welcome'))
        self.assertTemplateUsed(response, 'nutella_lovers/welcome.html')