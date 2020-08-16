from django.test import TestCase
from django.urls import reverse

from .models import User


class SignupTest(TestCase):

    def test_user_signed_up_success(self):
        response = self.client.post(reverse('create_account'), {
            'first_name': 'Isma',
            'last_name': 'Ouali',
            'username': 'Amsi',
            'email': '1235@gmail.com',
            'password1': 'jfdjfeerfew2514625aw',
            'password2': 'jfdjfeerfew2514625aw'
        })
        self.assertRedirects(response, reverse('welcome'))

    def test_form_not_valid(self):
        response = self.client.post(reverse('create_account'), {
            'first_name': 'Isma',
            'last_name': 'Ouali',
            'username': 'Amsi',
            'email': '1235@gmail.com',
            'password1': 'jfdjfeerfew2514625aw',
            'password2': 'jfdjfeerfew25146aw'
        })
        self.assertIn('password2', response.context['form'].errors)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_user_access_signup_page(self):
        response = self.client.get(reverse('create_account'))
        self.assertTemplateUsed(response, 'user/signup.html')


class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'Test',
            'email': 'test@gmail.com',
        })
        self.user.set_password('jfdjfeerfew2514625aw')
        self.user.save()

    def test_user_signed_in_success(self):
        credentials = {
            'email': 'test@gmail.com',
            'password': 'jfdjfeerfew2514625aw'
        }
        response = self.client.post(reverse('signin'), credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_access_signin_page(self):
        response = self.client.get(reverse('signin'))
        self.assertTemplateUsed(response, 'user/signin.html')

    def test_form_not_valid(self):
        response = self.client.post(reverse('signin'), {
            'email': 'rejwkotrefj@gmail.com',
            'password': 'fredst1516'
        })
        self.assertIn('Mauvais identifiants', response.context['errors'])
        self.assertTemplateUsed(response, 'user/signin.html')


class MyAccountTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'Test',
            'email': 'test@gmail.com',
        })
        self.user.set_password('jfdjfeerfew2514625aw')
        self.user.save()
        credentials = {
            'email': 'test@gmail.com',
            'password': 'jfdjfeerfew2514625aw'
        }
        logged_in = self.client.login(**credentials)

    def test_user_access_myaccount_page(self):
        response = self.client.get(reverse('myaccount'))
        self.assertTemplateUsed(response, 'user/myaccount.html')


class SignoutTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'Test',
            'email': 'test@gmail.com',
        })
        self.user.set_password('jfdjfeerfew2514625aw')
        self.user.save()
        credentials = {
            'email': 'test@gmail.com',
            'password': 'jfdjfeerfew2514625aw'
        }
        self.client.login(**credentials)
    
    def test_logged_out(self):
        response = self.client.get(reverse('signout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


