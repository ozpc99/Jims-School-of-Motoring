# Generated by Django 3.2.23 on 2024-02-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='lesson_price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]