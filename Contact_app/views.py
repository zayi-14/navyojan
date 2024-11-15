from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django import forms
from Scholarshipapp.models import Register
from .models import Contact,ContactMessage
from Scholarshipapp.models import *
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.



def contact(request):
    print("contact page")

    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    try:
        user = Register.objects.get(id=user_id)  # Get user object using user_id
    except Register.DoesNotExist:
        user = None

    if request.method == 'POST':
        print("POST request received")

        message = request.POST.get('message')

        if message:
            # Create and save the ContactMessage
            ContactMessage.objects.create(user=user, message=message)
            return redirect('Contact_app:contact')  # Redirect to the contact page or wherever you want after submission

    # Fetch other data you need for rendering the page
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    scholar = Scholarship_details.objects.all().order_by('-id')
    context = {'s_category': s_category, 'states': states,'education':education, 'allscholarship': allscholarship, 'scholar': scholar, 'user': user}

    return render(request, 'Contact_us.html', context)

# def contact(request):
#     print("contact page")
#     s_category=S_Category.objects.all().order_by('S_Category')
#     states=States.objects.all().order_by('States')
#     allscholarship=All_Scholarship.objects.all().order_by('All_Scholarship')
#     scholar = Scholarship_details.objects.all().order_by('-id')
#     education = Education.objects.all()
#     context={'s_category':s_category, 'states':states,'allscholarship':allscholarship,'scholar':scholar,'education':education}
#     # if request.method == 'POST':
#     #     form = ContactForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         subject = "Welcome to Babysmile"
#     #         message = "Our team will contact you within 24hrs."
#     #         email_from = 'babysmileapp2024@gmail.com'
#     #         email = form.cleaned_data['email']
#     #         recipient_list = email
#     #         send_mail(subject, message, email_from, [recipient_list])
#     #         return render(request, 'success.html')
#     # form = ContactForm()
#     # context = {'form': form}
#     return render(request, 'Contact_us.html',context)



# def about(request):
#     return render(request,'About_us.html')