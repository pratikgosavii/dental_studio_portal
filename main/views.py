import mimetypes
from multiprocessing import context
from django.shortcuts import render, redirect
from .forms import *
from django.http import FileResponse, HttpResponse, JsonResponse


from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm,mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph, Spacer
import pdfkit

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.



def add_doctor(request):

    if request.method == 'POST':

        form = doctor_Form(request.POST)

        if form.is_valid():

            form.save()

            return redirect('list_doctor')
        
        else:

            print(form.errors)
            
            return render(request, 'main/add_doctor.html', {'form' : form})

        return render(request, 'main/add_doctor.html', {'form' : form})

    else:

        form = doctor_Form

        return render(request, 'main/add_doctor.html', {'form' : form})


def update_doctor(request, doctor_id):

    if request.method == 'POST':

        instance = doctor.objects.get(id = doctor_id)

        form = doctor_Form(request.POST, instance=instance)

        if form.is_valid():

            form.save()

            return redirect('list_doctor')
        
        else:
            
            return render(request, 'main/add_doctor.html', {'form' : form})

        
    else:

        instance = doctor.objects.get(id = doctor_id)

        form = doctor_Form(instance=instance)


        return render(request, 'main/add_doctor.html', {'form' : form})


def delete_doctor(request, doctor_id):

   doctor.objects.get(id = doctor_id).delete()

   return redirect('list_doctor')



def list_doctor(request):

    data = doctor.objects.all()

    context = {

        'data' : data
    }

    return render(request, 'main/list_doctor.html', context)


def add_bill(request, doctor_id):


    if request.method == 'POST':

        doctor_instance = doctor.objects.get(id=doctor_id)

        form = bill_Form(request.POST)

        if form.is_valid():

            product = request.POST.getlist('product[]')
            teeth1 = request.POST.getlist('teeth1[]')
            teeth2 = request.POST.getlist('teeth2[]')
            teeth3 = request.POST.getlist('teeth3[]')
            teeth4 = request.POST.getlist('teeth4[]')
            unit = request.POST.getlist('unit[]')
            total_amount = request.POST.getlist('total_amount[]')
            print(teeth1)
            total_amount_bill = sum(map(int, total_amount))

            teeth1 = list(map(int, teeth1))
            teeth2 = list(map(int, teeth2))
            teeth3 = list(map(int, teeth3))
            teeth4 = list(map(int, teeth4))
          

            unit = (map(int, teeth4))

            instance = form.save(commit=False)
            instance.doctor = doctor_instance
            instance.total_amount = total_amount_bill
            instance.save()

            for a,b,c,d,e,f,g in zip(product, teeth1, teeth2, teeth3, teeth4, unit, total_amount):

                print('in for')
                order_detials.objects.create(order = instance, product = a, teeth1 = b, teeth2 = c, teeth3 = d, teeth4 = e, unit = f, total_amount = g)


            return JsonResponse({'status' : 'done'}, safe=False)

        

        else:

            error = form.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)


    else:

        print('here')

        form = bill_Form()

        return render(request, 'main/add_bill.html', {'form' : form, 'doctor_id' : doctor_id})



def update_bill(request, bill_id):

    bill_instance = order.objects.get(id=bill_id)
    doctor_instance = doctor.objects.get(id=bill_instance.doctor.id)

    
    if request.method == 'POST':

        form = bill_Form(request.POST, instance=bill_instance)

        if form.is_valid():

           
            print('saveeeeeeeeeeeeeeeeee')

            product = request.POST.getlist('product[]')
            teeth1 = request.POST.getlist('teeth1[]')
            teeth2 = request.POST.getlist('teeth2[]')
            teeth3 = request.POST.getlist('teeth3[]')
            teeth4 = request.POST.getlist('teeth4[]')
            unit = request.POST.getlist('unit[]')
            work_id = request.POST.getlist('work_id[]')
            total_amount = request.POST.getlist('total_amount[]')
            for i in product:
                print(i)
            total_amount_bill = sum(map(int, total_amount))

            instance = form.save(commit=False)
            instance.doctor = doctor_instance
            instance.total_amount = total_amount_bill
            instance.save()

            for a,b,c,d,e,f,g,h in zip(product, teeth1, teeth2, teeth3, teeth4, unit, total_amount, work_id):

                print(a)
               

                if h:


                    order_detial_instance = order_detials.objects.get(id = h)

                    order_detial_instance.product = str(a)
                    order_detial_instance.teeth1 = b
                    order_detial_instance.teeth2 = c
                    order_detial_instance.teeth3 = d
                    order_detial_instance.teeth4 = e
                    order_detial_instance.unit = f
                    order_detial_instance.total_amount = g
                    order_detial_instance.save()

                else:

                    print('creating object')

                    order_detials.objects.create(order = instance, product = a, teeth1 = b, teeth2 = c, teeth3 = d, teeth4 = e, unit = f, total_amount = g)


            return JsonResponse({'status' : 'done'}, safe=False)

        
        else:

            print(form.errors)

            print('----------------------saveeeeeeeeeeeeeeeeee')
            
            
            return render(request, 'main/add_doctor.html', {'form' : form})

    else:

        bill_instance = order.objects.get(id=bill_id)

        form = bill_Form(instance=bill_instance)

        order_detials_data = order_detials.objects.filter(order = bill_instance)
        print(order_detials_data.count())
        context = {

            'form' : form, 
            'doctor_id' : bill_instance.doctor.id, 
            'order_detials_data' : order_detials_data,
            'bill_count' : order_detials_data.count(),
            'bill_instance' : bill_instance.id
        }

        return render(request, 'main/update_bill.html', context)



def list_bill(request, doctor_id):

    instance = doctor.objects.get(id=doctor_id)

    data = order.objects.filter(doctor = instance)

    context = {

        'data' : data,
        'instance' : instance
    }

    return render(request, 'main/list_bill.html', context)




def delete_bill(request, bill_id):

    bill_instance = order.objects.get(id=bill_id)
    doctor_id = bill_instance.doctor.id
    bill_instance.delete()



    instance = doctor.objects.get(id=doctor_id)

    data = order.objects.filter(doctor = instance)

    context = {

        'data' : data,
        'instance' : instance
    }

    return render(request, 'main/list_bill.html', context)





def add_payment(request, bill_id):

    if request.method == 'POST':

        
        bill_instance = order.objects.get(id=bill_id)

        form = payment_Form(request.POST)

        if form.is_valid():

            total = []

            a = payments.objects.filter(bill = bill_instance)

            for i in a:

                total.append(i.amount)

            
            amount = form.cleaned_data['amount']



            if (int(sum(total)) + int(amount)) > int(bill_instance.total_amount):

                return render(request, 'main/add_payment.html', {'form' : form, 'msg' : 'Total is going above total cost of work'})

            print('000000000000000here')
                
            instance = form.save(commit=False)
            instance.bill = bill_instance
            instance.save()

            return redirect('list_payment', bill_instance.id)
        
        else:

            print(form.errors)

            print('----------------------saveeeeeeeeeeeeeeeeee')
            
            return render(request, 'main/add_payment.html', {'form' : form})


    else:

        form = payment_Form()

        return render(request, 'main/add_payment.html', {'form' : form})




def update_payment(request, payment_id):

    payment_instance = payments.objects.get(id=payment_id)
    bill_instance = order.objects.get(id = payment_instance.bill.id)

    if request.method == 'POST':

        
        form = payment_Form(request.POST, instance=payment_instance)

        if form.is_valid():

            total = []

            a = payments.objects.filter(bill = bill_instance)

            for i in a:

                total.append(i.amount)

            
            amount = form.cleaned_data['amount']

            
            if (int(sum(total)) + int(amount)) > int(bill_instance.total_amount):

                return render(request, 'main/add_payment.html', {'form' : form, 'msg' : 'Total is going above total cost of work'})


            form.save()

            return redirect('list_payment', payment_instance.bill.id)
        
        else:

            print(form.errors)

            print('----------------------saveeeeeeeeeeeeeeeeee')
            
            return render(request, 'main/add_payment.html', {'form' : form})


    else:

        form = payment_Form(instance = payment_instance)

        return render(request, 'main/add_payment.html', {'form' : form})






def list_payment(request, bill_id):

    instance = order.objects.get(id=bill_id)

    data = payments.objects.filter(bill = instance)

    pay = []

    for i in data:
        pay.append(i.amount)

    total_amount = sum(pay)

    remaning_amount = instance.total_amount - total_amount
    print('remaning_amount')
    print(remaning_amount)

    context = {

        'data' : data,
        'bill_id' : bill_id,
        'total_amount' : total_amount,
        'order_amount' : instance.total_amount,
        'remaning_amount' : remaning_amount
    }

    return render(request, 'main/list_payment.html', context)



def delete_payment(request, payment_id):

    payment_instance = payments.objects.get(id=payment_id)
    bill_id = payment_instance.bill
    payment_instance.delete()
    return redirect('list_payment',payment_instance.bill.id)






def number_to_word(number):
    def get_word(n):
        words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
        if n<=20:
            return words[n]
        else:
            ones=n%10
            tens=n-ones
            return words[tens]+" "+words[ones]
            
    def get_all_word(n):
        d=[100,10,100,100]
        v=["","Hundred And","Thousand","lakh"]
        w=[]
        for i,x in zip(d,v):
            t=get_word(n%i)
            if t!="":
                t+=" "+x
            w.append(t.rstrip(" "))
            n=n//i
        w.reverse()
        w=' '.join(w).strip()
        if w.endswith("And"):
            w=w[:-3]
        return w

    arr=str(number).split(".")
    number=int(arr[0])
    crore=number//10000000
    number=number%10000000
    word=""
    if crore>0:
        word+=get_all_word(crore)
        word+=" crore "
    word+=get_all_word(number).strip()+" Rupees"
    if len(arr)>1:
         if len(arr[1])==1:
            arr[1]+="0"
         word+=" and "+get_all_word(int(arr[1]))+" paisa"
    return word



def generate_bill(request, order_id):


    order_data = order.objects.get(id=order_id)
    print(order_data)
    order_details_data = order_detials.objects.filter(order = order_data)
    
    img_file = 'media/denal2.png'

    print(order_details_data)


    all_price = []


    
    for i in order_details_data:
        
        total_amount = i.total_amount
        all_price.append(total_amount)
    
        
    total_price = order_data.total_amount
    patient_name = order_data.patient_name
    date_time = order_data.date_time

    
    list_1 = []
    list_1.append([ "SR NO" , "Order Date", "Patient", "product", "Teeth#", "Unit", "Total Amount" ])

    count = 1


    for i in order_details_data:

        teeths = ''
        teeths = teeths + str(i.teeth1) + '     '
        teeths = teeths + str(i.teeth2) + '     '
        teeths = teeths + "\n\n"
        teeths = teeths + str(i.teeth3) + '     '
        teeths = teeths + str(i.teeth4) + '     '

        list_1.append([count, date_time, Paragraph(patient_name), i.product, teeths, i.unit, i.total_amount])

    DATA = list_1

    DATA1 = [
        ['Intact dental lab'],
        ['Gopipushpa Opp. Sadguru Gas Agency.\n Giri Nagar, R.TO Road. Akola - 444 005 (M.S.)\n '],
    ]

    DATA2 = [
        ['Yogesh G. Sarag'],
        ['80077 00877\n98504 30096'],
    ]

    payment_data = payments.objects.filter(bill = order_data)
    pay = []

    for i in payment_data:
        pay.append(i.amount)
    
    advance_price = int(sum(pay))

    grand_price = total_price - advance_price

    inword = number_to_word(grand_price)

    list_3 = []
    list_3.append(["Total Amount", total_price])
    list_3.append(["Advance Amount", advance_price])
    list_3.append(["Grand Total : " + inword, grand_price])
    DATA3 = list_3
   
    # creating a Base Document Template of page size A4

    time =  str(datetime.now())
    time = time.split('.')
    time = time[0].replace(':', '-')
    name = "Bill " + time + ".pdf"
    path = os.path.join(BASE_DIR) + '\static\csv\\bill.pdf'
    
    pdf = SimpleDocTemplate(path , pagesize = A4 )
    
    # standard stylesheet defined within reportlab itself
    styles = getSampleStyleSheet()
    
    # fetching the style of Top level heading (Heading1)
    title_style = styles[ "Heading1" ]
    
    # 0: left, 1: center, 2: right
    title_style.alignment = 1
    
    # creating the paragraph with
    # the heading text and passing the styles of it
    title = Paragraph( "" , title_style )
    
    pdf1 = canvas.Canvas(path)
    pdf1.drawImage(img_file, 50, 627, width=120, preserveAspectRatio=True, mask='auto')


    # creates a Table Style object and in it,
    # defines the styles row wise
    # the tuples which look like coordinates
    # are nothing but rows and columns
    

    style = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), ( -1, -1 ), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, -1 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),

        ]
    )

    style2 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (1,0), (1, -1), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTSIZE', (0, 0), (0, 0), 16),
        
        ]
    )

    style3 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "RIGHT" ),

          

        ]
    )

    style4 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ( "ALIGN" , ( 0, 0 ), ( 0, 2 ), "LEFT" ),
            ( "GRID" , (0, 0), ( -1, -1 ), 0, colors.black ),

            ('FONTNAME', (0,0), (0, 2), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTSIZE', (0, 0), (0, 2), 13),

        ]
    )



    
    # creates a table object and passes the style to it

    table1 = Table(DATA , style = style, colWidths=(1.4*cm, 3*cm, 4*cm, 4.5*cm, 3*cm, 1.2*cm, 2.4*cm), rowHeights=(1.5*cm))
    table2 = Table(DATA1 , style = style2, colWidths=(19.5*cm), rowHeights=(1.5*cm, 1.5*cm))
    table3 = Table(DATA2 , style = style3, colWidths=(19.5*cm))
    table4 = Table(DATA3 , style = style4, colWidths=(16.9*cm, 2.6*cm), rowHeights=(1*cm))
   


    # table = [ title , table3, table1, table2, table4, table5, table6, table7, table8])
    # table.set(Style)
    flow_obj = []
    frame1 = Frame(0,10,600,800)
    flow_obj.append(title)
    flow_obj.append(table2)
    flow_obj.append(table3)
    flow_obj.append(table1)
    flow_obj.append(table4)
   
    
    frame1.addFromList(flow_obj, pdf1)

    # building pdf
    pdf1.save()
    with open(path, 'rb') as fh:
        mime_type  = mimetypes.guess_type('receipt.pdf')
        response = HttpResponse(fh.read(), content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=receipt.pdf'

    return response








