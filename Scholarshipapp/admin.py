from django.contrib import admin
from Scholarshipapp.models import *
from Contact_app.models import *
from import_export.admin import ImportExportModelAdmin
from .resources import Scholarship_detailsResource



admin.site.register(ContactMessage)
admin.site.register(S_Category)
admin.site.register(States)
admin.site.register(Education)
admin.site.register(All_Scholarship)

class Scholarship_detailsAdmin(ImportExportModelAdmin):
    resource_class = Scholarship_detailsResource

admin.site.register(Scholarship_details, Scholarship_detailsAdmin)


admin.site.register(Register)
admin.site.register(UserPlanScholarship)
admin.site.register(User_Plan)
admin.site.register(applied_scholarship)
admin.site.register(User_Profile)
admin.site.register(upcoming_scholarship)
admin.site.register(my_wishlist)
admin.site.register(Approval)
admin.site.register(exam_calender)