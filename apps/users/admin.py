from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserProfile


class UsersAdmin(UserAdmin):
    pass


admin.site.register(UserProfile, UsersAdmin)
