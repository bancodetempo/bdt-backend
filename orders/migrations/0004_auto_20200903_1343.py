# Generated by Django 3.1 on 2020-09-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Efetuado')], default=0, verbose_name='Status do pedido'),
        ),
    ]
