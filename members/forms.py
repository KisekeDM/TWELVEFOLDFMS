from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'monthly_contribution_amount', 'date_joined']

        # We use 'widgets' to add Bootstrap classes to the input fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '07XX XXX XXX'}),
            'monthly_contribution_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }