from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

@login_required
def index(request):
    if settings.BETTING:
        return edit_bet(request)
    else:
        return ranking(request)

@login_required
def ranking(request):
    raise Http404

@login_required
def edit_bet(request):
    raise Http404

@login_required
def bet(request, username):
    raise Http404

@login_required
def results(request):
    raise Http404
