from django.shortcuts import render

# Create your views here.
def home_page(request, *args, **kwargs):
    context = {}
    return render(request, "base/homepage.html", context)