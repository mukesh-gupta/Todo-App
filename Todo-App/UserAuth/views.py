from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages
# Create your views here.

def signup(request):
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if request.POST['password1'] == request.POST['password2']:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('signup')
                else:

                    user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                                    last_name=last_name, email=email)
                    user.save()
                    messages.info(request,f'{username.capitalize()} Registered successfully !')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid Password')
                return render(request, 'UserAuth/signup.html')

        else:
            return render(request, 'UserAuth/signup.html')

def MartLogin(request):
    if request.method=="GET":
        return render(request,'UserAuth/login.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            messages.success(request, 'successfully logged in !')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Username and Password ')
            return render(request, 'UserAuth/login.html', {'form': AuthenticationForm()})

def MartLogout(request):
        user=request.user
        logout(request)
        messages.success(request,f'{user} successfully logged Out !')
        return redirect('users')




