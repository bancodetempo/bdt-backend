# Generated by Django 2.2.3 on 2019-08-03 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timebank', '0004_auto_20190803_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='reference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='orders.Order'),
        ),
    ]
