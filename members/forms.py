from django import forms
from .models import Member
from .models import Meeting


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'date_joined']

        # We use 'widgets' to add Bootstrap classes to the input fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '07XX XXX XXX'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'attendees']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. March Monthly Meeting'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # CheckboxSelectMultiple creates a list of checkboxes for the members
            'attendees': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input me-2'}),
        }