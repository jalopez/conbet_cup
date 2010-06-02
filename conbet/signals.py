from django.db.models.signals import pre_save, post_save
from django.conf import settings
from conbet.models import Qualification, GroupMatch, Round


def pre_save_groupmatch(sender, **kwargs):
    instance = kwargs['instance']
    if instance.home_goals != None and instance.visitor_goals != None:
        if instance.home_goals > instance.visitor_goals:
            instance.winner = 'H'
        elif instance.visitor_goals > instance.home_goals:
            instance.winner = 'V'
        else:
            instance.winner = 'T'


def post_save_groupmatch(sender, **kwargs):
    instance = kwargs['instance']
    unplayed_matches = instance.group.groupmatch_set.filter(winner__isnull=True)

    if len(unplayed_matches)==0:
        ranking = settings.RULES.rank_group(
            instance.group.team_set.all(),
            instance.group.groupmatch_set.all())
        for i, team in enumerate(ranking):
            team.group_order = i + 1
            team.save()

        for q in Qualification.objects.filter(group=instance.group):
            round = q.qualify_for
            team = instance.group.get_position(q.position) 
            if team:
                print("%d-th %s qualifies for %s (%s)" % (
                    q.position, q.group,
                    q.qualify_for, q.side,
                ))

                if q.side == 'H':
                    round.home = team
                else:
                    round.visitor = team
                round.save()


def pre_save_round(sender, **kwargs):
    instance = kwargs['instance']
    if instance.home_goals != None and instance.visitor_goals != None:
        if instance.home_goals > instance.visitor_goals:
            instance.winner = 'H'
        elif instance.visitor_goals > instance.home_goals:
            instance.winner = 'V'
        else:
            pass # Don't force a winner 


def post_save_round(sender, **kwargs):
    instance = kwargs['instance']
    if instance.winner != None:
        for q in Qualification.objects.filter(round=instance):
            round = q.qualify_for
            team = instance.get_position(q.position) 
            if team:
                print("%d-th %s qualifies for %s (%s)" % (
                    q.position, q.round,
                    q.qualify_for, q.side,
                ))
                if q.side == 'H':
                    round.home = team
                else:
                    round.visitor = team
                round.save()


def connect():
    pre_save.connect(pre_save_groupmatch, sender=GroupMatch)
    post_save.connect(post_save_groupmatch, sender=GroupMatch)
    pre_save.connect(pre_save_round, sender=Round)
    post_save.connect(post_save_round, sender=Round)

