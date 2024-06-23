from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def login_page(request):

    if request.method == 'POST':
        email : str = request.POST.get('email')
        password = request.POST.get('password')

        # Check kya hai user pehle se exist keta hai k nhi

        user_obj = User.objects.filter(username = email)

        # Aghr user exist kerta hai tu (condition lgaye hai)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verfied.')
            return HttpResponseRedirect(request.path_info)


        # Check username and password is correct or not
        user_obj = authenticate(username = email, password= password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        # User create hone k bad hum ise ek successful message dikhaye gy
        messages.warning(request, 'Invalid Credentials.')
        # Again redirect kerwa dy gy same page pr
        return HttpResponseRedirect(request.path_info)






    return render(request, 'accounts/login.html')

def register_page(request):
    # get kare ga email, passsword, first_name, last_name from user (register wale page ma hune name=first_name rakh hai or baki bhi ase hi name k sath get kya hai)

    if request.method == 'POST':
        first_name: str = request.POST.get('first_name')
        last_name : str = request.POST.get('last_name')
        email : str = request.POST.get('email')
        password = request.POST.get('password')

        # Check kya hai user pehle se exist keta hai k nhi

        user_obj = User.objects.filter(username = email)

        # Aghr user exist kerta hai tu (condition lgaye hai)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        
        # aghr user na ho tu create kare ga
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username= email)
        user_obj.set_password(password)
        user_obj.save()

        # User create hone k bad hum ise ek successful message dikhaye gy
        messages.success(request, 'An email has been sent on your mail.')
        # Again redirect kerwa dy gy same page pr
        return HttpResponseRedirect(request.path_info)



    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')

    except Exception as e:
        return HttpResponse('Invalid Email Token')
