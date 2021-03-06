from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from . import forms
from . import models
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings


class AskQuestionView(LoginRequiredMixin, View):

    form = forms.AskQuestionForm
    login_url = reverse_lazy('hasker_app:login')
    template_name = 'ask_question.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            tags_request = form.cleaned_data.pop('tags')
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            for tag_request in tags_request:
                tag, _ = models.Tag.objects.get_or_create(tag_text=tag_request.strip())
                tag.save()
                question.tags.add(tag)
            return redirect(reverse_lazy('hasker_app:question', kwargs={'pk': question.pk}))
        return render(request, self.template_name, context={"form": form})


class QuestionView(ListView):
    paginate_by = 20
    form = forms.AnswerForm
    template_name = 'question.html'
    email_header = 'New answer'
    email_body = '''You've got new answer: '''

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(models.Question, pk=self.kwargs['pk'])
        answers = models.Answer.objects.filter(question=question).order_by('-votes', '-created_date')
        context = self.get_context_data(object_list=answers)
        context['form'] = self.form()
        context['question'] = question
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwarg):
        question = get_object_or_404(models.Question, pk=self.kwargs['pk'])
        form = self.form(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            question = question
            question.answers += 1
            question.save()
            send_mail(
                self.email_header,
                "".join([self.email_body, request.build_absolute_uri(question.get_absolute_url())]),
                settings.EMAIL_HOST_USER,
                [question.user.email],
                fail_silently=False,)
        return redirect(reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))


class IndexView(ListView):
    model = models.Question
    paginate_by = 30
    template_name = 'index.html'

    def get_ordering(self):
        ordering = self.kwargs.get('orderby', '-created_date')
        return ordering


@login_required(login_url=reverse_lazy('hasker_app:login'))
def vote(request, object_type, obj_id, vote_up):
    objects = {
        'answer': models.Answer,
        'question': models.Question,
    }
    request_object = get_object_or_404(objects[object_type], pk=obj_id)
    question = request_object if object_type == 'question' else request_object.question
    already_voted_up = request_object.users_voted_up.filter(id=request.user.id).exists()
    already_voted_down = request_object.users_voted_down.filter(id=request.user.id).exists()
    if vote_up:
        if already_voted_down:
            request_object.votes += 1
            request_object.users_voted_down.remove(request.user)
        elif not already_voted_up:
            request_object.votes += 1
            request_object.users_voted_up.add(request.user)
    else:
        if already_voted_up:
            request_object.votes -= 1
            request_object.users_voted_up.remove(request.user)
        elif not already_voted_down:
            request_object.votes -= 1
            request_object.users_voted_down.add(request.user)
    request_object.save()
    return redirect(reverse_lazy('hasker_app:question', kwargs={'pk': question.id}))


@login_required(login_url=reverse_lazy('hasker_app:login'))
def mark_correct_answer(request, question_id, answer_id):
    question = get_object_or_404(models.Question, pk=question_id)
    if question.user == request.user:
        answer = get_object_or_404(models.Answer, pk=answer_id)
        question.correct_answer = answer
        question.save()
    return redirect(reverse_lazy('hasker_app:question',
                                 kwargs={'pk': request.resolver_match.kwargs['question_id']}))


class SearchResultsView(ListView):
    model = models.Question
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q').strip()
        if query.startswith('tag:'):
            query_tag = query.replace('tag:', '').strip()
            object_list = models.Question.objects.filter(tags__tag_text=query_tag)
        else:
            object_list = models.Question.objects.filter(
                Q(header__icontains=query) | Q(body__icontains=query)
            )
        return object_list.order_by('-votes', '-created_date')


class SignUpView(View):

    user_form = forms.SignUpForm
    user_profile_form = forms.UserProfileForm
    template_name = 'registration/signup.html'

    def get(self, request):
        user_form = self.user_form()
        user_profile_form = self.user_profile_form()
        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "user_profile_form": user_profile_form})

    def post(self, request):
        user_form = self.user_form(request.POST)
        user_profile_form = self.user_profile_form(request.POST, request.FILES)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user_id = user_form.instance.id
            user_profile.save()
            username, password = user_form.cleaned_data.get('username'), user_form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password)
            login(self.request, new_user)
            return redirect(reverse_lazy('hasker_app:index'))
        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "user_profile_form": user_profile_form})


class CustomLoginView(LoginView):
    authentication_form = forms.CustomAuthenticationForm


class ChangeProfileView(LoginRequiredMixin, View):

    user_form = forms.ChangeProfileForm
    user_profile_form = forms.UserProfileForm
    login_url = reverse_lazy('hasker_app:login')
    template_name = 'registration/settings.html'

    def get(self, request):
        user_form = self.user_form(instance=request.user)
        user_profile_form = self.user_profile_form(instance=request.user.userprofile)
        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "user_profile_form": user_profile_form})

    def post(self, request):
        user_form = self.user_form(request.POST, instance=request.user)
        user_profile_form = self.user_profile_form(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect(reverse_lazy('hasker_app:index'))
        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "user_profile_form": user_profile_form})
