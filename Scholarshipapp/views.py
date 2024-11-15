from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ScholarshipaddForm, ScholarshipcatForm
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Scholarship_item, Scholarship_category
from Scholarshipapp.models import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware
import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
def allscholarship(request, c_slug=None):
    print("home")
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    scholar = Scholarship_details.objects.all().order_by('-id')
    xam = exam_calender.objects.all()
    context = {'s_category': s_category, 'states': states, 'education': education,
               'allscholarship': allscholarship, 'scholar': scholar, 'xam': xam}
    # c_page = None
    # scholarship_list = None
    # if c_slug != None:
    #     c_page = get_object_or_404(Scholarship_category, slug=c_slug)
    #     scholarship_list = Scholarship_item.objects.all().filter(category=c_page, available=True)

    # else:
    #     scholarship_list = Scholarship_item.objects.all().filter(category=True)
    user_id = request.session.get('user_id')
    # if user_id:
    #     user = Register.objects.get(pk=user_id)
    #     user_plan_scholarship = UserPlanScholarship.objects.filter(
    #         user=user).first()
    #     if user_plan_scholarship:
    #         if user_plan_scholarship.u_plan.plan_name == 'Standard':
    #             return redirect('Scholarshipapp:scholar_page_premium')
    #         elif user_plan_scholarship.u_plan.plan_name == 'Premium':
    #             return redirect('Scholarshipapp:scholar_page_premium')
    #     else:
    #         return redirect('Scholarshipapp:scholar_page')
    return render(request, "scholarshipdetail.html", context)
    # return render(request, "scholarshipdetail.html", {'category': c_page, 'scholarship_list': scholarship_list})


def ScholarDetail(request, c_slug, product_slug):
    try:
        scholarship_list = Scholarship_item.objects.get(
            category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'scholarship_items.html', {'scholarship_list': scholarship_list})


def faqs(request):
    return render(request, 'FAQS_app/FAQS.html')


def addcat(request):
    if request.method == 'POST':
        # name = request.POST['sname']
        # description = request.POST['criteria']
        # image = request.POST['image']
        form = ScholarshipcatForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success.html')
            messages.success(request, "Entry created successfully")
    else:
        form = ScholarshipcatForm()

    return render(request, 'Scholarship_catadd.html', {'form': form})


def addscholarship(request):
    if request.method == 'POST':
        # name = request.POST['name']
        # offered_by = request.POST['sponsor']
        # price = request.POST['price']
        # state = request.POST['state']

        pub_date = request.POST['pub_date']
        last_date = request.POST['last_date']

        form = ScholarshipaddForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.pub_date = pub_date
            instance.last_date = last_date
            instance.save()
            # return redirect('success.html')
            messages.success(request, "Entry created successfully")
    else:
        form = ScholarshipaddForm()

    return render(request, 'Scholarship_add.html', {'form': form})

def scholarship_list(request):
    current_datetime = now()
    current_time = timezone.now()

    scholarships = Scholarship_details.objects.filter(
        Dead_line__gte=current_time)
    for scholarship in scholarships:
        if scholarship.Dead_line:
            deadline = scholarship.Dead_line
            if not deadline.tzinfo:  # If deadline is timezone-naive, make it timezone-aware
                deadline = make_aware(deadline)
            time_left = deadline - current_datetime
            scholarship.days_left = time_left.days
        else:
            scholarship.days_left = None

    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    scholar = Scholarship_details.objects.all().order_by('-id')


    scholarship_name = request.GET.get('scholarship_name')
    deadline = request.GET.get('deadline')

    if scholarship_name:
        scholarships = scholarships.filter(Scholarship_name__icontains=scholarship_name)
    
    if deadline:
        scholarships = scholarships.filter(Dead_line=deadline)

    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    scholar = Scholarship_details.objects.all().order_by('-id')    

    context = {
        
        'scholarships': scholarships,'s_category': s_category, 'education': education,
               'states': states, 'allscholarship': allscholarship,
        'request': request  # Pass the request to context to pre-fill form fields
    }

    # Check if the Clear button was clicked
    if 'clear' in request.GET:
      return redirect(request.path)
 
    return render(request, 'scholar_page.html', context)



def scholar_page(request):
    categories = request.GET.getlist('category')
    states = request.GET.getlist('state')
    all_scholarships = request.GET.getlist('all_scholarship')
    educations = request.GET.getlist('education')

    current_time = timezone.now()
    # Exclude scholarships whose deadline has passed
    scholarships = Scholarship_details.objects.filter(
        Dead_line__gte=current_time)
    # scholarships = Scholarship_details.objects.all()

    if categories:
        category_filters = Q()
        for category in categories:
            category_filters |= Q(S_Category__S_Category=category)
        scholarships = scholarships.filter(category_filters)

    if states:
        state_filters = Q()
        for state in states:
            state_filters |= Q(States__States=state)
        scholarships = scholarships.filter(state_filters)
        print(scholarships)
    if all_scholarships:
        all_scholarship_filters = Q()
        for all_scholarship in all_scholarships:
            all_scholarship_filters |= Q(
                All_Scholarship__All_Scholarship=all_scholarship)
        scholarships = scholarships.filter(all_scholarship_filters)
        print(scholarships)

    if educations:
        education_filters = Q()
        for education in educations:
            education_filters |= Q(Education__Education=education)
        scholarships = scholarships.filter(education_filters)

    current_datetime = now()

    for scholarship in scholarships:
        if scholarship.Dead_line:
            deadline = scholarship.Dead_line
            if not deadline.tzinfo:  # If deadline is timezone-naive, make it timezone-aware
                deadline = make_aware(deadline)
            time_left = deadline - current_datetime
            scholarship.days_left = time_left.days
        else:
            scholarship.days_left = None

    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    scholar = Scholarship_details.objects.all().order_by('-id')

    context = {'scholarships': scholarships, 's_category': s_category, 'education': education,
               'states': states, 'allscholarship': allscholarship}
    return render(request, 'scholar_page.html', context)


# def scholar_list(request):
#     s_category=S_Category.objects.all().order_by('S_Category')
#     states=States.objects.all().order_by('States')
#     allscholarship=All_Scholarship.objects.all().order_by('All_Scholarship')
#     context={'s_category':s_category, 'states':states,'allscholarship':allscholarship}
#     return render(request, 'scholar_page.html', context)

def scholar_page_premium(request):
    categories = request.GET.getlist('category')
    states = request.GET.getlist('state')
    all_scholarships = request.GET.getlist('all_scholarship')
    educations = request.GET.getlist('education')

    current_time = timezone.now()
    # Exclude scholarships whose deadline has passed
    scholarships = Scholarship_details.objects.filter(
        Dead_line__gte=current_time)
    # scholarships = Scholarship_details.objects.all()

    if categories:
        category_filters = Q()
        for category in categories:
            category_filters |= Q(S_Category__S_Category=category)
        scholarships = scholarships.filter(category_filters)

    if states:
        state_filters = Q()
        for state in states:
            state_filters |= Q(States__States=state)
        scholarships = scholarships.filter(state_filters)
        print(scholarships)
    if all_scholarships:
        all_scholarship_filters = Q()
        for all_scholarship in all_scholarships:
            all_scholarship_filters |= Q(
                All_Scholarship__All_Scholarship=all_scholarship)
        scholarships = scholarships.filter(all_scholarship_filters)
        print(scholarships)

    if educations:
        education_filters = Q()
        for education in educations:
            education_filters |= Q(Education__Education=education)
        scholarships = scholarships.filter(education_filters)

    current_datetime = now()

    for scholarship in scholarships:
        if scholarship.Dead_line:
            deadline = scholarship.Dead_line
            if not deadline.tzinfo:  # If deadline is timezone-naive, make it timezone-aware
                deadline = make_aware(deadline)
            time_left = deadline - current_datetime
            scholarship.days_left = time_left.days
        else:
            scholarship.days_left = None
    upcoming_scholar = upcoming_scholarship.objects.all()
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    context = {'scholarships': scholarships, 'upcoming_scholar': upcoming_scholar,
               's_category': s_category, 'states': states, 'education': education, 'allscholarship': allscholarship}
    return render(request, 'scholar_page_premium.html', context)


def user_profile_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    try:
        user = Register.objects.get(id=user_id)
        user_profile = User_Profile.objects.get(user=user)
    except Register.DoesNotExist:
        # Redirect to login if user not found
        return redirect('registration_app:new_login')
    except User_Profile.DoesNotExist:
        return redirect('Scholarshipapp:profile')
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'user_profile_page.html', context)


def edit_profile_image(request):
    user_profile = None
    user_profile_id = request.GET.get('user_profile_id')
    if user_profile_id:
        try:
            user_profile = User_Profile.objects.get(id=user_profile_id)
        except User_Profile.DoesNotExist:
            print("User profile not found for ID:",
                  user_profile_id)  # Debug statement
            user_profile = None
    else:
        print("No user_profile_id provided in the request!")  # Debug statement

    if request.method == 'POST':
        u_image = request.FILES.get('u_image')
        if u_image and user_profile:
            print("Received image:", u_image.name)  # Debug statement
            # Save image to filesystem
            fs = FileSystemStorage()
            filename = fs.save(u_image.name, u_image)
            print("File saved as:", filename)  # Debug statement
            # Update user_profile with new image
            user_profile.u_image = filename
            user_profile.save()

            
            print("Profile image updated successfully!")  # Debug statement
            return redirect('Scholarshipapp:user_profile_page')
        else:
            # Debug statement
            print("No image provided or user profile not found!")
            return render(request, 'edit_profile_image.html', {'user_profile': user_profile, 'error': 'No image provided or user profile not found'})

    return render(request, 'edit_profile_image.html', {'user_profile': user_profile})


def event(request):
    return render(request, 'event.html')

# def profile(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('registration_app:register')  # Redirect to login if not logged in
#     try:
#         user = Register.objects.get(id=user_id)
#     except Register.DoesNotExist:
#         return redirect('registration_app:new_login')  # Redirect to login if user not found
#     return render(request, 'profile.html', {'user': user})


# def profile(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('registration_app:new_login')  # Redirect to login if not logged in

#     try:
#         user = Register.objects.get(id=user_id)
#         # Check if the profile exists
#         user_profile = User_Profile.objects.get(user=user)
#         return redirect('Scholarshipapp:edit_profile')  # Redirect to edit_profile if profile exists
#     except Register.DoesNotExist:
#         return redirect('registration_app:new_login')  # Redirect to login if user not found
#     except User_Profile.DoesNotExist:
#         pass  # Proceed to profile creation if profile does not exist

#     if request.method == 'POST':
#         print("POST request received")
#         # Update Register model fields
#         user.f_Name = request.POST['f_name']
#         user.l_Name = request.POST['l_name']
#         user.dob = request.POST['dob']
#         user.Mob = request.POST['phone']
#         user.Email = request.POST['email']
#         user.Education = request.POST['education']
#         user.S_Category = request.POST['category']
#         user.save()

#         # Create and save the UserProfile
#         address = request.POST['address']
#         father_name = request.POST['father_name']
#         father_phone = request.POST['father_phone']
#         mother_name = request.POST['mother_name']
#         mother_phone = request.POST['mother_phone']
#         image=request.FILES['image']
#         certificate=request.FILES['certificate']
#         print(user.S_Category,father_name)
#         # User_Profile.objects.create(user=user, address=address, phone=phone)
#         return redirect('Scholarshipapp:edit_profile')  # Redirect to edit_profile after creating profile
#     return render(request, 'profile.html', {'user': user})


def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    try:
        user = Register.objects.get(id=user_id)
        # Check if the profile exists
        user_profile = User_Profile.objects.get(user=user)
        # Redirect to edit_profile if profile exists
        return redirect('Scholarshipapp:user_profile_page')
    except Register.DoesNotExist:
        # Redirect to login if user not found
        return redirect('registration_app:new_login')
    except User_Profile.DoesNotExist:
        pass  # Proceed to profile creation if profile does not exist

    if request.method == 'POST':
        print("POST request received")

        address = request.POST['address']
        father_name = request.POST['father_name']
        father_phone = request.POST['father_phone']
        mother_name = request.POST['mother_name']
        mother_phone = request.POST['mother_phone']
        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')

        # Create and save the UserProfile
        user_profile = User_Profile.objects.create(
            user=user,
            address=address,
            u_father=father_name,
            u_f_mob=father_phone,
            u_mother=mother_name,
            u_m_mob=mother_phone,
            u_image=image,
            u_certificate=certificate
        )

        # Save the selected plan
        plan_id = request.POST.get('plan_id')
        print(f"Selected plan_id: {plan_id}")
        if plan_id:
            try:
                selected_plan = User_Plan.objects.get(id=plan_id)
                UserPlanScholarship.objects.create(
                    user=user, u_plan=selected_plan)
            except Plan.DoesNotExist:
                print("Plan not found")  # Handle plan not found scenario

        # Redirect to edit_profile after creating profile
        return redirect('Scholarshipapp:user_profile_page')

    plans = User_Plan.objects.all()
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    return render(request, 'profile.html', {'user': user, 'plans': plans, 's_category': s_category, 'states': states, 'allscholarship': allscholarship})


# "below is crt code"
# def profile(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('registration_app:new_login')  # Redirect to login if not logged in

#     try:
#         user = Register.objects.get(id=user_id)
#         # Check if the profile exists
#         user_profile = User_Profile.objects.get(user=user)
#         return redirect('Scholarshipapp:edit_u_profile')  # Redirect to edit_profile if profile exists
#     except Register.DoesNotExist:
#         return redirect('registration_app:new_login')  # Redirect to login if user not found
#     except User_Profile.DoesNotExist:
#         pass  # Proceed to profile creation if profile does not exist

#     if request.method == 'POST':
#         print("POST request received")

#         # Update Register model fields
#         # user.f_Name = request.POST['f_name']
#         # user.l_Name = request.POST['l_name']
#         # user.dob = request.POST['dob']
#         # user.Mob = request.POST['phone']
#         # user.Email = request.POST['email']

#         # Retrieve and assign the selected education
#         # education_id = request.POST['education']
#         # try:
#         #     education_selected = Education.objects.get(pk=education_id)
#         #     user.Education = education_selected
#         # except Education.DoesNotExist:
#         #     pass  # Handle this appropriately

#         # # Retrieve and assign the selected category
#         # category_id = request.POST['category']
#         # try:
#         #     category_selected = S_Category.objects.get(pk=category_id)
#         #     user.S_Category = category_selected
#         # except S_Category.DoesNotExist:
#         #     pass  # Handle this appropriately

#         # user.save()

#         # Create and save the UserProfile
#         address = request.POST['address']
#         father_name = request.POST['father_name']
#         father_phone = request.POST['father_phone']
#         mother_name = request.POST['mother_name']
#         mother_phone = request.POST['mother_phone']
#         image = request.FILES.get('image')
#         certificate = request.FILES.get('certificate')

#         print(mother_name)
#         User_Profile.objects.create(
#             user=user,
#             address=address,
#             u_father=father_name,
#             u_f_mob=father_phone,
#             u_mother=mother_name,
#             u_m_mob=mother_phone,
#             u_image=image,
#             u_certificate=certificate
#         )

#         return redirect('Scholarshipapp:edit_u_profile')  # Redirect to edit_profile after creating profile

#     return render(request, 'profile.html', {'user': user})


# def edit_profile(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('registration_app:login')  # Redirect to login if not logged in

#     try:
#         user = Register.objects.get(id=user_id)
#         user_profile = UserProfile.objects.get(user=user)
#     except Register.DoesNotExist:
#         return redirect('registration_app:login')  # Redirect to login if user not found
#     except UserProfile.DoesNotExist:
#         return redirect('registration_app:profile')  # Redirect to profile creation if profile does not exist

#     if request.method == 'POST':
#         user_profile.address = request.POST['address']
#         user_profile.phone = request.POST['phone']
#         # Update other profile fields as necessary
#         user_profile.save()
#         return redirect('registration_app:edit_profile')  # Redirect to edit_profile after saving

#     return render(request, 'edit_profile.html', {'user_profile': user_profile})

def edit_u_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    try:
        user = Register.objects.get(id=user_id)
        user_profile = User_Profile.objects.get(user=user)
    except Register.DoesNotExist:
        # Redirect to login if user not found
        return redirect('registration_app:new_login')
    except User_Profile.DoesNotExist:
        # Redirect to profile creation if profile does not exist
        return redirect('Scholarshipapp:profile')

    if request.method == 'POST':
        # Update Register model fields
        user.f_Name = request.POST['f_name']
        user.l_Name = request.POST['l_name']
        user.dob = request.POST['dob']
        user.Mob = request.POST['mob']
        user.save()

        # Update UserProfile fields
        user_profile.address = request.POST['address']
        user_profile.phone = request.POST['phone']
        user_profile.save()

        # Redirect to edit_profile after saving
        return redirect('Scholarshipapp:edit_u_profile')

    return render(request, 'edit_u_profile.html', {'user_profile': user_profile, 'user': user})


def my_plan_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    user = get_object_or_404(Register, id=user_id)
    user_profile = User_Profile.objects.get(user=user)

    user_plan = UserPlanScholarship.objects.filter(user=user).first()
    plans = User_Plan.objects.all()

    print("User Plan:", user_plan)  # Debug statement

    context = {
        'user': user,
        'user_plan': user_plan,
        'plans': plans,
        'user_profile': user_profile,
    }

    return render(request, 'my_plan_page.html', context)


def choose_plan(request, plan_id):
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if not logged in
        return redirect('registration_app:new_login')

    user = get_object_or_404(Register, id=user_id)
    selected_plan = get_object_or_404(User_Plan, id=plan_id)

    # Get the existing UserPlanScholarship object if it exists
    user_plan = UserPlanScholarship.objects.filter(user=user).first()

    if user_plan:
        # Update the existing UserPlanScholarship object with the selected plan
        user_plan.plan = selected_plan
        user_plan.save()
    else:
        # If no existing UserPlanScholarship object exists, create a new one
        UserPlanScholarship.objects.create(
            user=user,
            plan=selected_plan
        )

    return redirect('Scholarshipapp:my_plan_page')


# def apply_scholar(request, scholarship_id):
#     if request.method == 'POST':
#         scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
#         if request.user.is_authenticated:  # Check if user is logged in
#             try:
#                 register_instance = Register.objects.get(u_name=request.user.username)
#             except Register.DoesNotExist:
#                 # Handle the case where the Register instance does not exist
#                 return redirect('Scholarshipapp:profile')  # Redirect to profile creation page

#             # Check if the user has already applied for this scholarship
#             if applied_scholarship.objects.filter(user=register_instance, scholarship=scholarship).exists():
#                 return redirect('Scholarshipapp:already_applied_url')

#             # Create applied_scholarship instance and save
#             applied_instance = applied_scholarship(user=register_instance, scholarship=scholarship)
#             applied_instance.save()

#             return redirect('Scholarshipapp:user_profile_page')  # Redirect to user panel or a success page
#         else:
#             return redirect('registration_app:new_login')  # Redirect to custom login page if user is not logged in

#     # If the request method is not POST, render the apply_scholar.html template
#     return render(request, 'apply_scholar.html', {'scholarship_id': scholarship_id})

# def apply_scholar(request, scholarship_id):
#     print("Apply Scholar view called")  # Debugging statement

#     scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
#     print("Scholarship found:", scholarship)  # Debugging statement

#     if 'user_id' not in request.session:
#         # Redirect to custom login page if user is not logged in
#         return redirect('registration_app:new_login')

#     user_id = request.session['user_id']
#     user = Register.objects.get(pk=user_id)

#     # Check if the user has created a profile
#     if not User_Profile.objects.filter(user=user).exists():
#         # Redirect to profile creation page if profile is not complete
#         return redirect('Scholarshipapp:profile')

#     # Check if the user has already applied for this scholarship
#     already_applied = applied_scholarship.objects.filter(
#         user=user, scholarship=scholarship).exists()
#     in_wishlist = my_wishlist.objects.filter(
#         user=user, scholarships=scholarship).exists()

#     # Check for referrer
#     referrer_id = request.GET.get('referrer')
#     if referrer_id:
#         referrer = get_object_or_404(Register, id=referrer_id)
#         referral, created = Referral.objects.get_or_create(
#             referrer=referrer, referred_email=user.Email, scholarship=scholarship)
#         print(f"Referral created: {created}, Referrer: {referrer}, Referred Email: {
#               user.Email}, Scholarship: {scholarship}")  # Debugging statement

#     if request.method == 'POST':
#         if not already_applied:
#             print("POST request received")  # Debugging statement

#             try:
#                 applied_instance = applied_scholarship(
#                     user=user, scholarship=scholarship)
#                 applied_instance.save()
#                 print("Applied scholarship saved to the database:",
#                       applied_instance)  # Debugging statement

#                 # Update referral status if applicable
#                 if referrer_id:
#                     referral.is_successful = True
#                     referral.referred_user = user
#                     referral.save()
#                     print(f"Referral marked as successful: {
#                           referral}")  # Debugging statement

#                 messages.success(
#                     request, 'Scholarship applied successfully. Check your profile.')
#                 # Redirect to user panel or a success page
#                 return redirect('Scholarshipapp:scholar_page')
#             except Exception as e:
#                 # Debugging statement
#                 print("Error occurred while saving applied scholarship:", e)
#                 messages.error(
#                     request, 'An error occurred while applying for the scholarship.')
#         else:
#             # Debugging statement
#             print("User has already applied for this scholarship.")
#             messages.info(
#                 request, 'You have already applied for this scholarship.')

#     s_category = S_Category.objects.all().order_by('S_Category')
#     states = States.objects.all().order_by('States')
#     allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
#     context = {'states': states, 'allscholarship': allscholarship, 's_category': s_category,
#                'scholarship': scholarship, 'already_applied': already_applied, 'in_wishlist': in_wishlist}
#     return render(request, 'apply_scholar.html', context)

def apply_scholar(request, scholarship_id):
    s_category = S_Category.objects.all().order_by('S_Category')
    states = States.objects.all().order_by('States')
    education = Education.objects.all()
    allscholarship = All_Scholarship.objects.all().order_by('All_Scholarship')
    print("Apply Scholar view called")  # Debugging statement

    scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
    print("Scholarship found:", scholarship)  # Debugging statement

    if 'user_id' not in request.session:
        return redirect('registration_app:new_login')  # Redirect to custom login page if user is not logged in

    user_id = request.session['user_id']
    user = Register.objects.get(pk=user_id)

    # Check if the user has created a profile
    if not User_Profile.objects.filter(user=user).exists():
        return redirect('Scholarshipapp:profile')  # Redirect to profile creation page if profile is not complete

    # Check if the user has chosen a plan
    # if not UserPlanScholarship.objects.filter(user=user).exists():
    #     return redirect('Scholarshipapp:choose_plan')

     # Check if the user has already applied for this scholarship
    already_applied = applied_scholarship.objects.filter(user=user, scholarship=scholarship).exists()
    in_wishlist = my_wishlist.objects.filter(user=user, scholarships=scholarship).exists()

    if request.method == 'POST':
        if not already_applied:
            print("POST request received")  # Debugging statement

            try:
                applied_instance = applied_scholarship(user=user, scholarship=scholarship)
                applied_instance.save()
                print("Applied scholarship saved to the database:", applied_instance)  # Debugging statement

                return redirect('Scholarshipapp:scholar_page')  # Redirect to user panel or a success page
            except Exception as e:
                print("Error occurred while saving applied scholarship:", e)  # Debugging statement
                # Handle the error, maybe redirect to an error page or render a template with an error message
        else:
            print("User has already applied for this scholarship.")  # Debugging statement

    return render(request, 'apply_scholar.html', {'scholarship': scholarship, 'already_applied': already_applied,'in_wishlist': in_wishlist,'s_category': s_category, 'states': states, 'education': education,
               'allscholarship': allscholarship})

#  use below code if not working
# def apply_scholar(request, scholarship_id):
#     print("Apply Scholar view called")  # Debugging statement

#     scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
#     print("Scholarship found:", scholarship)  # Debugging statement

#     if 'user_id' not in request.session:
#         return redirect('registration_app:new_login')  # Redirect to custom login page if user is not logged in

#     if request.method == 'POST':
#         print("POST request received")  # Debugging statement

#         try:
#             user_id = request.session['user_id']
#             user = Register.objects.get(pk=user_id)
#             print("Current user:", user)  # Debugging statement

#             applied_instance = applied_scholarship(user=user, scholarship=scholarship, applied_on=timezone.now())
#             applied_instance.save()
#             print("Applied scholarship saved to the database:", applied_instance)  # Debugging statement

#             return redirect('Scholarshipapp:user_profile_page')  # Redirect to user panel or a success page
#         except Exception as e:
#             print("Error occurred while saving applied scholarship:", e)  # Debugging statement
#             # Handle the error, maybe redirect to an error page or render a template with an error message

#     return render(request, 'apply_scholar.html', {'scholarship': scholarship})


def already_applied_view(request):
    return render(request, 'already_applied.html')


def view_applied_scholarships(request):
    print("View Applied Scholarships called")  # Debugging statement

    if 'user_id' not in request.session:
        # Redirect to login if not authenticated
        return redirect('registration_app:new_login')

    user_id = request.session['user_id']
    current_user = Register.objects.get(pk=user_id)
    print("Current user:", current_user)  # Debugging statement

    applied_scholarships = applied_scholarship.objects.filter(
        user=current_user)
    print("Applied scholarships:", applied_scholarships)  # Debugging statement

    user = get_object_or_404(Register, id=user_id)
    user_profile = User_Profile.objects.get(user=user)

    context = {
        'applied_scholarships': applied_scholarships, 'user': user, 'user_profile': user_profile
    }

    return render(request, 'applied_scholarship.html', context)

# def apply_for_scholarship(request, scholarship_id):
#     user = request.user
#     scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)

#     # Check if user has already applied
#     if applied_scholarship.objects.filter(user=user, scholarship=scholarship).exists():
#         # Handle the case where the user has already applied
#         return redirect('regisration_app:home', scholarship_id=scholarship_id)

#     # Apply for the scholarship
#     applied_scholarship.objects.create(user=user, scholarship=scholarship)
#     return redirect('Scholarshipapp:user_profile_page')


def wishlist_view(request):
    print("Wishlist view called")

    if 'user_id' not in request.session:
        return redirect('registration_app:new_login')

    user_id = request.session['user_id']
    user = Register.objects.get(pk=user_id)

    try:
        wishlist, created = my_wishlist.objects.get_or_create(user=user)
        current_time = timezone.now()
        scholarships = wishlist.scholarships.filter(
            Dead_line__gte=current_time)
        print("Wishlist found:", scholarships)
    except Exception as e:
        print("Error occurred while fetching wishlist:", e)
        scholarships = None

    user_profile = User_Profile.objects.get(user=user)

    return render(request, 'my_wishlist.html', {'scholarships': scholarships, 'user': user, 'user_profile': user_profile})


def add_to_wishlist(request, scholarship_id):
    print("Add to Wishlist view called")

    if 'user_id' not in request.session:
        return redirect('registration_app:new_login')

    user_id = request.session['user_id']
    user = Register.objects.get(pk=user_id)
    scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
    print("Scholarship found:", scholarship)

    try:
        wishlist, created = my_wishlist.objects.get_or_create(user=user)
        wishlist.scholarships.add(scholarship)
        print("Scholarship added to wishlist:", scholarship)
        return redirect('Scholarshipapp:wishlist_view')
    except Exception as e:
        print("Error occurred while adding to wishlist:", e)

    return redirect('Scholarshipapp:wishlist_view')


def remove_from_wishlist(request, scholarship_id):
    print("Remove from Wishlist view called")

    if 'user_id' not in request.session:
        return redirect('registration_app:new_login')

    user_id = request.session['user_id']
    user = Register.objects.get(pk=user_id)
    scholarship = get_object_or_404(Scholarship_details, id=scholarship_id)
    print("Scholarship found:", scholarship)

    try:
        wishlist = my_wishlist.objects.get(user=user)
        wishlist.scholarships.remove(scholarship)
        print("Scholarship removed from wishlist:", scholarship)
        return redirect('Scholarshipapp:wishlist_view')
    except my_wishlist.DoesNotExist:
        print("Wishlist does not exist for user:", user)
    except Exception as e:
        print("Error occurred while removing from wishlist:", e)

    return redirect('Scholarshipapp:wishlist_view')


def approval_status(request, user_id):
    # Retrieve the user based on user_id
    user = Register.objects.get(pk=user_id)

    # Filter approvals for the specific user
    approvals = Approval.objects.filter(user=user)

    user_profile = User_Profile.objects.get(user=user)

    context = {
        'user': user,
        'approvals': approvals,
        'user_profile': user_profile,
    }
    return render(request, 'approval_status.html', context)
