from django.shortcuts import redirect, render, HttpResponse
from .models import Doctor, Contact, Appointments
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from itertools import chain  # aa import queries ne merge karva mate chhe

# aa code geek4geeks mathi email sending mate lidhelo chhe
from django.conf import settings
from django.core.mail import send_mail
# code finish here

import random
import datetime
from django.utils import timezone

# aa code mobile phone messege mokalva mate
import zerosms
import getpass
# code finish here



# creat your views here

def index(request):
    doctors = Doctor.objects.all()
    params = {'doctors': doctors}
    return render(request, 'index.html', params)


def search(request):
    query = request.GET['search']
    if len(query) > 0 and 0 < 55:
        doctors_name = Doctor.objects.filter(name__icontains=query)

        doctors_address = Doctor.objects.filter(address__icontains=query)
        doctors_specializatioin = Doctor.objects.filter(specializatioin__icontains=query)
        doctors_city = Doctor.objects.filter(city__icontains = query)

        doctors = list(chain(doctors_name, doctors_address, doctors_specializatioin , doctors_city))
        params = {'doctors': doctors}
        # print(doctors)
    else:
        return HttpResponse('''<center><h1><b> We Respect Your Time. <br>
                                       Please Search Properly or Try Other Words
                               </b></h1></center>''')

    return render(request, 'd_search.html', params)


def user_sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email_id = request.POST.get('email')
        # phone_number = request.POST.get('user_phone_number')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        # check for any error in sign up

        # if len(username) > 10:
        #     messages.error(request ,"Your username must be under 10 characters")
        #     return redirect('user_sign_up.html')
        if not username.isalnum():
            messages.error(request, "username should only contain letters and numbers")
            return redirect('user_sign_up.html')
        if (password1 != password2):
            messages.error(request, "Please Match Both Passwords")
            return redirect('user_sign_up.html')
        # aaya email otp varification aapvanu chhe

        # Creating User
        myuser = User.objects.create_user(username, email_id, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.phone_number = phone_number
        myuser.save()
        messages.success(request, "Sign Up Successfull")

        # sign_up success email sending code is here
        subject = 'welcome to Aayu-Mitra.com'
        message = f' Hii {myuser.username}, thank you for registering in Aayu-Mitra.com' \
                  f' {myuser.username} You Can Now Enjoy Our All Service for Free , & Do not Forget to tell your buddies About Us. Thank You Again'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email]
        send_mail(subject, message, email_from, recipient_list)


        return redirect('/')

    else:
        return render(request, 'user_sign_up.html')

    return render(request, 'user_sign_up.html')


def user_login(request):
    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')

        user = authenticate(username=login_username, password=login_password)
        if user is not None:
            login(request, user)
            messages.success(request, "login successful , Please Tap This Button-->")
            return redirect('/')
        else:
            messages.error(request, "Invalid Password or Email , Please Try Again or Sign Up Now")
            return render(request, 'index.html')

    else:
        return HttpResponse('somethig went wrong')


def user_logout(request):
    logout(request)
    messages.error(request, "Successfully Logged Out")
    return redirect('/')


def consolt_page(request):
    doctors = Doctor.objects.all()
    params = {'doctors': doctors}
    return render(request, 'view_page.html', params)





def d_dashboard(request):
    if request.method == "POST":
        email = request.POST.get('d_email_id')
        password = request.POST.get('d_password')
        doctor = Doctor.objects.filter(email_id__icontains=email , password__icontains = password) #aa code ek fix doctor return karse

        # aa che login vali process
        if email == doctor[0].email_id and password == doctor[0].password:
            messages.success(request ,"Login Successfull, Thanks for Using Aayu-Mitra.com")

            # aa code thi login thayela doctor na Appointments Record table tarike aave chhe
            d_id = doctor[0].id
            record_history = Appointments.objects.filter(d_id__icontains = d_id)
            params = {"doctor": doctor , "record" : record_history , "d_id" : d_id}
            return render(request, 'd_dashboard_login.html' , params)
        else:
            print("sorry , code doesn't work")
            messages.error(request, "Invalid Password or Email , Please Try Again or Register Now")
            return render(request, 'd_dashboard_login.html')
    else:
        return render(request, 'd_dashboard_login.html')

def Appointment_record(request , d_id):
    if request.method == "POST":
        doctor = Doctor.objects.all()
        name = request.POST.get('name')
        print(name)
        email_id = request.POST.get('email', default=" ")
        date = request.POST.get('date', default=" ")
        phone_number = request.POST.get('phone_number', default=" ")
        confirmation_code = request.POST.get('confirmation_code', default=" ")
        age = request.POST.get('age')
        record_history = Appointments.objects.filter(name__icontains=name , d_id__icontains=d_id,email_id__icontains=email_id,
                                                     dateTime__icontains=date,phone_number__icontains=phone_number,
                                                     confirmation_code__icontains=confirmation_code , age__icontains=age)
        params = {"doctor": doctor, "record": record_history, "d_id": d_id}
    return render(request, 'Appointment_record.html' , params)

def consolt_view(request, consolt_id):

    # fetching doctors data using id
    doctors = Doctor.objects.filter(id=consolt_id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user)
            # user apppointment le atle a no badho data aahi fetch thase (emergency sahit)
            username = request.user.username
            name = request.POST.get('patient_name')
            age = request.POST.get('patient_age')
            gender = request.POST.get('patient_gender')
            email_id = request.user.email
            phone_number = request.POST.get('phone_number')
            emergency = request.POST.get('emergency')
            d_id = consolt_id
            dateTime = timezone.now()

            # aaya aapde ek random number generate karsu j partient ane compounder ne confirmation ma help karse
            confirmation_code = random.randint(1000 , 100000)

            appointments_record = Appointments(username = username , name=name , age=age , gender=gender , email_id = email_id ,
                                                phone_number = phone_number, emergency = emergency,
                                                confirmation_code = confirmation_code , d_id = d_id , dateTime = dateTime)
            appointments_record.save()


            # Appointment success email sending to patient --> code is here
            subject = f' Appointment Successful with {doctors[0].name}'
            message = f' Thank You {name}, for Using Aayu-Mitra.com \n' \
                      f' We have Sent Your Details to {doctors[0].name} , They will Shortly Contact You. Stay Blessed \n' \
                      f' Note That Your Confirmation Code is {confirmation_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email_id]
            send_mail(subject, message, email_from, recipient_list)
            print("SUCCESS : EMAIL REACHED PATIENT")

            # New Appointment email sending to Doctor --> code is here
            subject = f' Greeting Sir , New Appointment from Aayu-Mitra.com'
            message = f' {username} has Apppointed You. Here is All Details \n' \
                      f' Name : {name}  \n' \
                      f' Gender : {gender} \n' \
                      f' Age : {age} \n' \
                      f' Email : {request.user.email} \n' \
                      f' Phone Number : {phone_number} \n' \
                      f' Emergency : {emergency} \n' \
                      f' Please Note Your Confirmation Code : {confirmation_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [doctors[0].email_id]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "Appointment Successful , Check Your Email Please-->")
            print("SUCCESS : EMAIL REACHED DOCTOR")

        else :
            return render(request, 'consolt_view.html',
                          {'doctors': doctors[0]})  # [0] valu logic super chhe must learn every time

    elif request.method == 'POST' and not request.user.is_authenticated:
        return HttpResponse('''<center><h1><b> We Respect Your Time. <br>
                                            Please <a href="/user_sign_up.html">Sign Up</a> & if you have already Signed Up then Please <a href="/">Login</a> First
                                    </b></h1></center>''')

    else:
        return render(request, 'consolt_view.html',
                           {'doctors': doctors[0]})  # [0] valu logic super chhe must learn every time

    # aaya compounder ne email ane message aave teni mate na functions aavse




    return render(request, 'consolt_view.html', {'doctors': doctors[0]})  # [0] valu logic super chhe must learn every time


def left_sidebar(request):
    return render(request, 'left-sidebar.html')


def right_sidebar(request):
    return render(request, 'right-sidebar.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('user_name', '')
        phone = request.POST.get('user_phone_number', '')
        email = request.POST.get('user_email_id', '')
        suggestion = request.POST.get('user_suggestion', '')
        query = request.POST.get('user_query', '')
        complaint = request.POST.get('user_complaint', '')
        rating = request.POST.get('user_rating', '')
        contact = Contact(user_name=name, user_phone_number=phone, user_email_id=email,
                          user_suggestion=suggestion, user_query=query, user_complaint=complaint,
                          user_rating=rating)
        contact.save()
    return render(request, 'contactus.html')
