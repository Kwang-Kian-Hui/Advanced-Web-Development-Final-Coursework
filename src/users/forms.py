from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=40, help_text="Required. Add a valid email address.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    # clean functions
    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            # exception is thrown if no matching objects found
            return email
        raise forms.ValidationError(f"{email} is already in use. Please use another email.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except Exception as e:
            # exception is thrown if no matching object found
            return username
        raise forms.ValidationError(f"{username} is already in use. Please use another username.")