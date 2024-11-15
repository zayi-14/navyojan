from . import views
from django.urls import path, reverse

app_name = 'Scholarshipapp'

urlpatterns = [
    path('', views.allscholarship, name='allscholarship'),
    path('FAQS', views.faqs, name='FAQS'),
    path('addcat', views.addcat, name='addcat'),
    path('addscholarship', views.addscholarship, name='addscholarship'),
    path('scholar_page', views.scholar_page, name='scholar_page'),
    path('user_profile_page', views.user_profile_page, name='user_profile_page'),
    path('event',views.event,name='event'),
    path('wishlist_view',views.wishlist_view,name='wishlist_view'),
    path('wishlist/add/<int:scholarship_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:scholarship_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('apply_scholar/<int:scholarship_id>',views.apply_scholar,name='apply_scholar'),
    path('already_applied/', views.already_applied_view, name='already_applied_url'),
    path('edit_u_profile',views.edit_u_profile,name='edit_u_profile'),
    path('view_applied_scholarships',views.view_applied_scholarships,name='view_applied_scholarships'),
    path('my_plan_page',views.my_plan_page,name='my_plan_page'),
    path('scholar_page_premium',views.scholar_page_premium,name='scholar_page_premium'),
    path('choose_plan/<int:plan_id>/', views.choose_plan, name='choose_plan'),
    path('profile', views.profile, name='profile'),
    path('approval_status/<int:user_id>', views.approval_status, name='approval_status'),
    path('edit_profile_image/', views.edit_profile_image, name='edit_profile_image'),
    path('scholarship_list/', views.scholarship_list, name='scholarship_list'),

  ]
