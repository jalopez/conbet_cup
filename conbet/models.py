from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    
    def __unicode__(self):
        return unicode(self.name)

    def get_position(self, position):
        return self.team_set.get(group_order=position)
    
    def matches(self):
        return self.groupmatch_set.all().order_by('date', 'id')


class Team(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=False)
    coefficient = models.FloatField(null=True)
    group = models.ForeignKey(Group)
    group_order = models.IntegerField()

    def __unicode__(self):
        return unicode(self.name)


class Result(models.Model):
    RESULT_CHOICES = (
        ('H', 'Home'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    home = models.ForeignKey(Team, null=True, blank=True, related_name='home_match')
    visitor = models.ForeignKey(Team, null=True, blank=True, related_name='visitor_match')
    home_goals = models.IntegerField(null=True, blank=True)
    visitor_goals = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=1, null=True, blank=True, choices=RESULT_CHOICES)

    def winner_team(self):
        if self.winner == 'H':
            return self.home
        elif self.winner == 'V':
            return self.visitor
        else:
            return None

    def loser_team(self):
        if self.winner == 'H':
            return self.visitor
        elif self.winner == 'V':
            return self.home
        else:
            return None

    def get_position(self, position):
        if position == 1:
            return self.winner_team()
        elif position == 2:
            return self.loser_team()
        else:
            raise Exception("Out of range")


class Match(Result):
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        if self.groupname() != None:
            return u'%s - %s' % (self.home.name, self.visitor.name)
        else:
            return u'%s' % (self.round_obj())
    def groupname(self):
        try:
            match = GroupMatch.objects.get(id=self.id)
            return match.group.name
        except GroupMatch.DoesNotExist:
            return None
    def round_obj(self):
        try:
            round = Round.objects.get(id=self.id)
            return round
        except Round.DoesNotExist:
            return None

class GroupMatch(Match):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return u'%s - %s' % (self.home.name, self.visitor.name)


class Round(Match):
    # 1 for the final, 2 for semi-final, 3 for quarter-finals...
    stage = models.IntegerField()
    order = models.IntegerField() 

    STAGE_NAMES={
        1: 'Final - 3 y 4 puesto',
        2: 'Semifinal',
        3: 'Cuartos de final',
        4: 'Octavos de final',
    }

    def __unicode__(self):
        return u'%s %d' % (self.STAGE_NAMES[self.stage], self.order)


class Bet(Result):
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)

    def __unicode__(self):
        return u'%s on %s' % (self.owner, self.match)


class Qualification(models.Model):
    # What qualifies 
    group = models.ForeignKey(Group, null=True)
    round = models.ForeignKey(Round, null=True, related_name='round')
    position = models.IntegerField()

    # Qualifies for...
    qualify_for = models.ForeignKey(Round, related_name='qualify_for')
    SIDE_CHOICES = (
        ('H', 'Home team'),
        ('V', 'Visitor team'),
    )
    side = models.CharField(blank=False, max_length=1, choices=SIDE_CHOICES)

    def __unicode__(self):
        return "%s (%s)" % (self.qualify_for.id, self.side)
