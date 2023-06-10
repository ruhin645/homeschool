from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


from .forms import UserAuthenticationForm,UserRegisterationForm

from itertools import chain
#regestering user through admin
def register_view(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save() 
            user_name=form.cleaned_data.get('username')
            login(request,user)
            return redirect('home')
        else:
            return render(request,'add_user.html',{'form':form})
    form=UserRegisterationForm()
    return render(request,'add_user.html',{'form':form})

def login_view(request):
    if request.method=="POST":
        form=UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=user_name,password=password)
            if user!=None:
                login(request,user)
                if user.is_teacher==True:
                    return redirect('/tdashboard')
                elif user.is_student==True:
                    return redirect('/tdashboard/std')
                elif user.is_staff==True:
                    return redirect('/loc_admin')
                return redirect('/')
        else:
            return render(request,'loginpage.html',{'form':form})
    form=UserAuthenticationForm()
    return render(request,'loginpage.html',{'form':form})