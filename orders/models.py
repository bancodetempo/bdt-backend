import uuid

from django.db import models, transaction
from django.contrib.auth import get_user_model

from timebank.models import Account


class Order(models.Model):

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    STATUS_PENDING = 0
    STATUS_CONFIRMED = 1

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendente'),
        (STATUS_CONFIRMED, 'Efetuado'),
    )
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Identificador Público'
    )
    requester = models.ForeignKey(
        get_user_model(),
        verbose_name='Solicitante',
        on_delete=models.PROTECT,
        related_name='requester',
    )
    grantor = models.ForeignKey(
        get_user_model(),
        verbose_name='Concedente',
        on_delete=models.PROTECT,
        related_name='grantor',
    )
    description = models.CharField(
        max_length=240,
        verbose_name='Descrição',
    )
    order_price = models.DecimalField(
        verbose_name='Valor da troca',
        decimal_places=1,
        max_digits=5,
        help_text='Valor da troca',
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        verbose_name='Status do pedido',
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        price = self.order_price
        description = self.description
        requester = str(self.requester)
        grantor = str(self.grantor)

        exhibition = '{} solicitou {} de {}'.format(requester, description, grantor)

        return exhibition

    @classmethod
    def confirm_order(cls, order_uid):
        with transaction.atomic():
            order = cls.objects.select_for_update().get(uid=order_uid)
            order_price = order.order_price
            order.status = cls.STATUS_CONFIRMED
            order.save()
            requester = order.requester
            grantor = order.grantor

            Account.withdraw(requester, order_price)
            Account.deposit(grantor, order_price)



