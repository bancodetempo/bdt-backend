# Generated by Django 2.2.3 on 2019-08-03 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timebank', '0003_auto_20190723_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.Order'),
        ),
    ]
