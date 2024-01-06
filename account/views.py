from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


def user_login(request):
    """ Базовое представление входа пользователя в систему """
    if request.method == "POST":
        form = LoginForm(request.POST)  # экземпляр формы с переданными данными
        if form.is_valid():  # форма валидна: заполнены корректно все поля
            cd = form.cleaned_data
            # Аутентификация пользователя и возвращение объекта User
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                # Проверка статуса пользователя
                if user.is_active:
                    login(request, user)  # задаём пользователя в текущем сеансе
                    return HttpResponse('Аутентификация выполнена успешно')
                else:
                    return HttpResponse('Отключенная учётная запись')
            else:
                return HttpResponse('Недопустимый логин и/или пароль')
    else:
        # Если GET, то создаётся экземпляр новой формы входа.
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    Представление dashboard и применили к нему декоратор login_required
    из фреймворка аутентификации. Декоратор login_required проверяет
    аутентификацию текущего пользователя.
    """
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    """
    Представление создания учётных записей пользователей.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль, хэшируя его
            # при помощи метода .set_password перед сохранением в БД.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлён успешно')
        else:
            messages.error(request, 'Ошибка при обновлении профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})

