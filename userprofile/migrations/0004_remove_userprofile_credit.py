# Generated by Django 3.2.23 on 2024-02-20 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_userprofile_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='credit',
        ),
    ]