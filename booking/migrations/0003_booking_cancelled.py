# Generated by Django 3.2.23 on 2024-02-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_booking_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancelled',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
