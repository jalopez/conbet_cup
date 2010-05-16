import json

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.contrib.auth.models import User

from conbet.models import Match, Bet, GroupMatch, Round, Group

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
    if request.method == 'POST':
        update_bet(request)
    return bet(request, request.user.username, editable=True) 

@login_required
def bet(request, username, editable=False):
    user = get_object_or_404(User, username=username)

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
        try:
            bet = Bet.objects.get(owner=user, match=match)
        except Bet.DoesNotExist:
            bet = Bet(owner=user, match=match)
        bets.append(bet)

    return render_to_response('bet.html', {
        'groups': Group.objects.all().order_by('name'),
        'bets': bets,
        'rounds': rounds,
        'valid_goals': range(settings.MAX_GOALS+1),
        'editable': editable,
    })

@login_required
def results(request):
    raise Http404

### Aux functions


def update_bet(request):
    bet_info = json.loads(request.POST.get('bets'))
    for (match_id, match_info) in bet_info.items():
        match = Match.objects.get(id=match_id)
        try:
            bet = Bet.objects.get(owner=request.user, match=match)
        except Bet.DoesNotExist:
            bet = Bet(owner=request.user, match=match)
        bet.home_goals = match_info['home_goals']
        bet.visitor_goals = match_info['visitor_goals']
        if bet.home_goals > bet.visitor_goals:
            bet.winner = 'H'
        elif bet.home_goals < bet.visitor_goals:
            bet.winner = 'V'
        else:
            try:
                group_match = GroupMatch.objects.get(id=match.id)
                bet.winner = 'T'
            except GroupMatch.DoesNotExist: 
                bet.winner = match_info['winner']
        bet.save()
