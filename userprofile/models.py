from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)

    phone = models.CharField(max_length=15, null=True, blank=True)

    license_no = models.CharField(max_length=25, null=True, blank=True)
    license_expiry = models.DateField(default=None, blank=True, null=True)

    home_house_no = models.CharField(max_length=40, null=True, blank=True)
    home_street = models.CharField(max_length=100, null=True, blank=True)
    home_town = models.CharField(max_length=40, null=True, blank=True)
    home_post_code = models.CharField(max_length=7, null=True, blank=True)

    theory_test_date = models.DateTimeField(default=None, blank=True, null=True)
    theory_test_center = models.CharField(choices=THEORY_TEST_CENTERS, max_length=100, null=True, blank=True)

    mock_test_date = models.DateTimeField(default=None, blank=True, null=True)
    mock_test_address = models.TextField(null=True, blank=True)
    
    practical_test_date = models.DateTimeField(default=None, blank=True, null=True)
    practical_test_center = models.CharField(choices=PRACTICAL_TEST_CENTERS, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'