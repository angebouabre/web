#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
register = template.Library()


@register.filter(name='display_name')
def display_name(nom):
    try :
        nom = nom.replace("_", " ")
    except:
        nom = None
    return nom 


@register.filter(name='display_state')
def display_state(state):
    if state == True: 
        state = "Activé"
    else:
        state = "Désactivé"
    return state 
