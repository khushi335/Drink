from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from .models import People,Category,Drink
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator


import logging
logger=logging.getLogger('django')

import re

# Create your views here.

@login_required(login_url='log_in')
def index(request):
    cate = Category.objects.all()
    cateid = request.GET.get('category')
    drinks = Drink.objects.filter(category__id=cateid).order_by('id') if cateid else Drink.objects.all().order_by('id')

    paginator = Paginator(drinks, 3)
    page_num = request.GET.get('page')
    data = paginator.get_page(page_num)

    context = {
        'categories': cate,
        'drinks': data,
        'selected_category': int(cateid) if cateid else None,
        'num': range(1, data.paginator.num_pages + 1),
        'date': datetime.now(),
    }

    if request.method == 'POST':
        Name = request.POST.get('Name')
        Phone_Number = request.POST.get('Phone_Number')
        Email = request.POST.get('Email')
        Message = request.POST.get('Message')

        try:
            user = People(Name=Name, Phone_Number=Phone_Number, Email=Email, Message=Message)
            user.full_clean()
            user.save()

            subject = "Drink Info"
            message = render_to_string('main/message.html', {'Name': Name, 'date': datetime.now()})
            from_email = 'sahkhushi946@gmail.com'
            recipient_list = [Email, 'skhushi0218@gmail.com']

            email_msg = EmailMessage(subject, message, from_email, recipient_list)
            email_msg.send(fail_silently=True)

            messages.success(request, f'Hi {Name}, your data is successfully submitted! Please check your mail.')
            return redirect('index')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('index')
        
    return render(request, 'main/index.html', context)




@login_required(login_url='log_in')
def about(request):
    return render(request,"main/about.html")

@login_required(login_url='log_in')
def contact(request):
    if request.method=='POST':
        Name=request.POST.get('Name')
        Phone_Number=request.POST.get('Phone_Number')
        Email=request.POST.get('Email')
        Message=request.POST.get('Message')

        try:
            user=People(Name=Name,Phone_Number=Phone_Number,Email=Email,Message=Message)
            user.full_clean()
            user.save()

            subject="drink"
            message=render_to_string('main/message.html',{'Name':Name,'date':datetime.now()})
            from_email='sahkhushi946@gmail.com'
            recipient_list=['skhushi0218@gmail.com']
            
            email_msg=EmailMessage(subject,message,from_email,recipient_list)
            email_msg.send(fail_silently=True)

            messages.success(request,f' Hi {Name},your data is succesfully submitted !!!!! please check your mail ')
            return redirect('contact')
        
        except Exception as e:
            messages.error(request,f'Error : {str(e)}')
            return redirect('contact')
        
    return render(request,"main/contact.html")

## For Auth
def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me','') #on or None

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Username is not register yet')

            return redirect('log_in')
        
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(12000000000)
            else :
                request.session.set_expiry(0)

            next=request.POST.get('next','')

            return redirect(next if next else 'index')
        else:
            messages.error(request,'Invalid password!!')
            return redirect('log_in')
        
    next=request.GET.get('next','')

    return render(request,'auth/login.html',{'next':next})

def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password==cpassword:
            try:
                validate_password(password)

                if User.objects.filter(username=username).exists():
                    messages.error(request,"Username is already registered !!!")
                    return redirect('register')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email is already registered !!!")
                    return redirect('register')
                
                if username==password:
                    messages.error(request,"Username and Password shouldn't be same")
                    return redirect('register')
                
                
                if not re.search(r'[A-Z]',password):
                    messages.error(request,'Your password should at least contain one upper letter')
                    return redirect('register')
                
                
                if not re.search(r'\W',password):
                    messages.error(request,'Your password should at least contain one special character')
                    return redirect('register')
                
                
                if not re.search(r'\w',password):
                    messages.error(request,'Your password should contain characters from a to Z, digits from 0-9, and the underscore _ character')
                    return redirect('register')
                
                

                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"Your Form is successfully registered !!!!!")
                return redirect('log_in')
            
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                    return redirect('register')
        
        else:
            messages.error(request,"Your password and confirm password doesn't match")
            return redirect('register')
            
    return render(request,"auth/register.html")

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)

    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()  
            return redirect('log_in')

    return render(request,'auth/change_password.html',{'form':form})



@login_required(login_url='log_in')
def location(request):
    return render(request,"main/location.html")