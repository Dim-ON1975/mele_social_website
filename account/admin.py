from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Профиль пользователя на сайте администрирования """
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']
