from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Course1
from .forms import CreateCourseForm
from django.db.models.functions import Lower

#only logged in user can access certain pages
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'multipleuser/index.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'multipleuser/signupuser.html',{'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) #,take category st or tch)
                #saving new user to the database    
                user.save()
                # logging in the saved user
                login(request, user)
                #redirecting the logged in user to the currentuser page by passing current user function
                return redirect('currentuser')
            except IntegrityError:
                return render(request,'multipleuser/signupuser.html',{'form': UserCreationForm(), 'error': 'This username isnt available, try another!'})

        else:
            return render(request,'multipleuser/signupuser.html',{'form': UserCreationForm(), 'error': 'passwords didnt match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'multipleuser/loginuser.html',{'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'multipleuser/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and Password didnot match. Try Again!'})
        else:
            login(request, user)
                #redirecting the logged in user to the currentuser page by passing current user function
                #if usertype=st -> redirect to viewstudentcourse.html, else usertype= tch ->
            return redirect('currentuser')

@login_required
def logoutuser(request):
    #we only want to log some user out if it is post, if logout is a get request browser will log u out as soon as u log in so cant access logout page by '/logout'
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required
def createcourse(request):
    #similar to somemone when someone is signing up
    if request.method == 'GET':
        return render(request,'multipleuser/createcourse.html',{'form': CreateCourseForm()})
    else:
        try:
            form = CreateCourseForm(request.POST  or None, request.FILES or None)
            #commit false save will not save it in the database
            newcourse = form.save(commit=False)
            newcourse.user = request.user
            newcourse.save()
            #sending the new course to the current page
            return redirect('currentuser')  
        except ValueError:          
            return render(request,'multipleuser/createcourse.html',{'form': CreateCourseForm(), 'error': 'Wrong Data passed in. Please try again.'})

@login_required
def currentuser(request):
    #filter makes sure that only logged in user course is shown not everyones
     course1 = Course1.objects.filter(user=request.user)
     list_video_next = Course1.objects.values_list("files")
     #list_video_prev = Course1.reverse.value_list("files")
     return render(request,'multipleuser/currentuser.html', { 'course1': course1})

@login_required
def viewcourse(request, course_pk):
     course = get_object_or_404(Course1, pk=course_pk, user=request.user)
     if request.method == 'GET':
         form = CreateCourseForm(instance = course)
         return render(request,'multipleuser/viewcourse.html', { 'course': course, 'form': form })
#request.user allows only the particular user to update his/her own course
     else:
         try: #instance= course will help django to understand its an exisiting object and we are trying to update that
            form = CreateCourseForm(request.POST  or None, request.FILES or None, instance = course)
            form.save()
            return redirect('currentuser')  

         except ValueError:
            return render(request,'multipleuser/viewcourse.html', { 'course1': course1, 'form': form, 'error': 'Wrong Data passed in. Please try again.'})

@login_required           
def deletevideo(request, course_pk):
    course = get_object_or_404(Course1, pk=course_pk, user=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('currentuser')


