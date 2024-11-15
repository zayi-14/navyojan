from django.urls import path
from . import views


app_name = 'registration_app'

urlpatterns = [

    path('register', views.register, name='register'),
    path('new_login', views.new_login, name='new_login'),
    path('', views.home, name='home'),
    path('createnew_password', views.createnew_password, name='createnew_password'),
    path('update_password', views.update_password, name='update_password'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success.html/', views.success, name='success'),
    path('cancel.html/', views.cancel, name='cancel'),
    path('student_details', views.student_details, name='student_details'),
    path('student_lists', views.student_list, name='student_list'),
    path('logout/', views.logout, name='logout'),
    path('webhook', views.webhook_fun1, name='webhook_fun1'),

]
