from django import forms


class StudentFilterForm(forms.Form):
    EDUCATION_CHOICES = (
        ('High School', 'High School'),
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
    )

    education_level = forms.ChoiceField(choices=EDUCATION_CHOICES, required=False)


# forms.py
# class PaymentForm(forms.Form):
#     amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
#     # Add other payment-related fields as needed




# class PaymentForm(forms.Form):
#     payment_amount = forms.DecimalField(label='Payment Amount', max_digits=10, decimal_places=2)

# forms.py

# from django import forms
# from .models import Registration
#
# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['username', 'email']
#
# class PaymentForm(forms.Form):
#     payment_amount = forms.DecimalField(label='Payment Amount', max_digits=10, decimal_places=2)
#     # Add other payment-related fields as needed
