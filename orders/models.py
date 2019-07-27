from django.db import models
from django.contrib.auth import get_user_model


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
