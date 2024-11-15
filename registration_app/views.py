import datetime
from datetime import datetime, timedelta
from django.contrib import messages
import json
import stripe
import logging
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import JsonResponse, HttpResponse, request
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentFilterForm
from .models import CustomUser, Payment_webhook
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from Scholarshipapp.models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


# YOUR_DOMAIN = 'http://127.0.0.1:5000'

# Create your views here.
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = CustomUser.custom_authenticate(username=username, password=password)
#         user_details = Payment_webhook.objects.all()
#         if user is not None:
#             print("Hello")
#             if user_details.filter(user_id=user.id, expiry_date__lt=datetime.now(timezone.utc)).exists():
#                 print("***Hello***")
#                 messages.info(request, "Your payment has expired. Please renew your subscription.")
#                 CustomUser.login(request, user)
#                 return render(request, 'content_home1.html')
#             elif username == 'Admin':
#                 CustomUser.login(request, user)
#                 return render(request, 'content_home_admin.html')
#             elif user_details.filter(user_id=user.id, payment_status='paid').exists():
#                 print("%%%%%Hello")
#                 CustomUser.login(request, user)
#                 return render(request, 'content_home_student.html')
#             else:
#                 CustomUser.login(request, user)
#                 return render(request, 'content_home1.html')
#         else:
#             messages.info(request, "Invalid Credentials")
#             return redirect('registration_app:login')
#     else:
#         return render(request, 'login.html')
    #     if user is not None:
    #         # Check if the user's payment is paid
    #         if user_details.filter(user_id=user.id, payment_status='paid').exists():
    #             if user_details.filter(user_id=user.id, expiry_date__lt=datetime.now()).exists():
    #                 messages.info(request, "Your payment has expired. Please renew your subscription.")
    #                 return render(request, 'checkout.html')
    #             if username == 'Admin':
    #                 CustomUser.login(request, user)
    #                 return render(request, 'content_home_admin.html')
    #             else:
    #                 CustomUser.login(request, user)
    #                 return render(request, 'content_home1.html')
    #         else:
    #             messages.info(request, "Your payment is pending. Please complete your payment.")
    #             return render(request, 'checkout.html')
    #     else:
    #         messages.info(request, "Invalid Credentials")
    #         return redirect('registration_app:login')
    # else:
    #     return render(request, 'login.html')


# def registerchechi(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST.get('firstname')
#         last_name = request.POST.get('lastname')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         dob = request.POST.get('dob')
#         education = request.POST.get('education')
#         package = False
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')
#         if password == cpassword:
#             print("First")
#             if CustomUser.objects.filter(username=username).exists():
#                 messages.info(request, "Username Taken")
#                 return redirect('registration_app:register')
#             elif CustomUser.objects.filter(email=email).exists():
#                 messages.info(request, "Email Taken")
#                 return redirect('registration_app:register')
#             else:
#                 user = CustomUser.objects.create_user(username=username, email=email, password=password,
#                                                       first_name=first_name, last_name=last_name, dob=dob,
#                                                       education=education, phone=phone, package=package)
#                 print("User created")
#                 return redirect('registration_app:login')
#         else:
#             messages.info(request, "Password not Matching")
#             return redirect('registration_app:register')

#     return render(request, "registration.html")


def register(request):
    s_category=S_Category.objects.all().order_by('S_Category')
    states=States.objects.all().order_by('States')
    education=Education.objects.all().order_by('Education')
    context={'s_category':s_category, 'states':states,'education':education}
    if request.method=='POST':
        u_name=request.POST['username']
        f_Name=request.POST['fname']
        l_Name=request.POST['lname']
        dob=request.POST['dob']
        Mob=request.POST['phone']
        Email=request.POST['email']
        s_category=request.POST['s_category']
        S_Category_selected=S_Category.objects.get(S_Category=s_category)
        education=request.POST['education']
        Education_selected=Education.objects.get(Education=education)
        Password=request.POST['password']
        # Re_Password=request.POST['cpassword']
        states=request.POST['states']
        States_selected=States.objects.get(States=states)
        print(S_Category_selected)
        Register.objects.create(u_name=u_name,f_Name=f_Name,l_Name=l_Name,dob=dob,Mob=Mob,Email=Email,S_Category=S_Category_selected,Education=Education_selected,Password=Password,States=States_selected)
    return render(request,'registration.html',context)



def new_login(request):
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all().order_by('Education')
    context = {'s_category': s_category, 'states': states, 'education': education}

    if request.method == "POST":
        login_credential = request.POST.get('log_credential')
        password = request.POST.get('log_password')

        if login_credential and password:
            try:
                if '@' in login_credential:
                    user = Register.objects.get(Email=login_credential)
                else:
                    user = Register.objects.get(Mob=login_credential)
                
                # Manually authenticate by checking the password
                if user.Password == password:  # Assuming password is stored in plain text (not recommended)
                    request.session['u_name'] = user.u_name
                    request.session['u_fname'] = user.f_Name
                    request.session['u_email'] = user.Email
                    request.session['user_id'] = user.id
                    print("Session after login:", request.session)
                    return redirect('Scholarshipapp:allscholarship')  # Redirect to the homepage upon successful login
                else:
                    # Add an error message
                    messages.error(request, 'Incorrect Password!!!')
                    return redirect('registration_app:register')  # Redirect back to login page if login fails
            except Register.DoesNotExist:
                # Add an error message
                messages.error(request, 'User Does Not Exist!!!')
                return redirect('registration_app:register')  # Redirect back to login page if login fails
        else:
            # Add an error message
            messages.error(request, 'Please provide both email/mobile number and password.')
            return redirect('registration_app:register')  # Redirect back to login page if login fails

    return render(request, 'registration.html', context)


# try below view if not logined in
# def new_login(request):
#     s_category=S_Category.objects.all().order_by('S_Category')
#     states=States.objects.all().order_by('States')
#     education=Education.objects.all().order_by('Education')
#     context={'s_category':s_category, 'states':states,'education':education}
#     if request.method == "POST":
#         email = request.POST.get('log_email')
#         password = request.POST.get('log_password')
#         try:
#             user = Register.objects.get(Email=email, Password=password)
#             print("success")
#             request.session['u_name'] = user.u_name
#             request.session['u_fname'] = user.f_Name
#             request.session['u_email'] = user.Email
#             request.session['user_id'] = user.id
#             print("Session:", request.session.items())

#             return redirect('registration_app:home')  # Redirect to the homepage upon successful login
#         except Register.DoesNotExist:
#             print("nope")
#             return redirect('registration_app:register')  # Redirect back to login page if login fails
#     return render(request, 'registration.html',context)


def home(request):
    s_category=S_Category.objects.all().order_by('S_Category')
    states=States.objects.all().order_by('States')
    education=Education.objects.all().order_by('Education')
    context={'s_category':s_category, 'states':states,'education':education}
    return render(request, 'content_home.html',context)

def logout(request):
    request.session.flush()  # Clear all session data
    return redirect('registration_app:new_login')  # Redirect to login page


def createnew_password(request):
    return render(request, "update_password.html")


def update_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        # Check if the username exists in the database
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            print("Please enter a valid username")
            return render(request, "login.html")

        # Update the user's password
        user.set_password(new_password)
        user.save()

        return render(request, "login.html")
    else:
        return render(request, "update_password.html")
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # try:
    #     user = CustomUser.objects.get(username=username)
    # except CustomUser.DoesNotExist:
    #     print("Please enter a valid username")
    #     return render(request, "login.html")
    #
    #     # Update the user's password
    # user.set_password(password)
    # user.save()
    #
    # return render(request, "login.html")
    # # user_details = CustomUser.objects.all()
    # # user = CustomUser.objects.get(username=username)
    # # if user.filter(username=username).exists():
    # #     # CustomUser.objects.filter(username=username).update(
    # #     #     password=password,
    # #     # )
    # #     user.set_password(password)
    # #     user.save()
    # # else:
    # #     print("Please enter a valid username")
    # return render(request, "login.html")


# def process_payment(request):
#     if request.method == 'POST':
#         print("Entered****************************")
#         plan = request.POST.get('selectedPlan')
#         print(plan)
#         # form = PaymentForm(request.POST)
#         # if form.is_valid():
#         if plan is not None:
#             # amount = form.cleaned_data['amount']
#             amount_float = float(plan)
#             amount_rupees = int(amount_float * 100)
#             try:
#                 # Create a Stripe PaymentIntent
#                 payment_intent = stripe.PaymentIntent.create(
#                     amount=amount_rupees,  # Convert to rupee
#                     currency='inr',
#                     source=request.POST['stripeToken'],
#                     description='Payment description'
#                     # Add additional parameters as needed
#                 )
#                 return render(request, 'payment.html', {'client_secret': payment_intent.client_secret})
#             except Exception as e:
#                 return render(request, 'payment_error.html', {'error': str(e)})
#     else:
#         form = PaymentForm()
#     return render(request, 'payment_body-tmp.html', {'form': form})

def student_details(request):
    students = CustomUser.objects.all()
    return render(request, 'student_list.html', {'students': students})


def student_list(request):
    form = StudentFilterForm(request.GET)
    students = CustomUser.objects.exclude(username='Admin')

    # Filter students based on the selected education level
    education_level = request.GET.get('education_level')
    if education_level:
        students = students.filter(education=education_level)

    return render(request, 'student_lists.html', {'form': form, 'students': students})


# Payment view

# def payment_view(request):
#     return render(request, 'payment1.html', {'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
#
#
# @csrf_exempt
# def stripe_webhook(request):
#     # Handle Stripe webhook events here
#     payload = request.body
#     sig_header = request.headers['Stripe-Signature']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the event
#     if event.type == 'payment_intent.succeeded':
#         payment_intent = event.data.object  # contains a stripe.PaymentIntent
#         # Update your database or handle payment success here
#
#     return HttpResponse(status=200)
@csrf_exempt
def create_checkout_session(request):
    plan = request.POST.get('selectedPlan')  # Correct the field name
    uid = request.POST.get('userid')
    # plan = 10000
    if plan is not None:
        plan_amount = int(float(plan) * 100)
        # print(plan_amount)
        # print(plan_amount)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Package',
                    },
                    'unit_amount': plan_amount,
                },
                'quantity': 1,
            }],

            mode='payment',
            success_url='http://127.0.0.1:5000/success.html',  # Update with your actual URLs
            cancel_url='http://127.0.0.1:5000/cancel.html',  # Update with your actual URLs
        )
        pamt = plan_amount
        chk_senid = session.id
        dt = datetime.now()
        Payment_webhook.objects.create(user_id=uid, payment_amount=pamt, checkout_session_id=chk_senid, payment_date=dt)
    return redirect(session.url, code=303)

    # else:
    #     return JsonResponse({'error': 'No plan selected'})


# @csrf_exempt
# @login_required
# def update_package(request):
#     if request.method == 'POST':
#         user1 = request.user
#         user1.package = True
#         user1.save()
#         return JsonResponse({'message': 'User details updated successfully'})
#     return JsonResponse({'message': 'Invalid request method'}, status=405)
@csrf_exempt
def webhook_fun1(request):
    payload = request.body
    event = None

    try:
        stripe.api_key1 = 'whsec_EgnHBd9zvCx7nFj2k5Df1MlN8ZvmbdvM'
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key1
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    # ... handle other event types
    elif event.type == 'checkout.session.completed':
        # expiry_date = datetime.now() + datetime.timedelta(days=365)
        # payment_method = event.data.object  contains a stripe.PaymentMethod
        # print(event.data.object.id)
        # expiry_date = F('payment_date') + relativedelta(years=+1)
        expiry_date = datetime.now() + relativedelta(years=1)
        # payment_date = F('payment_date')
        # expiry_date = payment_date + relativedelta(years=1)
        print(expiry_date)
        details = Payment_webhook.objects.filter(checkout_session_id=event.data.object.id).update(
            payment_intent_id=event.data.object.payment_intent,
            payment_status=event.data.object.payment_status,
            expiry_date=expiry_date)
        # details.save()

        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


# def home(request):
#     return render(request, 'checkout.html')


# success view
def success(request):
    return render(request, 'success.html')
    # cancel view


def cancel(request):
    return render(request, 'cancel.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
