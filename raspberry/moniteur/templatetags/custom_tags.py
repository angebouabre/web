from django import template
register = template.Library()


@register.filter(name='display_name')
def display_name(nom):
    try :
        nom = nom.replace("_", " ")
    except:
        nom = None
    return nom 
