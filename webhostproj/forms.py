from django import forms
from django.core.validators import RegexValidator

class usersForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'  # ✅ Placeholder added
        })
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'  # ✅ Placeholder added
        })
    )

    phone = forms.CharField(
        max_length=15,
        label="Phone Number",
        validators=[
            RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone'  # ✅ Placeholder added
        })
    )
    
    
