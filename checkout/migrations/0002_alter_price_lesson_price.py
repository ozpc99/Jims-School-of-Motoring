# Generated by Django 3.2.23 on 2024-02-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='lesson_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, unique=True),
        ),
    ]
