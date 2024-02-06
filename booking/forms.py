from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('full_name', 'email',
                  'lesson_type', 'lesson_date', 'lesson_time',
                  'house_no', 'street',
                  'town', 'post_code',
                  'billpayer_name',
                  'billpayer_house_no',
                  'billpayer_street',
                  'billpayer_town',
                  'billpayer_post_code',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels
        and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email',
            'lesson_type': 'Lesson Type',
            'lesson_date': 'Date',
            'lesson_time': 'Time',
            'house_no': 'House Name/No.',
            'street': 'Street',
            'town': 'Town',
            'post_code': 'Post Code',
            'billpayer_name': 'Cardholder Name',
            'billpayer_house_no': 'Billing Address House Name/No.',
            'billpayer_street': 'Billing Address Street',
            'billpayer_town': 'Billing Address Town/City',
            'billpayer_post_code': 'Billing Address Post Code',
        }
        
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False