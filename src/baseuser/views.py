from django.shortcuts import render

# Create your views here.
def home_page(request, *args, **kwargs):
    context = {}
    return render(request, "baseuser/homepage.html", context)