from django.contrib import admin

from timebank.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
