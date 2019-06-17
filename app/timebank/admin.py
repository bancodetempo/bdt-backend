from django.contrib import admin

from timebank.models import Account, AccountTransaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    pass
