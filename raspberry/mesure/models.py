#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class CarteManager(models.Manager):
    def get_by_natural_key(self, nom_carte):
        print "ça passe ici...."
        return self.get(nom_carte=nom_carte)

class Carte(models.Model):
    
    objects = CarteManager()

    nom_carte = models.CharField(max_length=30, unique=True)
    type_carte = models.CharField(max_length=30, blank=True, null=True)
    mac = models.CharField(max_length=30, blank=True, null=True)
    memoire_disque = models.CharField(max_length=30, blank=True, null=True)
    is_activated = models.BooleanField()
    
    def __unicode__(self):
        return u"%s" % self.nom_carte

    def natural_key(self):
        return (self.nom_carte)
        
        
class CapteurManager(models.Manager):
    def get_by_natural_key(self, nom_capteur):
        return self.get(nom_capteur=nom_capteur)

class Capteur(models.Model):
    
    objects = CapteurManager()
    
    nom_capteur = models.CharField(max_length=30, unique=True)
    marque = models.CharField(max_length=30, blank=True, null=True)
    localisation = models.CharField(max_length=30, blank=True, null=True)
    type_mesure = models.CharField(max_length=30, blank=True, null=True)     
    date_activation = models.DateTimeField(blank=True, null=True)
    date_achat = models.DateField(blank=True, null=True)
    carte = models.ForeignKey(Carte)

    def __unicode__(self):
        return u"%s" % self.nom_capteur

    def natural_key(self):
        return (self.nom_capteur)


class Mesure(models.Model):
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    capteur = models.ForeignKey(Capteur)

    def __unicode__(self):
        return u"%s" % self.valeur
