from django.shortcuts import render, redirect
from .models import User, Task
from datetime import date
import bcrypt, re

from django.contrib import messages
def index(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    messages.success(request,"User Successfully created!")
    request.session['user_id'] = new_user.id
    return redirect('/welcome')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/') 
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/welcome')

    return redirect('/')
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    messages.success(request,"User Successfully created!")
    request.session['user_id'] = new_user.id
    return redirect('/welcome')
def welcome(request):
    if 'user_id' in request.session:
        logged_in_user = User.objects.get(id=request.session['user_id'])
        all_tasks = Task.objects.all()
        user_tasks = logged_in_user.tasks_uploaded
        today_date = date.today()
        daily_score =0
        for task in all_tasks:
            if task.day_completed== today_date and task.completed_by == logged_in_user:
                daily_score = daily_score + 1
        context = {
        'logged_in_user': logged_in_user,
        'all_tasks' : all_tasks,
        'daily_score': daily_score,
        'today_date': today_date,
        'user_tasks': user_tasks
        }
        return render(request,'welcome.html',context)
def addtask(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    all_tasks = Task.objects.all()
    new_task = Task.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        day_completed = request.POST['day_completed'],
        time_spent = request.POST['time_spent'],
        completed_by = logged_in_user
    )
    logged_in_user.score +=1 
    logged_in_user.save()

    context = {
        'logged_in_user' : logged_in_user,
        'all_tasks': all_tasks
    }
    return redirect('/welcome')
def new_account(request):
    return render(request,'register.html')

def logout(request):
    request.session.clear()
    return redirect('/')