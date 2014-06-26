#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class CarteManager(models.Manager):
    def get_by_natural_key(self, nom_carte):
        return self.get(nom_carte=nom_carte)

class Carte(models.Model):
    
    objects = CarteManager()

    slug = models.SlugField(max_length=30, unique=True, blank=True)
    
    RASPBERRY = 'Raspberry'
    ARDUINO = 'Arduino'
    DALLAS = 'Dallas'
    
    CARTE_TYPE = (
        (RASPBERRY, 'Raspberry'),
        (ARDUINO, 'Arduino'),
        (DALLAS, 'Dallas'),
    )

    nom_carte = models.CharField(max_length=30, unique=True)
    type_carte = models.CharField(max_length=12,
                                   choices=CARTE_TYPE,
                                   default=RASPBERRY,
                                   blank=True,
                                   null=True)
    mac = models.CharField(max_length=30, blank=True, unique=True)
    memoire_disque = models.CharField(max_length=30, blank=True, null=True)
    is_activated = models.BooleanField()
    status = models.CharField(max_length=6)
    
    def __unicode__(self):
        return u"%s" % self.nom_carte

    def get_absolute_url(self):
        return "/mesure/carte/%s" %self.slug


    def save(self, **kwargs):
        self.slug = self.nom_carte
        super(Carte, self).save()

    def natural_key(self):
        return (self.nom_carte)
        
        
class CapteurManager(models.Manager):
    def get_by_natural_key(self, nom_capteur):
        return self.get(nom_capteur=nom_capteur)

class Capteur(models.Model):
    
    objects = CapteurManager()
    
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    
    ENTREPOT1 = 'ENTREPOT_1'
    ENTREPOT2 = 'ENTREPOT_2'
    ENTREPOT3 = 'ENTREPOT_3'
    ENTREPOT4 = 'ENTREPOT_4'
    
    LOCAL_CHOICES = (
        (ENTREPOT1, 'Entrepot 1'),
        (ENTREPOT2, 'Entrepot 2'),
        (ENTREPOT3, 'Entrepot 3'),
        (ENTREPOT4, 'Entrepot 4'),
    )
    
    HYGROMETRIE = 'Hygrometrie'
    TEMPERATURE = 'Temperature'
    
    MESURE_TYPE = (
        (HYGROMETRIE, 'Hygrometrie'),
        (TEMPERATURE, 'Temperature'),
    )

    localisation= models.CharField(max_length=10,
                                   choices=LOCAL_CHOICES,
                                   default=ENTREPOT1)
    type_mesure = models.CharField(max_length=12,
                                   choices=MESURE_TYPE,
                                   default=TEMPERATURE,
                                   blank=True,
                                   null=True)
                                       
    nom_capteur = models.CharField(max_length=30, unique=True)
    marque = models.CharField(max_length=30, blank=True, null=True)
    date_activation = models.DateTimeField(blank=True, null=True)
    date_achat = models.DateField(blank=True, null=True)
    carte = models.ForeignKey(Carte)

    def __unicode__(self):
        return u"%s" % self.nom_capteur

    def save(self, **kwargs):
        self.slug = self.nom_capteur
        super(Capteur, self).save()

    def natural_key(self):
        return (self.nom_capteur)


class Mesure(models.Model):
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    date_mesure = models.DateTimeField(blank=True, null=True)
    capteur = models.ForeignKey(Capteur)

    def __unicode__(self):
        return u"%s" % self.valeur
