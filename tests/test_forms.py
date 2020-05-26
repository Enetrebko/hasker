from django.test import TestCase
from hasker_app.forms import AskQuestionForm, AnswerForm, SignUpForm, CustomAuthenticationForm, ChangeProfileForm
from django.contrib.auth.models import User


class AskQuestionFormTest(TestCase):

    def test_empty_header(self):
        data = {'header': '',
                'body': 'Body',
                'tags': 'tag',
                }
        form = AskQuestionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['header'])

    def test_empty_body(self):
        data = {'header': 'Header',
                'body': '',
                'tags': 'tag',
                }
        form = AskQuestionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['body'])

    def test_header_too_long(self):
        data = {'header': 'a' * 301,
                'body': 'Body',
                'tags': 'tag',
                }
        form = AskQuestionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at most', form.errors['header'][0])

    def test_body_too_long(self):
        data = {'header': 'Header',
                'body': 'a' * 1001,
                'tags': 'tag',
                }
        form = AskQuestionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at most', form.errors['body'][0])

    def test_too_much_tags(self):
        data = {'header': 'Header',
                'body': 'Body',
                'tags': 'tag1, tag2, tag3, tag4',
                }
        form = AskQuestionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter three tags or less', form.errors['tags'])

    def test_valid_form_empty_tags(self):
        data = {'header': 'Header',
                'body': 'Body',
                'tags': '',
                }
        form = AskQuestionForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_form_tags_with_spaces(self):
        data = {'header': 'Header',
                'body': 'Body',
                'tags': 'tag1,  tag2',
                }
        form = AskQuestionForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_form_tags_wo_spaces(self):
        data = {'header': 'Header',
                'body': 'Body',
                'tags': 'tag1,tag2',
                }
        form = AskQuestionForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_form_tags_zero_length(self):
        data = {'header': 'Header',
                'body': 'Body',
                'tags': 'tag1,tag2,,,tag3,,',
                }
        form = AskQuestionForm(data)
        self.assertTrue(form.is_valid())


class AnswerFormTest(TestCase):

    def test_empty_body(self):
        data = {'body': ''}
        form = AnswerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['body'])

    def test_valid_form(self):
        data = {'body': 'body'}
        form = AnswerForm(data)
        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):

    def test_invalid_username(self):
        data = {'username': 'a,b',
                'email': 'aa@bb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd123456',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid username', form.errors['username'][0])

    def test_too_long_username(self):
        data = {'username': 'a' * 101,
                'email': 'aa@bb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd123456',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at most', form.errors['username'][0])

    def test_invalid_email(self):
        data = {'username': 'testuser',
                'email': 'aabb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd123456',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'][0])

    def test_username_already_exists(self):
        User.objects.create(username='user', email='aa@bb.cc', password='pwd123456')
        data = {'username': 'testuser',
                'email': 'aa@bb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd123456',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('A user with that username already exists.', form.errors['username'][0])

    def test_invalid_password(self):
        data = {'username': 'testuser',
                'email': 'aa@bb.cc',
                'password1': 'pwd',
                'password2': 'pwd',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('This password is too short', form.errors['password2'][0])

    def test_passwords_dont_match(self):
        data = {'username': 'testuser',
                'email': 'aa@bb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd',
                }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('The two password fields didn’t match.', form.errors['password2'][0])

    def test_valid_form(self):
        data = {'username': 'testuser',
                'email': 'aa@bb.cc',
                'password1': 'pwd123456',
                'password2': 'pwd123456',
                }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())


class CustomAuthenticationFormTest(TestCase):

    def test_does_not_exist(self):
        data = {'username': 'testuser',
                'password': 'pwd123456',
                }
        form = CustomAuthenticationForm(None, data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please enter a correct %(username)s and password', form.error_messages['invalid_login'])

    def test_incorrect_pass(self):
        user = User.objects.create(username='testuser', email='test@test.com')
        user.set_password('pwd123456')
        user.save()
        data = {'username': 'testuser',
                'password': 'pwd1234567',
                }
        form = CustomAuthenticationForm(None, data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please enter a correct %(username)s and password', form.error_messages['invalid_login'])

    def test_valid_form(self):
        user = User.objects.create(username='testuser', email='aa@bb.cc')
        user.set_password('pwd123456')
        user.save()
        data = {
            'username': 'testuser',
            'password': 'pwd123456',
        }
        form = CustomAuthenticationForm(None, data)
        self.assertTrue(form.is_valid())


class ChangeProfileFormTest(TestCase):

    def test_invalid_email(self):
        data = {'email': 'aabb.cc'}
        form = ChangeProfileForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'][0])

    def test_valid_form(self):
        data = {'email': 'aa@bb.cc'}
        form = ChangeProfileForm(data)
        self.assertTrue(form.is_valid())
