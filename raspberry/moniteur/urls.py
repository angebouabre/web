from django.conf.urls import patterns, include, url
from moniteur.views import DashBoardView, LocalisationView # TemperatureDetail
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
   url(r'^localisation/$', LocalisationView.as_view(), name='localisation'), 
   url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'), 
   #url(r'^$', TemperatureList.as_view(), name='temperatures'),
   # url(r'^temperature/(?P<pk>\d+)/$', TemperatureDetail.as_view(), name='temperature'),
    
)
