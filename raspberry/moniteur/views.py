#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Avg, Max, Min

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView

from moniteur.models import *
#from django.views.generic import ListView, DetailView, TemplateView
#from django.db.models import Count
#from datetime import date, timedelta

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse


import nmap
import subprocess

import os
import sys 

#subprocess.check_call(["python","/home/bouable/esigetel/web/raspberry/raspberry/dmon.py","&"])

class LocalisationView(ListView):
    model = Capteur 
    context_object_name = 'capteurs'
    template_name = 'localisations.html'

class EntrepotDetailView(ListView):
    #TODO Filter by date or last number of measures
    model = Capteur 
    context_object_name = 'capteurs'
    template_name = 'entrepot-detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntrepotDetailView, self).get_context_data(**kwargs)
         
        localisation = self.kwargs['localisation']
        capteurs = Capteur.objects.filter(localisation=localisation)
         
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        st = start_date
        en = end_date


        st1 = start_date
        st2 = end_date
        
        if start_date and end_date:
            st_date = start_date.split(' ')[0]
            st_time = start_date.split(' ')[1]
            start_date = str(st_date.split('/')[2]+'-'+st_date.split('/')[1]+'-'+st_date.split('/')[0]+' '+st_time)

            en_date = end_date.split(' ')[0]
            en_time = end_date.split(' ')[1]
            end_date = str(en_date.split('/')[2]+'-'+en_date.split('/')[1]+'-'+en_date.split('/')[0]+' '+en_time)
            mesures = Mesure.objects.filter(capteur__in=capteurs, date_mesure__range=(start_date,end_date))
        else:
            hour = (datetime.now() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")
            now = datetime.now().strftime("%d/%m/%Y %H:%M") 
            
            mesures = Mesure.objects.filter(capteur__in=capteurs) #TODO filter mesures in range from hour to now



        for capteur in capteurs:
            capteur.mesures = mesures.filter(capteur=capteur)
            capteur.last_mesure = capteur.mesures.last()

        #for mesure in mesures:
        #    print mesure.capteur, mesure.capteur.type_mesure, mesure.valeur
       

        hour = (datetime.now() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")
        twelve = (datetime.now() - timedelta(hours=12)).strftime("%d/%m/%Y %H:%M")
        twenty_four = (datetime.now() - timedelta(hours=24)).strftime("%d/%m/%Y %H:%M")
        week = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y %H:%M")
        month = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y %H:%M")
        year = (datetime.now() - timedelta(days=365)).strftime("%d/%m/%Y %H:%M")
       

        context['hour'] = hour 
        context['twelve'] = twelve
        context['twenty_four'] = twenty_four
        context['week'] = week
        context['month'] = month
        context['year'] = year
        

        if st1 == twelve:
            context['start_date'] = twelve 
        elif st1 == twenty_four: 
            context['start_date'] = twenty_four
        elif st1 == week: 
            context['start_date'] = week
        elif st1 == month: 
            context['start_date'] = month
        elif st1 == year: 
            context['start_date'] = year
        else:
            context['start_date'] = hour 

        context['end_date'] = datetime.now().strftime("%d/%m/%Y %H:%M") 
        
        context['mesures'] = mesures
        context['capteurs'] = capteurs 
        context['localisation'] = localisation 
        return context


class CapteurDetailView(DetailView):
    #TODO Filter by date or last number of measures
    model = Capteur
    context_object_name = 'capteur'
    template_name = 'capteur-detail.html'

    def get_context_data(self, **kwargs):
        context = super(CapteurDetailView, self).get_context_data(**kwargs)
        
        capteur = self.kwargs['slug']
        capteur = Capteur.objects.get(slug=capteur)
        
        mesures = Mesure.objects.filter(capteur=capteur)
        stats = mesures.aggregate(Avg('valeur'), Max('valeur'), Min('valeur'))
        
        capteur.mes_moy = stats['valeur__avg']
        capteur.mes_max = stats['valeur__max']
        capteur.mes_min = stats['valeur__min']
        capteur.last_mesure = mesures.last()
       
        context['capteur'] = capteur 
        context['mesures'] = mesures.order_by('-date_mesure')[:5]
        return context
       






class CarteListView(ListView):
    model = Carte
    context_object_name = 'cartes'
    template_name = 'cartes-list.html'

    def get_context_data(self, **kwargs):
        context = super(CarteListView, self).get_context_data(**kwargs)

 
        try:
            cur =  os.getcwd()
            nmap_info_file = cur+"/moniteur/info.txt"
            openedFile = open(nmap_info_file)
        
            mac = None
            for line in openedFile:
                if 'MAC_ADDRESS=' in line:
                    carte = Carte()
                    mac = line.split('=')[1].rstrip()
                    carte.nom_carte = mac.replace(":","_")
                    carte.mac = mac
                    carte.is_activated = False
                    if carte.nom_carte != "None" and str(carte.mac).lower().replace(" ","") != "00:17:33:31:6f:c8":
                        carte.save()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass
        

        context['hosts'] = "" 
        return context




class CarteDetailView(DetailView):
    model = Carte
    context_object_name = 'carte'
    template_name = 'carte-detail.html'

    def post(self, request, *args, **kwargs):
        carte = self.kwargs['slug']
        carte = Carte.objects.get(nom_carte=carte)
        #self.object = self.get_object() 
        carte.nom_carte = self.request.POST.get('nom_carte')
        carte.type_carte = self.request.POST.get('type_carte')
        carte.mac = self.request.POST.get('mac')
        carte.memoire_disque = self.request.POST.get('memoire_disque')
        carte.is_activated = self.request.POST.get('is_activated', False)
        carte.save() 
 
        return HttpResponseRedirect("/mesure/carte/%s" %carte.nom_carte)             
 
    def get_context_data(self, **kwargs):
        context = super(CarteDetailView, self).get_context_data(**kwargs)
        
        carte = self.kwargs['slug']
        carte = Carte.objects.get(nom_carte=carte)
        capteurs = Capteur.objects.filter(carte=carte)
         
        carte.status = "down"  #Initialize status and ip to down and None
        carte.ip = None
        try:
            cur =  os.getcwd()
            nmap_info_file = cur+"/moniteur/info.txt"
            openedFile = open(nmap_info_file)
        
            mac = None
            ip = " "
            status = " "
            last_nmap = " "
            for line in openedFile:
                if 'MAC_ADDRESS=' in line:
                    mac = line.split('=')[1].rstrip()
                if 'IP_ADDRESS=' in line:
                    ip = line.split('=')[1].rstrip()
                if 'STATUS=' in line:
                    status = line.split('=')[1].rstrip()
                if 'DERNIER_NMAP=' in line:
                    last_nmap = line.split('=')[1].rstrip()
                
                if str(mac).lower().replace(" ","") == str(carte.mac).lower().replace(" ",""):
                    carte.ip = ip 
                    carte.status = status
                else:
                    pass 
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
            last_nmap = "No network" 

        mesures = Mesure.objects.filter(capteur__in=capteurs)
        
        for capteur in capteurs:
            capteur.mesures = mesures.filter(capteur=capteur)
            capteur.last_mesure = capteur.mesures.last()
        

        if carte.is_activated == True:
            carte.checked = "checked"
        else:
            carte.checked = " "

        if carte.type_carte == "Raspberry":
            carte.raspberry = "selected"
        elif carte.type_carte == "Arduino":
            carte.arduino = "selected"
        else:
            carte.dallas = "selected"


        context['capteurs'] = capteurs 
        context['last_nmap'] = last_nmap
        context['carte'] = carte
        context['capteurs'] = capteurs
        return context

