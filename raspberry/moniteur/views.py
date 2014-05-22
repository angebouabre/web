from django.shortcuts import render
from django.db.models import Avg, Max, Min

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

class EntrepotDetailView(ListView):
    model = Capteur 
    context_object_name = 'capteurs'
    template_name = 'entrepot-detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntrepotDetailView, self).get_context_data(**kwargs)
       
        localisation = self.kwargs['localisation']
        capteurs = Capteur.objects.filter(localisation=localisation)
        
        mesures = Mesure.objects.filter(capteur__in=capteurs)
        for capteur in capteurs:
            capteur.mesures = mesures.filter(capteur=capteur)
            stats = capteur.mesures.aggregate(Avg('valeur'), Max('valeur'), Min('valeur'))
            capteur.mes_moy = stats['valeur__avg']
            capteur.mes_max = stats['valeur__max']
            capteur.mes_min = stats['valeur__min']
            print capteur, capteur.type_mesure
            print capteur.mesures 
            print stats
             
        context['capteurs'] = capteurs 
        context['localisation'] = localisation 
        return context


class CarteDetailView(DetailView):
    model = Carte
    context_object_name = 'carte'
    template_name = 'carte-detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(CarteDetailView, self).get_context_data(**kwargs)
        
        carte = self.kwargs['slug']
        print type(carte)
        carte = Carte.objects.filter(nom_carte=carte)
        capteurs = Capteur.objects.filter(carte=carte)
        

        context['capteurs'] = capteurs
        return context

