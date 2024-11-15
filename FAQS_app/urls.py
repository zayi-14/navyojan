from django.urls import path
from .views import addfaq, faq_list
from . import views

app_name = 'FAQS_app'

urlpatterns = [
    path('faqs/', views.faq_list, name='faq_list'),
    path('addfaq/', views.addfaq, name='addfaq'),
  
]
