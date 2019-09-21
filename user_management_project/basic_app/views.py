from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def user_login(request):
    #check if the form has been submitted
    if request.method == 'POST':
        #get the data from the form
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        #authenticate the user
        user = authenticate(username=uname, password=passw)
        #check if the user is autheticated or not
        if user:
            #check if the user is an active user
            if user.is_active:
                #user is autheticated & active
                #print("user is autheticated & active")
                #login the user - activate the login status of the user
                login(request, user)
                #print("user logged in")
                #redirect the user to the post login Page
                #return HttpResponseRedirect('URL')
                #or
                #return HttpResponseRedirect(reverse('URL_Name'))
                return HttpResponseRedirect(reverse('userhome'))
            else:
                #user is autheticated & inactive
                #print("user is autheticated & inactive")
                #display some message on the screen
                return HttpResponse("<h1>User Inactive!</h1>")
        else:
            #print("Unauthenticated Login attempt!")
            #display some message on the screen
            #return HttpResponse("<h1>User Unauthenticated!</h1>")
            return render(request,'basic_app/login.html',{'err':'Invalid User Credentials!'})

    else:
        return render(request,'basic_app/login.html')

@login_required
def userhome(request):
    return render(request, 'basic_app/userhome.html')

@login_required
def userlogout(request):
    #logout the user programatically
    logout(request)
    #redirect the user
    return HttpResponseRedirect(reverse('login'))

def register(request):

    registered = False

    if request.method == 'POST':
        #form submitted
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        #check form validity
        if user_form.is_valid() and profile_form.is_valid():
            #form is valid

            #save the user_form
            user = user_form.save()
            #hash the password
            user.set_password(user.password)
            #save
            user.save()

            #save the profile_form - but do not commit the changes as yet as the file & other data is not present
            profile = profile_form.save(commit=False)
            #set the profile's user
            profile.user = user

            #update profile_pic
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            #finally save the profile form
            profile.save()

            registered=True
        else:
            #form is invalid
            print(user_form.errors)
            print(profile_form.errors)
    else:
        #1st time load
        #create empty forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,'basic_app/register.html',
    {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'registered' : registered
    })
