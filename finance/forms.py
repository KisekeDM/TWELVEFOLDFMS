from django import forms
from .models import Contribution
from .models import Loan
from .models import Repayment
from .models import Fine

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
        fields = ['member', 'is_on_behalf', 'beneficiary', 'principal_amount', 'duration_months', 'issue_date']

        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'is_on_behalf': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'beneficiary': forms.Select(attrs={'class': 'form-select'}),
            'principal_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount (KES)'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['amount', 'date_paid']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount (KES)'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['member', 'amount', 'reason', 'date_issued', 'is_paid']

        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 100.00'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Late Arrival'}),
            'date_issued': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReportFilterForm(forms.Form):
    MONTH_CHOICES = [
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ]
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    year = forms.IntegerField(initial=2026, widget=forms.NumberInput(attrs={'class': 'form-control'}))