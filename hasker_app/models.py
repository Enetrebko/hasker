from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    header = models.TextField(max_length=300)
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True, null=True)
    answers = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    users_voted = models.ManyToManyField(User, related_name='questions_voted', blank=True)
    correct_answer = models.OneToOneField('Answer',
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name='correct_answer_set')

    def __str__(self):
        return self.header


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
    users_voted = models.ManyToManyField(User, related_name='answers_voted', blank=True)

    def __str__(self):
        return self.body


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='pictures/', default='pictures/default.jpg')


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
