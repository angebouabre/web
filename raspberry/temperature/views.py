from django.shortcuts import render

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from temperature.models import Temperature
from django.views.generic import ListView, DetailView
from django.db.models import Count
from datetime import date, timedelta



class TemperatureList(ListView):
    
    model = Temperature
    context_object_name = 'temperatures_list'
    template_name = 'temperatures.html'
    paginate_by = 25
    queryset = Temperature.objects.all().order_by('-date_time')
