from django.db.utils import Error
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import requests
meal_api_url = "https://www.themealdb.com/api/json/v1/1/random.php"
from django.contrib import messages
from .models import *
import re, bcrypt

# Create your views here.
def index(request):
    r = requests.get(meal_api_url)
    r = r.json()
    meals = r['meals']
    context = {
        "meals" : meals
    }
    print(r['meals'])
    return render(request,'index.html',context)

def sign_in(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.authenticate(email, password):
            messages.error(request, 'Email and Password do not match')
            return redirect("/")
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        return redirect("/home")
    return redirect('/home')

def protected(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
        "user": user,
        
        }
        return render(request, 'account-notes.html', context)
    else: 
        messages.error(request, 'You must be logged in to do that')
        return redirect("/home")

    
def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validation(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
    return redirect('/home')
    

def dashboard(request):
    context = {
        'favorites': Favorites.objects.all()
    }
    return render (request, 'favorites.html', context)
    
def home(request):
    r = requests.get(meal_api_url)
    r = r.json()
    meals = r['meals']
    context = {
        "meals" : meals
    }
    return render(request,'recipe.html', context)

def add_to_fave(request):
    return render(request,'add-to-fave.html')

def create(request):
    Favorites.objects.create(
        title = request.POST['title'],
        category = request.POST['category'],
        instructions = request.POST['instructions'],
        ingredients = request.POST['ingredients'],
    
    )
    return redirect('/dashboard')

def edit(request,id):
    fave_to_edit = Favorites.objects.get(id=id)
    fave_to_edit.save()
    return render(request, 'edit.html')


def delete(request,id):
    
    fave_to_delete = Favorites.objects.get(id=id)
    fave_to_delete.delete()
    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')  

def back(request):
    request.session.clear()
    return redirect('/home')  


#def user_account(request, user_id):
    if 'user_id' not in request.session:
        #return redirect('/notes')
        context = {
            'user_account': User.objects.get(id=user_id)
        }
    return render(request, 'account-notes.html', context)
