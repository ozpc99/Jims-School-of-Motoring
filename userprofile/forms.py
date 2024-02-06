from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone',
            'license_no',
            'license_expiry',
            'home_house_no',
            'home_street',
            'home_town',
            'home_post_code',
            'theory_test_date',
            'theory_test_center',
            'mock_test_date',
            'mock_test_address',
            'practical_test_date',
            'practical_test_center',
        ]
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
            'theory_test_date': forms.DateInput(attrs={'type': 'date'}),
            'mock_test_date': forms.DateInput(attrs={'type': 'date'}),
            'practical_test_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UpdateNameForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['first_name', 'last_name']

class UpdatePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['phone']

class UpdateHomeAddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = [
            'home_house_no',
            'home_street',
            'home_town',
            'home_post_code',
        ]

class UpdateLicenseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['license_no', 'license_expiry']

class UpdateTheoryTestForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['theory_test_date', 'theory_test_center']

class UpdatePracticalTestForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['practical_test_date', 'practical_test_center']