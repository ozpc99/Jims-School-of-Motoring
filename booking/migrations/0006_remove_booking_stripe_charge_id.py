# Generated by Django 3.2.23 on 2024-02-21 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_booking_stripe_charge_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='stripe_charge_id',
        ),
    ]
