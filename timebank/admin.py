from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from timebank.models import (
        Account,
        AccountTransaction,
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    pass

