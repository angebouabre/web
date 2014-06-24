from django.conf.urls import patterns, include, url
from moniteur.views import LocalisationView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'raspberry.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^mesure/', include('moniteur.urls', namespace='raspberry', app_name='moniteur')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', LocalisationView.as_view(), name='localisation'),
    )
