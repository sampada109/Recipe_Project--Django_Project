from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')    #4th commit adding function for home page


def users(request):
    return render(request, 'user.html')    #5th commit adding users page