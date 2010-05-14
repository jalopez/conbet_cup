from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', 'admin.contrib.auth.views.login', {'template_name':
        'login.html'}),
    (r'^', include('conbet.urls')),
)
