from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('conbet',
    (r'^$', 'views.index'),
    (r'^user/$', 'views.ranking'),
    (r'^user/(?P<username>\w+)/$', 'views.bet'),
    (r'^results/$', 'views.results'),
)
