from django.contrib import auth
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def homepage(request):
    return render(request,"homepage.html")

def contact(request):
    if request.method == "POST":
        msg_name = request.POST['full-name']
        msg_email = request.POST['email']
        msg = request.POST['message']

        #send mail
        send_mail(
            'Message from '+ msg_name,
            msg,
            msg_email,
            ['itzamir092@gmail.com'],
        )
        return render(request, "contact.html")
    else:
        return render(request, "contact.html")

def adm(request):
    return render(request,'admin_panel.html')


