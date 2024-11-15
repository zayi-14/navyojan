from django import forms
from .models import FAQ
from . import views


class FAQaddform(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
