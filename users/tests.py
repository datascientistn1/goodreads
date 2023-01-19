from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTest(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                'username': 'Botirbekkkk',
                'first_name': 'Botirbek',
                'last_name': 'Ruzimboyev',
                'email': 'botirbek@gmail.com',
                'password': 'somepassword'
            }
        )

        user = CustomUser.objects.get(username='Botirbekkkk')

        self.assertEqual(user.first_name, 'Botirbek')
        self.assertEqual(user.last_name, 'Ruzimboyev')
        self.assertEqual(user.email, 'botirbek@gmail.com')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'first_name': 'Botirbek',
                'email': 'botirbek@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', "This field is required.")
        self.assertFormError(response, 'form', 'password', "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'username': 'Botirbekkkk',
                'first_name': 'Botirbek',
                'last_name': 'Ruzimboyev',
                'email': 'botirbek',
                'password': 'somepassword'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username='nurzilola', first_name='Nurzilola')
        user.set_password('nurzilola2004')
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                'username': 'nurzilola',
                'first_name': 'Nurzilola',
                'last_name': 'Maminova',
                'email': 'nurzilola@gmail.com',
                'password': 'nurzilola2004'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', "A user with that username already exists.")


class LoginTest(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='nurzilola', first_name='Nurzilola')
        self.db_user.set_password('nurzilola2004')
        self.db_user.save()

    def test_seccessful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'nurzilola',
                'password': 'nurzilola2004'
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'nurzilolaaa',
                'password': 'nurzilola2004'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'nurzilola',
                'password': 'nurzilolaaa2004'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='nurzilola', password='nurzilola2004')
        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(username='nurzilola', first_name='Nurzilola', last_name="Maminova",
                                         email="nurzilola@gmail.com")
        user.set_password('nurzilola2004')
        user.save()
        self.client.login(username='nurzilola', password='nurzilola2004')

        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username='nurzilola', first_name='Nurzilola', last_name="Maminova",
                                         email="nurzilola@gmail.com")
        user.set_password('nurzilola2004')
        user.save()

        self.client.login(username='nurzilola', password='nurzilola2004')

        response = self.client.post(
            reverse("users:profile_edit"),
            data={
                "username": 'nurzilola',
                "first_name": 'Nurzilola',
                "last_name": "Maminovaaa",
                'email': "nurzilola3@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Maminovaaa")
        self.assertEqual(user.email, "nurzilola3@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))





