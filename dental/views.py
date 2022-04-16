import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import *

from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *



@login_required(login_url='login')
def index(request):



    pay = [] 

    orders_count = order_detials.objects.all().count()

    payment_data = payments.objects.all()

    doctors_data = doctor.objects.all().count()

    for i in payment_data:
        pay.append(i.amount)

    amount = sum(pay)
    

    context = {
        
        'orders_count' : orders_count,
        'amount' : amount,
        'doctors_data' : doctors_data,
        
    }

    return render(request, 'dashboard.html', context)





def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)

            
            if user:
                print('yes')
                login(request, user)
                return redirect('index')

            else:

                msg = 'Credentials wrong'


                context = {
                    'msg': msg,
                    'form': forms,
                }
                return render(request, 'users/login.html', context)
        
        else:

           
            context = {
                'form': forms,
                }
            return render(request, 'users/login.html', context)
    context = {'form': forms}
    return render(request, 'users/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')