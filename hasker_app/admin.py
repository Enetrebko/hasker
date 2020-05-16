from django.contrib import admin
from .models import Question, Answer, UserProfile
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
