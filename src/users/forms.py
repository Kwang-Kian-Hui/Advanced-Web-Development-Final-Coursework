from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

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
        except User.DoesNotExist:
            # exception is thrown if no matching objects found
            return email
        raise forms.ValidationError(f"{email} is already in use. Please use another email.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            # exception is thrown if no matching object found
            return username
        raise forms.ValidationError(f"{username} is already in use. Please use another username.")

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def save(self, request):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Your email or password is incorrect.")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'profile_img')
    
    # clean functions
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # exception is thrown if no matching objects found
            return email
        raise forms.ValidationError(f"{email} is already in use. Please use another email.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            # exception is thrown if no matching object found
            return username
        raise forms.ValidationError(f"{username} is already in use. Please use another username.")

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.profile_img = self.cleaned_data['profile_img']
        if commit:
            user.save()
        return user