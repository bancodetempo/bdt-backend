# Generated by Django 2.2.15 on 2020-08-20 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20200820_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='google_drive_spreadsheet_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]