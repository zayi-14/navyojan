# forms.py
from django import forms
from .models import Scholarship_category, Scholarship_item, Scholarship_details
from . import views





class ScholarshipaddForm(forms.ModelForm):
    class Meta:
        model = Scholarship_item
        exclude = ['pub_date', 'last_date']
        fields = ['name', 'pub_date', 'last_date', 'offered_by', 'price', 'state', 'category']


class ScholarshipcatForm(forms.ModelForm):
    class Meta:
        model = Scholarship_category
        fields = ['name', 'description', 'image']

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship_details
        fields = [
            'Scholarship_logo', 
            'Scholarship_name', 
            'Offered_by', 
            'Award', 
            'S_Category', 
            'Education', 
            'All_Scholarship', 
            'States', 
            'Published_date', 
            'Dead_line', 
            'Scholar_Description'
        ]
        widgets = {
            'S_Category': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
            'Education': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
            'All_Scholarship': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
            'States': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
            'Published_date': forms.DateInput(attrs={'class': 'form-control'}),
            'Dead_line': forms.DateInput(attrs={'class': 'form-control'}),
            'Scholar_Description': forms.Textarea(attrs={'class': 'form-control'}),
        }