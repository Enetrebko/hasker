from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class Question(models.Model):
    header = models.TextField(max_length=300)
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)
    answers = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    users_voted_up = models.ManyToManyField(User, related_name='questions_voted_up', blank=True)
    users_voted_down = models.ManyToManyField(User, related_name='questions_voted_down', blank=True)
    correct_answer = models.OneToOneField('Answer',
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name='correct_answer_set')

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('hasker_app:question', kwargs={'pk': self.pk})


class Tag(models.Model):
    tag_text = models.TextField(null=True)

    def __str__(self):
        return self.tag_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0)
    users_voted_up = models.ManyToManyField(User, related_name='answers_voted_up', blank=True)
    users_voted_down = models.ManyToManyField(User, related_name='answers_voted_down', blank=True)

    def __str__(self):
        return self.body


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='pictures/', blank=True)

    @property
    def image_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.STATIC_URL + 'img/default.jpeg'
