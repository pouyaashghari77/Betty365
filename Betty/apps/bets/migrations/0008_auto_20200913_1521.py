# Generated by Django 3.0.6 on 2020-09-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0007_auto_20200913_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='selection',
            field=models.CharField(choices=[('Home', 'Home'), ('Home', 'Away')], max_length=4, verbose_name='Selection'),
        ),
        migrations.AlterField(
            model_name='bet',
            name='side',
            field=models.CharField(choices=[('Back', 'Back'), ('Lay', 'Lay')], max_length=4, verbose_name='Side'),
        ),
    ]
