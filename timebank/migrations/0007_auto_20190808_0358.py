# Generated by Django 2.2.3 on 2019-08-08 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timebank', '0006_accounttransaction_balance_after_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='uid',
        ),
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='timebank.Account', verbose_name='Conta'),
        ),
    ]
