from django.shortcuts import render,reverse
# Login imports
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Http imports
from django.http import HttpResponse,HttpResponseRedirect
# Models and Forms import
from .forms import User_Form
from django.contrib.auth.models import User
from .models import student_res
# Error message import
from django.contrib import messages

# Create your views here.
def SignUp(request):
    form = User_Form()
    if request.method == 'POST':
        form = User_Form(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'authorization/signup.html',{'form':form})

def student_register(request):
    form = User_Form()
    if request.method == "POST":
        form = User_Form(request.POST)
        phone = request.POST['phone']
        std = request.POST['class']
        if form.is_valid():
            user = form.save(commit=True)
            sa = student_res(user=user,phone=phone, std=std)
            user.save()
            sa.save()
        return HttpResponseRedirect(reverse('exam:test_list'))
    return render(request,'authorization/student_signup.html',{'form':form})

def LoginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('exam:test_list'))
            else:
                return HttpResponse('User is not active')
        else:
            messages.error(request,"Username or Password is incorrect")
            return HttpResponseRedirect('/authorize/login/')
    return render(request,'authorization/login.html')

@login_required
def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect('/authorize/login/')



