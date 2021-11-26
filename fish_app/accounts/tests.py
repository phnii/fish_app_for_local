from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import SignupForm
from .views import SignupView

class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@email.com',
            password='testpass123'
        )
        self.assertEqual(superuser.username, 'testsuperuser')
        self.assertEqual(superuser.email, 'testsuperuser@email.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

class SignupPageTests(TestCase):
    
    def setUp(self):
        url =  '/accounts/signup/'
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
        self.assertContains(self.response, 'ユーザー')
        self.assertNotContains(
            self.response, 'これは新規投稿ページではありません。'
        )

    def test_signup_form(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, user.username)
        self.assertEqual(get_user_model().objects.all()[0].email, user.email)