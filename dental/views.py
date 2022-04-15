import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import *


# @login_required(login_url='login')
def index(request):

    if request.user.is_superuser:

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

        return render(request, 'dashboard.html')