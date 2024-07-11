from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User     #user model
from django.contrib import messages           # for flashing messages
from django.contrib.auth import authenticate, login , logout   # for user authentication , mantaining login sessions, logout session
from django.contrib.auth.decorators import login_required      #login required for users page as it will prevent anyone to access the users page
from django.db.models import Q    # OR function

# Create your views here.


def home(request):
    user = User.objects.all()
    top_rated_recipes = recipes.objects.order_by('-ratings')[:3]    #25
    popular_recipes = recipes.objects.order_by('-views')[:3]
    recently_added_recipes = recipes.objects.order_by('-recp_create_date')[:3]
    return render(request, 'home.html', {'user':user, 'top_rated_recipes': top_rated_recipes, 
                                          'popular_recipes': popular_recipes, 
                                          'recently_added_recipes': recently_added_recipes})    #4th commit adding function for home page


#filtering recipes
def filter_recipes(request, filter_type):     #26
    user = User.objects.all()
    if filter_type == 'breakfast':
        filtered = recipes.objects.filter(category__category__iexact = 'Breakfast').order_by('-recp_last_modified_date')
    elif filter_type == 'lunch':
        filtered = recipes.objects.filter(category__category__iexact = 'Lunch').order_by('-recp_last_modified_date') 
    elif filter_type == 'dinner':
        filtered = recipes.objects.filter(category__category__iexact = 'Dinner').order_by('-recp_last_modified_date')  
    elif filter_type == 'rated':
        filtered = recipes.objects.order_by('-ratings')  
    elif filter_type == 'popular':
        filtered = recipes.objects.order_by('-views')  
    elif filter_type == 'recent':
        filtered = recipes.objects.order_by('-recp_create_date')  
    else:
        filtered = recipes.objects.none()    

    return render(request, 'filter_recipe.html', {'user':user, 'filtered':filtered, 'filter_type':filter_type})



#recipe detail page
def recipe_detail(request, id):        #27
    user = User.objects.all()
    recipe = recipes.objects.get(id = id)
    profile = Profile.objects.get(user = recipe.user)
    comment = comments.objects.filter(recipe=recipe).order_by('-com_date')
    return render(request,'recipe_detail.html', {'user':user, 'recipe':recipe, 'comment':comment, 'profile':profile})



#user profile page
def user_profile(request, username):
    user = User.objects.get(username = username)
    usr_profile = Profile.objects.get(user = user)
    recipe = recipes.objects.filter(user = user)

    return render(request, 'user_profile.html', {'user':user, 'usr_profile':usr_profile, 'recipe':recipe})



# edit user profile
@login_required(login_url="/user_login/")
def edit_profile(request, username):
    if request.user.username != username:       #only authorized user can have access
        return redirect('user_login')
    
    user = User.objects.get(username = username)
    user_profile = Profile.objects.get(user = user)

    if request.method == 'POST':
        data = request.POST
        profile_img = request.FILES.get('profile_img')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        if profile_img:
            user_profile.profile_img = profile_img

        user.save()
        user_profile.save()
        messages.success(request, 'Profile Edited successfully!')
        return redirect('user_profile', username=user.username)
    
    return render(request, 'edit_profile.html', {'user':user, 'user_profile':user_profile})


# edit password
@login_required(login_url="/user_login/")
def change_password(request, username):
    if request.user.username != username:       #only authorized user have access
        return redirect('user_login')
    
    user = User.objects.get(username = username)

    if request.method == 'POST':
        data = request.POST
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Check if current_password is correct
        if not user.check_password(current_password):
            messages.error(request, 'Your current password is Incorrect!')
            return redirect('change_password', username=user.username)
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password Changed successfully!')

        # Authenticate user with the new password and log in again
        user = authenticate(username=user.username, password=new_password)
        if user is not None:
            login(request, user)

        return redirect('user_profile', username=user.username)
    
    return render(request, 'edit_password.html')




#user page
@login_required(login_url="/user_login/")     #20th   preventing users page from indirect access
def users(request):
    if request.method == 'POST':
        data = request.POST
        recp_img = request.FILES.get('recp_img')
        recp_name = data.get('recp_name')
        recp_desp = data.get('recp_desp')
        recp_category_name = data.get('recp_catg')
        recp_tags = data.get('recp_tags')
        print(recp_name, recp_desp, recp_img, recp_category_name, recp_tags)

        tag_list = recp_tags.split(',')
        tag_list = [tag.strip() for tag in recp_tags.split(',')]
        print(tag_list)

        # Get or create the category
        ctg, created = recp_category.objects.get_or_create(category=recp_category_name)

        # adding to data model
        recipe = recipes.objects.create(
            user = request.user,
            recp_name = recp_name,
            recp_desp = recp_desp,
            recp_img = recp_img,
            category = ctg
        )
        for tag_name in tag_list:
            tg, created = Tags.objects.get_or_create(tag=tag_name)
            recipe.tags.add(tg)

        print('added--')

        return redirect('/user/')
    
    queryset = recipes.objects.filter(user = request.user)
    context = {'recipes': queryset}
    
    return render(request, 'user.html' , {'recipes': queryset})    #5th commit adding users page



#delete recipe 
@login_required(login_url="/user_login/")     #21th   preventing users page from indirect access
def delete_recp(request, id):
    queryset = recipes.objects.get(id = id)
    queryset.delete()
    return redirect('/user/')



#update recipe
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



#logout
def user_logout(request):    #18th
    logout(request)
    return redirect('/')


#login
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


#sign-in
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



# for search request 
def search_recipe(request):
    query = request.GET.get('search')
    print(query)
    if query != None:
        recipe_list = recipes.objects.filter(
            Q(recp_name__icontains=query) | 
            Q(recp_desp__icontains=query) | 
            Q(user__username__icontains=query) | 
            Q(tags__tag__icontains=query) | 
            Q(category__category__icontains=query)
        ).distinct()
    else:
        recipe_list = recipes.objects.all().order_by('-recp_last_modified_date')

    return render(request, 'search.html', {'recipe_list': recipe_list, 'query': query})