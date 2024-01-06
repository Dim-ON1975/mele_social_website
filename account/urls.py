from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Предыдущий url входа
    # path('login/', views.user_login, name='login')

    # url-адреса входа и выхода
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # url-адреса смены пароля:
    # работа с формой для смены пароля
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # сообщение об успехе смены пароля пользователем
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # url-адреса сброса пароля:
    # сброс пароля
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # сообщение о том, что было отправлено электронное письмо с ссылкой для сброса пароля
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # позволяет пользователю установить новый пароль
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # страница об успехе, на которую перенаправляется пользователь после сброса пароля
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # аутентификация, включая смену и замену пароля
    path('', include('django.contrib.auth.urls')),
    # информационная панель
    path('', views.dashboard, name='dashboard'),
    # регистрация пользователей
    path('register/', views.register, name='register'),
    # редактирование профиля
    path('edit/', views.edit, name='edit')
]
