from datetime import datetime
from operator import truediv
from django.db import models

# Create your models here.


class doctor(models.Model):

    name = models.CharField(max_length=50)
    mobile_no = models.IntegerField()
    address = models.CharField(max_length=225)


class order(models.Model):
    
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    date_time = models.DateField(auto_now=True, blank = True, null = True)
    patient_name = models.CharField(max_length=225)
    total_amount = models.IntegerField()

class order_detials(models.Model):

    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.CharField(max_length=225)
    teeth1 = models.IntegerField(blank = True, null = True)
    teeth2 = models.IntegerField(blank = True, null = True)
    teeth3 = models.IntegerField(blank = True, null = True)
    teeth4 = models.IntegerField(blank = True, null = True)
    unit = models.IntegerField()
    total_amount = models.IntegerField()

class payments(models.Model):
    
    bill = models.ForeignKey(order, on_delete=models.CASCADE)
    amount = models.IntegerField()
