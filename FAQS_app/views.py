from django.shortcuts import render, get_object_or_404, redirect
from .models import FAQ
from django.contrib import messages
from .forms import FAQaddform
from django.urls import reverse


# Create your views here.

def addfaq(request):
    if request.method == 'POST':
        form = FAQaddform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry created successfully")
            # return redirect('faq_list')
            return render(request, 'AddFAQ.html')
    else:
        form = FAQaddform()
    return render(request, 'AddFAQ.html', {'form': form})


def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'FAQS.html', {'faqs': faqs})


