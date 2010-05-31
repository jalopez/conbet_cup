from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('conbet',
    (r'^$', 'views.index'),
    (r'^users/$', 'views.ranking'),
    (r'^users/(?P<username>\w+)/$', 'views.bet'),
    (r'^results/$', 'views.results'),
    (r'^rank_group/(?P<groupname>\w+)/?$', 'views.rank_group'),
    (r'^rules/$', 'views.rules'),
)
