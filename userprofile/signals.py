from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from .models import UserProfile

THEORY_TEST_CENTERS = (
    ("Alnwick", "Alnwick"),
    ("Bishop Auckland", "Bishop Auckland"),
    ("Hexham", "Hexham"),
    ("Middlesbrough", "Middlesbrough"),
    ("Newcastle", "Newcastle"),
    ("Sunderland", "Sunderland"),
)

PRACTICAL_TEST_CENTERS = (
    ("Blyth", "Blyth"),
    ("Darlington", "Darlington"),
    ("Durham", "Durham"),
    ("Gateshead", "Gateshead"),
    ("Gosforth", "Gosforth"),
    ("Hartlepool", "Hartlepool"),
    ("Hexham", "Hexham"),
    ("Middlesbrough", "Middlesbrough"),
    ("Sunderland", "Sunderland"),
)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)