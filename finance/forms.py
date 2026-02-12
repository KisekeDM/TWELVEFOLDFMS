from django import forms
from .models import Contribution
from .models import Loan

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['member', 'amount', 'month_paid_for', 'date']

        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500.00'}),
            'month_paid_for': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['member', 'principal_amount', 'duration_months', 'issue_date']

        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'principal_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter amount (KES)'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }