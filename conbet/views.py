# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext

from conbet.models import Match, Bet, GroupMatch, Round, Group, Qualification, Result, Team, CachedRanking
from conbet.helpers import *


def index(request):
    if settings.BETTING:
        if request.user.is_authenticated():
            return edit_bet(request)
        else:
            return HttpResponseRedirect("login/?next=/")
    else:
        return ranking(request)

def ranking(request):
    users = []
    position = 0
    last_points = None
    for user in User.objects.all():
        try:
            points = user.cachedranking.total_points 
        except CachedRanking.DoesNotExist:
            points = 0
        users.append({
            'points': points,
            'name': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
        })
    users = sorted(users, key=lambda x: -x['points'])
    for user in users:
        if user["points"] != last_points:
            last_points = user["points"]
            position += 1
        user["position"] = position
    settings.PRIZES.set_prizes(users)
    
    return render_to_response('ranking.html', { 'users': users },
        context_instance=RequestContext(request))


@login_required
def edit_bet(request):
    if request.method == 'POST':
        update_bet(request)
    return bet(request, request.user.username, editable=True) 


@login_required
def bet(request, username, editable=False):
    user = get_object_or_404(User, username=username)
    if user != request.user and settings.BETTING:
        return HttpResponseForbidden()

    stages = Round.objects.values('stage').distinct().order_by('-stage')
    rounds = []
    for s in stages:
        stage = s['stage']
        rounds.append([
            Round.STAGE_NAMES[stage],
            Round.objects.filter(stage=stage).order_by('order'),
            ])

    bets = []
    for match in Match.objects.all():
        bet, created = Bet.objects.get_or_create(owner=user, match=match)
        bets.append(bet)

    try:
        total_score = user.cachedranking.total_points 
    except CachedRanking.DoesNotExist:
        total_score = 0
    return render_to_response('bet.html', {
        'groups': Group.objects.all().order_by('name'),
        'qualifications': Qualification.objects.all(),
        'teams': Team.objects.all(),
        'bets': bets,
        'rounds': rounds,
        'valid_goals': range(settings.MAX_GOALS+1),
        'editable': editable,
        'points': score_bet(user),
        'total_score': total_score,
        'bet_user': user
    }, context_instance=RequestContext(request))


@login_required
def results(request):
    stages = Round.objects.values('stage').distinct().order_by('-stage')
    rounds = []
    for s in stages:
        stage = s['stage']
        rounds.append([
            Round.STAGE_NAMES[stage],
            Round.objects.filter(stage=stage).order_by('order'),
            ])

    return render_to_response('bet.html', {
        'groups': Group.objects.all().order_by('name'),
        'teams': Team.objects.all(),
        'bets': Match.objects.all(),
        'rounds': rounds,
        'editable': False,
    }, context_instance=RequestContext(request))


def rank_group(request, groupname):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    group_matches = json.loads(request.POST.get('matches'))

    group = get_object_or_404(Group, name=groupname)
    teams = group.team_set.all()
    results = []
    for match_info in group_matches:
        match = group.groupmatch_set.get(id=match_info["id"])
        results.append(Result(home=match.home, visitor=match.visitor,
            home_goals=match_info['home_goals'], 
            visitor_goals=match_info['visitor_goals'],
            winner=match_info['winner']))

    ranking = settings.RULES.rank_group(teams, results, with_points=True)
    return HttpResponse(json.dumps(map(lambda t: (t[0].code, t[1]), ranking)),
        content_type="text/json")
