from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'google_drive_spreadsheet_id', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'google_drive_spreadsheet_id', 'first_name', 'last_name'),
        }),
    )
    ordering = ('date_joined',)
    list_display = ('email', 'first_name', 'last_name',
                    'google_drive_spreadsheet_id', 'is_staff', 'date_joined',)
    search_fields = ('first_name', 'last_name', 'email',
                     'google_drive_spreadsheet_id')


admin.site.register(CustomUser, CustomUserAdmin)
