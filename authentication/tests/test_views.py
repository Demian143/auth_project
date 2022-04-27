from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate


class TestSignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = self.client.post(reverse('authentication:signin'),
                                         data={"name": "Demian",
                                               "email": "demian@example.com",
                                               "password": "123456"})

    def test_get_signin_page(self):
        response = self.client.get(reverse('authentication:signin'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signin.html')

    def test_signin_success(self):
        self.assertEquals(self.new_user.status_code, 302)

    def test_signin_user_already_exist(self):
        user_already_exist = self.client.post(reverse('authentication:signin'),
                                              data={"name": "Demian",
                                                    "email": "demian@example.com",
                                                    "password": "123456"})

        self.assertEquals(user_already_exist.content,
                          b'User already exists.')


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.page = self.client.get(reverse('authentication:user_login'))
        self.new_user = self.client.post(reverse('authentication:signin'),
                                         data={"name": "Demian",
                                               "email": "demian@example.com",
                                               "password": "123456"})

    def test_get_login_page(self):
        self.assertEquals(self.page.status_code, 200)

    def test_authentication_success(self):
        login = self.client.post(
            reverse('authentication:user_login'), data={"name": "Demian", "password": "123456"})
        self.assertEquals(login.status_code, 302)

    def test_invalid_username(self):
        login = self.client.post(
            reverse('authentication:user_login'), data={"name": "Demiann", "password": "123456"})
        self.assertEquals(login.content, b'Something wrong, try again.')

    def test_invalid_password(self):
        login = self.client.post(
            reverse('authentication:user_login'), data={"name": "Demian", "password": "1234567"})
        self.assertEquals(login.content, b'Something wrong, try again.')

    def test_user_logout(self):
        logout = self.client.get(reverse('authentication:user_logout'))
        self.assertEquals(logout.status_code, 302)


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = self.client.post(reverse('authentication:signin'),
                                         data={"name": "Demian",
                                               "email": "demian@example.com",
                                               "password": "123456"})
        self.user_login = self.client.post(reverse('authentication:user_login'),
                                           data={"name": "Demian",
                                                 "password": "123456"})
        self.page = self.client.get(reverse('authentication:delete_account'))

    def test_get_delete_page(self):
        self.assertEquals(self.page.status_code, 200)

    def test_deletion_success(self):
        delete = self.client.post(reverse('authentication:delete_account'), data={
            "password": "123456", "confirm_password": "123456"})

        self.assertEquals(delete.status_code, 302)

    def test_trying_to_login_with_deleted_user(self):
        self.test_deletion_success()
        user_login = self.client.post(reverse('authentication:user_login'),
                                      data={"name": "Demian",
                                            "password": "123456"})
        # try to login again
        self.assertEquals(user_login.content, b'Something wrong, try again.')


class TestUserHomePage(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_user = self.client.post(reverse('authentication:signin'),
                                         data={"name": "Demian",
                                               "email": "demian@example.com",
                                               "password": "123456"})
        self.user_login = self.client.post(reverse('authentication:user_login'),
                                           data={"name": "Demian",
                                                 "password": "123456"})
        self.page = self.client.get(reverse('authentication:user_home'))

    def test_get_user_home_page(self):
        self.assertEquals(self.page.status_code, 200)


class TestUpdateCredentials(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "demian@example.com"
        self.password = "123456"
        self.username = "Demian"

        self.new_user = self.client.post(reverse('authentication:signin'),
                                         data={"name": self.username,
                                               "email": self.email,
                                               "password": self.password})
        self.user_login = self.client.post(reverse('authentication:user_login'),
                                           data={"name": "Demian",
                                                 "password": "123456"})
        self.update_email = self.client.get(
            reverse('authentication:update_email'))
        self.update_username = self.client.get(
            reverse('authentication:update_username'))
        self.update_password = self.client.get(
            reverse('authentication:update_password'))

    def test_get_update_email(self):
        self.assertEquals(self.update_email.status_code, 200)

    def test_get_update_username(self):
        self.assertEquals(self.update_username.status_code, 200)

    def test_get_update_password(self):
        self.assertEquals(self.update_password.status_code, 200)

    def test_update_email(self):
        new_email = 'demian_new@example.com'
        self.client.post(reverse('authentication:update_email'), data={
                         'new_email': new_email, 'confirm_new_email': new_email, 'password': self.password})

        user = authenticate(username=self.username, password=self.password)

        self.assertIsNotNone(user)
        self.assertEquals(user.email, new_email)

    def test_update_username(self):
        new_username = "Demian_new"

        self.client.post(reverse('authentication:update_username'), data={
                         'new_username': new_username, 'password': self.password})

        user = authenticate(username=new_username, password=self.password)

        self.assertIsNotNone(user)
        # I know it's redundant, but let's make sure it works properly
        self.assertEquals(user.username, new_username)

    def test_update_password(self):
        new_password = "1234567"

        self.client.post(reverse('authentication:update_password'), data={
                         'old_password': self.password,
                         'new_password': new_password,
                         'confirm_new_password': new_password})

        user = authenticate(username=self.username, password=new_password)
        self.assertIsNotNone(user)

        login_with_new_password_template = self.client.post(reverse('authentication:user_login'), data={
            "name": self.username, "password": new_password})

        self.assertAlmostEquals(
            login_with_new_password_template.status_code, 302)
