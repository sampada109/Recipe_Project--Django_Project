from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User     #user model
from django.contrib import messages           # for flashing messages
from django.contrib.auth import authenticate, login , logout   # for user authentication , mantaining login sessions, logout session
from django.contrib.auth.decorators import login_required      #login required for users page as it will prevent anyone to access the users page

# Create your views here.


def home(request):
    user = User.objects.all()
    top_rated_recipes = recipes.objects.order_by('-ratings')[:3]    #25
    popular_recipes = recipes.objects.order_by('-views')[:3]
    recently_added_recipes = recipes.objects.order_by('-recp_create_date')[:3]
    return render(request, 'home.html', {'user':user, 'top_rated_recipes': top_rated_recipes, 
                                          'popular_recipes': popular_recipes, 
                                          'recently_added_recipes': recently_added_recipes})    #4th commit adding function for home page



def filter_recipes(request, filter_type):     #26
    user = User.objects.all()
    if filter_type == 'breakfast':
        filtered = recipes.objects.filter(category__category = 'Breakfast')
    elif filter_type == 'lunch':
        filtered = recipes.objects.filter(category__category = 'Lunch')  
    elif filter_type == 'dinner':
        filtered = recipes.objects.filter(category__category = 'Dinner')  
    elif filter_type == 'rated':
        filtered = recipes.objects.order_by('-ratings')  
    elif filter_type == 'popular':
        filtered = recipes.objects.order_by('-views')  
    elif filter_type == 'recent':
        filtered = recipes.objects.order_by('-recp_create_date')  
    else:
        filtered = recipes.objects.none()    

    return render(request, 'filter_recipe.html', {'user':user, 'filtered':filtered, 'filter_type':filter_type})




@login_required(login_url="/user_login/")     #20th   preventing users page from indirect access
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


@login_required(login_url="/user_login/")     #21th   preventing users page from indirect access
def delete_recp(request, id):
    queryset = recipes.objects.get(id = id)
    queryset.delete()
    return redirect('/user/')



@login_required(login_url="/user_login/")     #21th   preventing users page from indirect access
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


def user_logout(request):    #18th
    logout(request)
    return redirect('/')


def user_login(request):
    if request.method == 'POST':         #17th
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username):     #check if username exist or not
            messages.error(request, 'username does not exist!')   #if not exist
            return redirect('/user_login/')
        
        user = authenticate(username = username , password = password)   # authenticate if username with coorect password

        if user is None:
            messages.error(request, 'Invalid password!')   #if username and password does not match
            return redirect('/user_login/')
        else:
            login(request, user)    #if user has correct password then login user and mantain session
            return redirect('/user/')


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




def user_profile(request):
    return render(request, 'user_profile.html')