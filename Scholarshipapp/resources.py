# resources.py
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, DateTimeWidget
from .models import Scholarship_details, S_Category, All_Scholarship, States, Education, Eligibility

class Scholarship_detailsResource(resources.ModelResource):
    S_Category = fields.Field(
        column_name='S_Category',
        attribute='S_Category',
        widget=ManyToManyWidget(S_Category, field='S_Category')
    )
    All_Scholarship = fields.Field(
        column_name='All_Scholarship',
        attribute='All_Scholarship',
        widget=ManyToManyWidget(All_Scholarship, field='All_Scholarship')
    )
    States = fields.Field(
        column_name='States',
        attribute='States',
        widget=ManyToManyWidget(States, field='States')
    )
    Education = fields.Field(
        column_name='Education',
        attribute='Education',
        widget=ManyToManyWidget(Education, field='Education')
    )
    Published_date = fields.Field(
        column_name='Published_date',
        attribute='Published_date',
        widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S')
    )
    Dead_line = fields.Field(
        column_name='Dead_line',
        attribute='Dead_line',
        widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S')
    )

    class Meta:
        model = Scholarship_details
        fields = (
            'id', 'Scholarship_name', 'Offered_by', 'Award', 'Published_date', 
            'Dead_line', 'Scholar_Description', 'S_Category', 'All_Scholarship', 
            'States', 'Education'
        )
        export_order = (
            'id', 'Scholarship_name', 'Offered_by', 'Award', 'Published_date', 
            'Dead_line', 'Scholar_Description', 'S_Category', 'All_Scholarship', 
            'States', 'Education'
        )
