# Generated by Django 3.0.6 on 2020-07-26 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0002_auto_20200710_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdrawalrequest',
            name='user',
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
        migrations.DeleteModel(
            name='WithdrawalRequest',
        ),
    ]
