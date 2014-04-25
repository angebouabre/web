#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Temperature(models.Model):
    
    date_time = models.DateTimeField("Date de mesure")
    temperature = models.CharField("Temperature Mésuré", max_length=10)

    def __unicode__(self):
        return u"Temperature_du_%s" % self.date_time
