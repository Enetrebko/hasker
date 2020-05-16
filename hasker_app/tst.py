class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login', }),
        max_length=30, label=u'Логин'
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта', }),
        required=True, max_length=254, label=u'E-mail',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*****'}),
        min_length=6, label=u'Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*****'}),
        min_length=6, label=u'Повторите пароль'
    )
    avatar = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'ask-signup-avatar-input', }),
        required=False, label=u'Аватар'
    )

    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2", "avatar"]
