from django.conf.urls import patterns, include, url
#from mesure.views import TemperatureList # TemperatureDetail
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', TemperatureList.as_view(), name='temperatures'),
   # url(r'^temperature/(?P<pk>\d+)/$', TemperatureDetail.as_view(), name='temperature'),
    
)
