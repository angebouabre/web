from django.shortcuts import render

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView

from moniteur.models import *
#from django.views.generic import ListView, DetailView, TemplateView
#from django.db.models import Count
#from datetime import date, timedelta


class LocalisationView(ListView):
    model = Capteur 
    context_object_name = 'capteurs'
    template_name = 'localisations.html'

class DashBoardView(ListView):
    model = Carte 
    context_object_name = 'cartes'
    template_name = 'dashboard.html'

#    def get_context_data(self, **kwargs):

