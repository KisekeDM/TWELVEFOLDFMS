from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmailRegistrationForm(UserCreationForm):
    # Make email a required field on the form
    email = forms.EmailField(required=True, help_text='Required. We will use this to log you in and reset your password.')

    class Meta(UserCreationForm.Meta):
        model = User
        # Ask for username (for display purposes) and email
        fields = ('username', 'email')