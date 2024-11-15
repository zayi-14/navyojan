from django.shortcuts import render
from django.db import models
from Scholarshipapp.models import Scholarship_item
from django.db.models import Q
# Create your views here.

def SearchResult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        scholarships = Scholarship_item.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        return render(request, 'search.html', {'query': query, 'scholarships': scholarships})

