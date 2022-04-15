from logging import PlaceHolder
from django import forms
from django.forms.widgets import DateTimeInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime





class doctor_Form(forms.ModelForm):
    class Meta:
        model = doctor
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'battery_no'
            }),

        }

class payment_Form(forms.ModelForm):
    class Meta:
        model = payments
        fields = '__all__'
        exclude = ['order', 'bill']

        widgets = {
            
            'order': forms.Select(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),

        }


class bill_Form(forms.ModelForm):
    class Meta:
        model = order
        fields = '__all__'
        exclude = ['date_time', 'doctor', 'total_amount']
        widgets = {
            
            'doctor': forms.Select(attrs={
                'class': 'form-control', 'id': 'doctor'
            }),

            'patient_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'patient_name'
            }),

        }


class bill_details_Form(forms.ModelForm):
    class Meta:
        model = order_detials
        fields = '__all__'
        widgets = {

            'product': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'product'
            }),

            'teeth1': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),

            'teeth2': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),

            'teeth3': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),

            'teeth4': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),

            'unit': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),

            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_amount'
            }),


        }
