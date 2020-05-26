from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class MultiTagField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return [val.strip() for val in value.split(',') if len(val.strip()) > 0]


class AskQuestionForm(forms.ModelForm):

    tags = MultiTagField(required=False,
                         label='Tags',
                         help_text=_('Add up to 3 tags to describe what your question is about'),
                         widget=forms.Textarea(attrs={'placeholder': 'e.g. tag1, tag2, tag3',
                                                      'class': 'form-control', 'rows': 1}),
                         )

    class Meta:
        model = models.Question
        fields = ('header', 'body',)
        labels = {
            'header': 'Title',
        }
        help_texts = {
            'header': _('Be specific and imagine you’re asking a question to another person'),
            'body': _('Include all the information someone would need to answer your question')
        }
        widgets = {
            'header': forms.Textarea(attrs={'placeholder': 'e.g. How to python',
                                            'class': 'form-control', 'rows': 1}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if len(data) > 3:
            raise forms.ValidationError(_("Enter three tags or less"))
        return data


class AnswerForm(forms.ModelForm):

    class Meta:
        model = models.Answer

        fields = ('body',)
        labels = {
            'body': 'Your answer'
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


class SignUpForm(UserCreationForm):

    username = forms.CharField(label='Login',
                               max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               )

    email = forms.EmailField(label='Email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             )

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                )
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(label='Login',
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
                             )
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               )


class ChangeProfileForm(forms.ModelForm):

    email = forms.EmailField(label='Email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             )

    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        fields = ('avatar',)
