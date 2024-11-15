from django.urls import path
from . import views


app_name = 'admin_app'

urlpatterns = [ 
                path('admindex',views.admindex,name='admindex'),
               
                path('scolar_disply/', views.scolar_disply, name='scolar_disply'),
                path('scholar_det_form',views.scholar_det_form,name='scholar_det_form'),
                path('eligibility_form',views.eligibility_form,name='eligibility_form'),
                path('eligibility-form-view/', views.eligibility_form_view, name='eligibility_form_view'),
                path('edit-eligibility-form/<int:pk>/', views.edit_eligibility_form, name='edit_eligibility_form'),
                path('delete-eligibility-form/<int:pk>/', views.delete_eligibility_form, name='delete_eligibility_form'),
                path('user_tables',views.user_tables,name='user_tables'),
                path('commeneted',views.commeneted,name='commeneted'),
                path('scholarship_detail_table',views.scholarship_detail_table,name='scholarship_detail_table'),
                path('export_scholarship_details/', views.export_scholarship_details_to_excel, name='export_scholarship_details'),
                path('scholarship/edit/<int:pk>/', views.edit_scholarship, name='edit_scholarship'),
                path('scholarships/add/', views.add_scholarship, name='add_scholarship'),
                path('confirm_delete/<int:pk>/', views.confirm_delete, name='confirm_delete'),
                path('categories/', views.category_list, name='category_list'),
                path('categories/add/', views.add_category, name='add_category'),
                path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
                path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
                path('states/', views.states_list, name='states_list'),
                path('states/add/', views.add_state, name='add_state'),
                path('states/edit/<int:pk>/', views.edit_states, name='edit_states'),
                path('states/delete/<int:pk>/', views.states_delete, name='states_delete'),
                path('education_list/', views.education_list, name='education_list'),
                path('education/add/', views.add_education, name='add_education'),
                path('education_list/edit/<int:pk>/', views.edit_education, name='edit_education'),
                path('education_list/delete/<int:pk>/', views.education_delete, name='education_delete'),
                path('exam_calender_view/', views.exam_calender_view, name='exam_calender_view'),
                path('exam_calender_view/edit/<int:pk>/', views.edit_exam, name='edit_exam'),
                path('exam_calender_view/delete/<int:pk>/', views.exam_delete, name='exam_delete'),
                # path('admin_register/', views.admin_register, name='admin_register'),
                path('admin_login/', views.admin_login, name='admin_login'),
                path('scholarship_detail/edit/<int:pk>', views.edit_scholarship_detail, name='edit_scholarship_detail'),
                path('scholarship_detail/<int:pk>/delete/', views.delete_scholarship_detail, name='delete_scholarship_detail'),
              
]