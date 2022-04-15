from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
    path('add-doctor/', add_doctor, name='add_doctor'),
    path('update-doctor/<doctor_id>', update_doctor, name='update_doctor'),
    path('delete-doctor/<doctor_id>', delete_doctor, name='delete_doctor'),
    path('list-doctor/', list_doctor, name='list_doctor'),

    path('order/<doctor_id>', add_bill, name='add_bill'),
    path('update-order/<bill_id>', update_bill, name='update_bill'),
    path('list-order/<doctor_id>', list_bill, name='list_bill'),
    path('delete-order/<bill_id>', delete_bill, name='delete_bill'),

    
    path('add-payment/<bill_id>', add_payment, name='add_payment'),
    path('update-payment/<payment_id>', update_payment, name='update_payment'),
    path('delete-payment/<payment_id>', delete_payment, name='delete_payment'),
    path('list-payment/<bill_id>', list_payment, name='list_payment'),

    
    path('bill-generate<order_id>', generate_bill, name='generate_bill'),



]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)