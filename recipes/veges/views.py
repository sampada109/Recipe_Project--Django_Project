from django.shortcuts import render, redirect
from .models import *

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