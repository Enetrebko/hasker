from django.test import TestCase
from django.urls import reverse_lazy
from django.core import mail
from hasker_app.forms import *
from hasker_app.models import *


class AskQuestionViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('pwd123456')
        user.save()

    def test_not_auth_user_redirect(self):
        response = self.client.get(reverse_lazy("hasker_app:ask"))
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")),
                                                "?next=",
                                                str(reverse_lazy("hasker_app:ask"))]))

    def test_auth_user_get(self):
        self.client.login(username='testuser', password='pwd123456')
        response = self.client.get(reverse_lazy("hasker_app:ask"))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('ask_question.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIsInstance(response.context['form'], AskQuestionForm)
        self.client.logout()

    def test_auth_user_ask_question(self):
        self.client.login(username='testuser', password='pwd123456')
        response = self.client.post(reverse_lazy("hasker_app:ask"),
                                    data={'header': 'Header', 'body': 'Body', 'tags': 'tag'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        question = Question.objects.get(header='Header')
        self.assertRedirects(response, reverse_lazy('hasker_app:question', args=[question.id]))
        self.assertQuerysetEqual(question.tags.all(), ['<Tag: tag>'])
        self.assertEqual(question.body, 'Body')
        self.client.logout()


class QuestionViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', email='aa@bb.cc')
        user.set_password('pwd123456')
        user.save()
        another_user = User.objects.create(username='another_user')
        another_user.set_password('pwd123456')
        another_user.save()
        self.question = Question.objects.create(header='Header', body='Body', user=user)
        self.answer = Answer.objects.create(question=self.question, body='Body', user=another_user)
        self.another_answer = Answer.objects.create(question=self.question, body='Another Body', user=another_user)

    def test_not_auth_user_get(self):
        response = self.client.get(reverse_lazy("hasker_app:question", kwargs={'pk': self.question.pk}))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertNotIn('answer_form.html', template_names)

    def test_auth_user_get(self):
        self.client.login(username='testuser', password='pwd123456')
        response = self.client.get(reverse_lazy("hasker_app:question", kwargs={'pk': self.question.pk}))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIn('answer_form.html', template_names)
        self.assertIsInstance(response.context['form'], AnswerForm)
        self.client.logout()

    def test_auth_user_answer(self):
        self.client.login(username='another_user', password='pwd123456')
        response = self.client.post(reverse_lazy("hasker_app:question", kwargs={'pk': self.question.pk}),
                                    data={'body': 'test_answer'},
                                    follow=True
                                    )
        self.assertEqual(response.status_code, 200)
        answer = Answer.objects.get(body='test_answer')
        self.assertIn(answer, self.question.answer_set.all())
        self.assertRedirects(response, reverse('hasker_app:question', kwargs={'pk': self.question.pk}))

        # test email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.question.user.email])
        self.assertEqual(mail.outbox[0].subject, 'New answer')
        self.assertIn(self.question.get_absolute_url(), mail.outbox[0].body)
        self.client.logout()

    def test_not_auth_vote_question_redirect(self):
        url = reverse_lazy("hasker_app:vote_up", kwargs={'object_type': 'question', 'obj_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")), "?next=", str(url)]))
        url = reverse_lazy("hasker_app:vote_down", kwargs={'object_type': 'question', 'obj_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")), "?next=", str(url)]))

    def test_auth_vote_question(self):
        self.client.login(username='testuser', password='pwd123456')
        user = User.objects.get(username='testuser')
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, 0)

        # vote up

        url = reverse_lazy("hasker_app:vote_up", kwargs={'object_type': 'question', 'obj_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, 1)
        self.assertIn(user, question.users_voted_up.all())

        # vote up again

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, 1)
        self.assertIn(user, question.users_voted_up.all())

        # vote down

        url = reverse_lazy("hasker_app:vote_down", kwargs={'object_type': 'question', 'obj_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, 0)
        self.assertNotIn(user, question.users_voted_up.all())
        self.assertNotIn(user, question.users_voted_down.all())

        # vote down again

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, -1)
        self.assertNotIn(user, question.users_voted_up.all())
        self.assertIn(user, question.users_voted_down.all())

        # vote down one more time

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.votes, -1)
        self.assertNotIn(user, question.users_voted_up.all())
        self.assertIn(user, question.users_voted_down.all())
        self.client.logout()

    def test_not_auth_vote_answer_redirect(self):
        url = reverse_lazy("hasker_app:vote_up", kwargs={'object_type': 'answer', 'obj_id': self.answer.pk})
        response = self.client.get(url)
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")), "?next=", str(url)]))
        url = reverse_lazy("hasker_app:vote_down", kwargs={'object_type': 'answer', 'obj_id': self.answer.pk})
        response = self.client.get(url)
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")), "?next=", str(url)]))

    def test_auth_vote_answer(self):
        self.client.login(username='testuser', password='pwd123456')
        user = User.objects.get(username='testuser')
        answer = Answer.objects.get(id=self.answer.id)
        question = answer.question
        self.assertEqual(answer.votes, 0)

        # vote up

        url = reverse_lazy("hasker_app:vote_up", kwargs={'object_type': 'answer', 'obj_id': self.answer.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        answer = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer.votes, 1)
        self.assertIn(user, answer.users_voted_up.all())

        # vote up again

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        answer = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer.votes, 1)
        self.assertIn(user, answer.users_voted_up.all())

        # vote down

        url = reverse_lazy("hasker_app:vote_down", kwargs={'object_type': 'answer', 'obj_id': self.answer.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        answer = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer.votes, 0)
        self.assertNotIn(user, answer.users_voted_up.all())
        self.assertNotIn(user, answer.users_voted_down.all())

        # vote down again

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        answer = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer.votes, -1)
        self.assertNotIn(user, answer.users_voted_up.all())
        self.assertIn(user, answer.users_voted_down.all())

        # vote down one more time

        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))
        answer = Answer.objects.get(id=self.answer.id)
        self.assertEqual(answer.votes, -1)
        self.assertNotIn(user, answer.users_voted_up.all())
        self.assertIn(user, answer.users_voted_down.all())
        self.client.logout()

    def test_mark_right_answer_not_auth(self):
        url = reverse_lazy("hasker_app:correct_answer", kwargs={'answer_id': self.answer.pk,
                                                                'question_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")), "?next=", str(url)]))

    def test_mark_right_answer_not_owner(self):
        self.client.login(username='another_user', password='pwd123456')
        url = reverse_lazy("hasker_app:correct_answer", kwargs={'answer_id': self.answer.pk,
                                                                'question_id': self.question.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': self.question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertIsNone(question.correct_answer)
        self.client.logout()

    def test_mark_right_answer_owner(self):
        self.client.login(username='testuser', password='pwd123456')
        url = reverse_lazy("hasker_app:correct_answer", kwargs={'answer_id': self.answer.id,
                                                                'question_id': self.question.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse_lazy('hasker_app:question', kwargs={'pk': self.question.id}))
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(self.answer, question.correct_answer)

        # mark another answer

        url = reverse_lazy("hasker_app:correct_answer", kwargs={'answer_id': self.another_answer.id,
                                                                'question_id': self.question.id})
        _ = self.client.get(url)
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(self.another_answer, question.correct_answer)
        self.client.logout()


class IndexViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse_lazy("hasker_app:index"))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIn('index.html', template_names)
        self.assertIn('questions_list.html', template_names)


class SearchViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        self.question1 = Question.objects.create(header='a', body='b', user=user)
        self.question2 = Question.objects.create(header='b', body='ab', user=user)
        self.question3 = Question.objects.create(header='ba', body='b', user=user)
        self.question4 = Question.objects.create(header='bb', body='a', user=user)
        self.question5 = Question.objects.create(header='bc', body='b', user=user)

    def test_empty_query(self):
        response = self.client.get(reverse_lazy("hasker_app:search_results"), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Question.objects.all()), len(response.context['object_list']))

    def test_search_any(self):
        response = self.client.get(reverse_lazy("hasker_app:search_results"), {'q': 'a'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question1, response.context['object_list'])
        self.assertIn(self.question2, response.context['object_list'])
        self.assertIn(self.question3, response.context['object_list'])
        self.assertIn(self.question4, response.context['object_list'])
        self.assertNotIn(self.question5, response.context['object_list'])

    def search_tag(self):
        tag1 = Tag.objects.create(tag_text='tag1')
        tag2 = Tag.objects.create(tag_text='tag2')
        self.question1.tags.add(tag1)
        self.question2.tags.add(tag1)
        self.question2.tags.add(tag2)
        response = self.client.get(reverse_lazy("hasker_app:search_results"), {'q': 'tag:  tag1 '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question1, response.context['object_list'])
        self.assertIn(self.question2, response.context['object_list'])
        self.assertNotIn(self.question3, response.context['object_list'])
        response = self.client.get(reverse_lazy("hasker_app:search_results"), {'q': 'tag:tag1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question1, response.context['object_list'])
        self.assertIn(self.question2, response.context['object_list'])
        self.assertNotIn(self.question3, response.context['object_list'])


class SignUpView(TestCase):
    def test_get(self):
        response = self.client.get(reverse('hasker_app:signup'))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('registration/signup.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIsInstance(response.context['user_form'], SignUpForm)
        self.assertIsInstance(response.context['user_profile_form'], UserProfileForm)

    def test_post_redirect(self):
        response = self.client.post(reverse_lazy('hasker_app:signup'),
                                    data={'username': 'testuser',
                                          'email': 'aa@bb.cc',
                                          'password1': 'pwd123456',
                                          'password2': 'pwd123456'})
        self.assertRedirects(response, reverse_lazy("hasker_app:index"))


class CustomLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('pwd123456')
        self.user.save()

    def test_get(self):
        response = self.client.get(reverse('hasker_app:login'))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('registration/login.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_post_redirect(self):
        response = self.client.post(reverse_lazy('hasker_app:login'),
                                    data={'username': 'testuser', 'password': 'pwd123456'})
        self.assertRedirects(response, reverse_lazy("hasker_app:index"))


class ChangeProfileView(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('pwd123456')
        self.user.save()
        self.userprofile = UserProfile.objects.create(user=self.user)

    def test_not_auth_user_redirect(self):
        response = self.client.get(reverse_lazy("hasker_app:settings"))
        self.assertRedirects(response, "".join([str(reverse_lazy("hasker_app:login")),
                                                "?next=",
                                                str(reverse_lazy("hasker_app:settings"))]))

    def test_auth_user_get(self):
        self.client.login(username='testuser', password='pwd123456')
        response = self.client.get(reverse('hasker_app:settings'))
        self.assertEqual(response.status_code, 200)
        template_names = [template.name for template in response.templates]
        self.assertIn('base.html', template_names)
        self.assertIn('registration/settings.html', template_names)
        self.assertIn('navbar.html', template_names)
        self.assertIn('sidebar.html', template_names)
        self.assertIsInstance(response.context['user_form'], ChangeProfileForm)
        self.assertIsInstance(response.context['user_profile_form'], UserProfileForm)
        self.assertEqual(response.context['user_form'].instance, self.user)
        self.assertEqual(response.context['user_profile_form'].instance, self.userprofile)

    def test_post_redirect(self):
        self.client.login(username='testuser', password='pwd123456')
        response = self.client.post(reverse_lazy('hasker_app:settings'),
                                    data={'email': 'aa@bb.cc'})
        self.assertRedirects(response, reverse_lazy("hasker_app:index"))


class LogoutTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('hasker_app:logout'))
        self.assertRedirects(response, reverse_lazy("hasker_app:index"))
