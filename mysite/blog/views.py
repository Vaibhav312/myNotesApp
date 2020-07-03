from django.shortcuts import render
from blog.forms import UserForm,ContactUsForm,NotesForm
from blog.models import NotesInfo,User
from django.contrib import messages
from django.contrib.sessions.models import Session

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.session.get('username'):
        return HttpResponseRedirect(reverse('mainpageloggedin'))
    if request.session.get('username')==None:
        
        return render(request,'index.html')
    
    

def help(request):
    if request.session.get('username'):
         return HttpResponseRedirect(reverse('mainpageloggedin'))
    return render(request,'help.html')

@login_required
def mainpageloggedin(request):
    if request.session.get('username'):
        userx=request.user.id
    
        if request.method=="POST":
            add_note=NotesForm(data=request.POST)
            if add_note.is_valid():
                userx=request.user.id
                
                add_note.save()
                context={"user_data":userx}
                messages.success(request, 'Notes saved successfully!',extra_tags='alert')
                return HttpResponseRedirect(reverse('mainpageloggedin'),context)
        else:
            add_note=NotesForm()
        return render(request,'mainpageloggedin.html',context={'notes':add_note,"user_data":userx})
    if request.session.get('username')==None:
        return HttpResponseRedirect(reverse('index')) 



def display_notes(request):
    if request.session.get('username'):
        total_notes=NotesInfo.objects.filter(user=request.user.id).values('id','add_notes').order_by('-id')
    
        data=[]
        for x in total_notes:
            data.append(x)
        if data==[]:
            context={"empty":""}
            return render(request,"all_notes.html",context)
        return render(request,"all_notes.html",context={"show_notes":data})
    if request.session.get('username')==None:
        return HttpResponseRedirect(reverse('index'))                                                         




def lastContact(request):
    if request.session.get('username'):
         return HttpResponseRedirect(reverse('mainpageloggedin'))
    return render(request,'lastContact.html')

def contactus(request):
    if request.session.get('username'):
         return HttpResponseRedirect(reverse('mainpageloggedin'))
    else:
        if request.method== "POST":
            contact=ContactUsForm(data=request.POST)
            if contact.is_valid():
                contact.save()
                return HttpResponseRedirect(reverse('lastContact'))
        else:
            contact = ContactUsForm()
        return render(request,'contactus.html',context={'contacts':contact})




@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if not request.session.get('username'):
        registered = False

        if request.method == 'POST':

            # Get info from "both" forms
            # It appears as one form to the user on the .html page
            user_form = UserForm(data=request.POST)

            # Check to see both forms are valid
            if user_form.is_valid():

                # Save User Form to Database
                user = user_form.save()

                # Hash the password
                user.set_password(user.password)

                # Update with Hashed password
                user.save()


                # Registration Successful!
                registered = True
                login(request,user)
                request.session['username']=user.username
          
                return HttpResponseRedirect(reverse('user_login'))

            else:
                # One of the forms was invalid if this else gets called.
                print(user_form.errors)

        else:
            # Was not an HTTP post so we just render the forms as blank.
            user_form = UserForm()

        # This is the render and context dictionary to feed
        # back to the registration.html file page.
        return render(request,'sign_up.html',
                            {'user_form':user_form,
                            'registered':registered})
    return HttpResponseRedirect(reverse('mainpageloggedin'))

def user_login(request):
    if not request.session.get('username'):
        if request.method == 'POST':
            # First get the username and password supplied
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)

            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to some page.
                    # In this case their homepage.
                    #request.session.set_expiry(60)
                    request.session['username']=username
                    return HttpResponseRedirect(reverse('mainpageloggedin'))
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                messages.success(request, 'Wrong Credentials!',extra_tags='alert')

        else:
            #Nothing has been provided for username or password.
            return render(request, 'login.html',)
    return HttpResponseRedirect(reverse('mainpageloggedin'))
    
@login_required
def update(request,pk):
    if request.session.get('username')==None:
         return HttpResponseRedirect(reverse('index'))
    else:
        note=NotesInfo.objects.get(id=pk)
        form=NotesForm(instance=note)
        if request.method=='POST':
            form=NotesForm(request.POST,instance=note)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/mainpageloggedin/all_notes')
        
        
        context={"form":form}

        return render(request,'update_task.html',context)

@login_required
def delete(request,pk):
    
        item=NotesInfo.objects.get(id=pk)
        if request.method=='POST':
            item.delete()
           
            return HttpResponseRedirect('/mainpageloggedin/all_notes')
        
        
        context={"item":item}

        return render(request,'delete.html',context)
