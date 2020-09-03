from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('requester', 'description',
                    'grantor', 'order_price', 'status')
    actions = ['confirm_orders']

    def confirm_orders(self, request, queryset):
        for order in queryset:
            uid = order.uid
            Order.confirm_order(uid)
    confirm_orders.short_description = "Confirmar pedidos de troca de horas selecionados"
