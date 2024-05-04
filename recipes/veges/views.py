from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User     #user model
from django.contrib import messages           # for flashing messages

# Create your views here.


def home(request):
    return render(request, 'home.html')    #4th commit adding function for home page


def users(request):
    if request.method == 'POST':
        data = request.POST
        recp_img = request.FILES.get('recp_img')
        recp_name = data.get('recp_name')
        recp_desp = data.get('recp_desp')
        # print(recp_name, recp_desp, recp_img)

        # adding to data model
        recipes.objects.create(
            recp_name = recp_name,
            recp_desp = recp_desp,
            recp_img = recp_img
        )

        return redirect('/user/')
    
    queryset = recipes.objects.all()
    context = {'recipes': queryset}
    
    return render(request, 'user.html' , {'recipes': queryset})    #5th commit adding users page



def delete_recp(request, id):
    queryset = recipes.objects.get(id = id)
    queryset.delete()
    return redirect('/user/')


def update_recp(request, id):
    queryset = recipes.objects.get(id = id)
    context = {'update_recipe': queryset}

    if request.method == 'POST':
        data = request.POST
        recp_img = request.FILES.get('recp_img')
        recp_name = data.get('recp_name')
        recp_desp = data.get('recp_desp')

        queryset.recp_name = recp_name
        queryset.recp_desp = recp_desp

        if recp_img:
            queryset.recp_img = recp_img

        queryset.save()    
        return redirect('/user/')

    return render(request, 'update.html', {'update_recipe': queryset})


def user_login(request):
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, 'username already exists!')
            return redirect('/user_signup/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)   #for encrypting the password (hash password)

        user.save()

        messages.success(request, 'Your account has been created successfully. You may now login!')

        return redirect('/user_login/')

    return render(request, 'signin.html')