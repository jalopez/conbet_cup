from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('conbet',
    (r'^$', 'views.index'),
    (r'^users/$', 'views.ranking'),
    (r'^users/(?P<username>\w+)/$', 'views.bet'),
    (r'^results/$', 'views.results'),
    (r'^rank_group/(?P<groupname>\w+)/?$', 'views.rank_group'),
    (r'^rules/$', direct_to_template, {'template': 'rules.html'}, "rules"),
)
