# Generated by Django 3.2.23 on 2024-02-20 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='stripe_charge_id',
            field=models.CharField(default='', max_length=254),
        ),
    ]