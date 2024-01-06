# Формы для работы с аккаунтом
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    """ Форма аутентификации пользователя в БД """
    username = forms.CharField(label='Имя пользователя')  # имя пользователя
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')  # пароль с настройкой ввода


class UserRegistrationForm(forms.ModelForm):
    """ Модельная форма регистрации пользователя """
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        """Валидация введённого пароля (проверка, что оба одинаковы)"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        else:
            return cd['password2']

    def clean_email(self):
        """Проверка (валидация) адреса электронной почты на уникальность"""
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Электронная почта уже используется')
        return data


class UserEditForm(forms.ModelForm):
    """
    Позволит пользователям редактировать свое имя,
    фамилию и адрес электронной почты,
    которые являются атрибутами встроенной в Django модели User
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """Проверка (валидация) адреса электронной почты на уникальность"""
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Электронная почта уже используется')
        return data


class ProfileEditForm(forms.ModelForm):
    """
    Позволит пользователям редактировать данные профиля,
    сохраненные в конкретно-прикладной модели Profile
    """

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
