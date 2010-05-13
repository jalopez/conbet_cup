from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=False)
    coefficient = models.FloatField(null=True)
    group = models.ForeignKey(Group)
    group_order = models.IntegerField()

    def __unicode__(self):
        return self.name


class Result(models.Model):
    RESULT_CHOICES = (
        ('H', 'Home'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    home_goals = models.IntegerField(null=True)
    visitor_goals = models.IntegerField(null=True)
    winner = models.CharField(max_length=1, null=True, choices=RESULT_CHOICES)

    class Meta:
        abstract = True


class Match(Result):
    date = models.DateTimeField(null=True)
    location = models.CharField(max_length=50, null=True)
    home = models.ForeignKey(Team, null=True, related_name='home_match')
    visitor = models.ForeignKey(Team, null=True, related_name='visitor_match')


class GroupMatch(Match):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "%s - %s" % (self.home, self.visitor)


class Round(Match):
    # F for the final, S for semi-final, Q for quarter-finals...
    stage = models.CharField(max_length=1, blank=False)
    order = models.IntegerField() 

    def __unicode__(self):
        return "%s%s" % (self.stage, self.order)


class Bet(Result):
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)

class Qualification(models.Model):
    group = models.ForeignKey(Group, null=True)
    round = models.ForeignKey(Round, null=True, related_name='round')
    position = models.IntegerField()
    qualify_for = models.ForeignKey(Round, related_name='qualify_for')
    SIDE_CHOICES = (
        ('H', 'Home team'),
        ('V', 'Visitor team'),
    )
    side = models.CharField(blank=False, max_length=1, choices=SIDE_CHOICES)

    def __unicode__(self):
        return "%s (%s)" % (self.qualify_for.id, self.side)

