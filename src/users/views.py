from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from users.forms import UserRegistrationForm

def registration_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return HttpResponse(f"You are already logged in as {user.email}.")
    context = {}

    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            # redirect(path_name) as defined in urls.py
            return redirect("home")
        else:
            context['registration_form'] = form
    return render(request, 'users/register.html', context)