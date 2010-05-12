from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=False)
    coefficient = models.FloatField()

    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    date = models.DateTimeField(null=True)
    group = models.ForeignKey(Group, null=True)
    location = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.id


class Round(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    # F for the final, S for semi-final, Q for quarter-finals...
    stage = models.CharField(max_length=1, blank=False)
    order = models.IntegerField() 
    match = models.ForeignKey(Match)

    def __unicode__(self):
        return self.id


class Qualification(models.Model):
    group = models.ForeignKey(Group, null=True)
    round = models.ForeignKey(Round, null=True, related_name='round')
    position = models.IntegerField()
    qualify_for = models.ForeignKey(Round, related_name='qualify_for')
    SIDE_CHOICES = (
        ('C', 'Competing'),
        ('V', 'Visitor'),
    )
    side = models.CharField(blank=False, max_length=1, choices=SIDE_CHOICES)

    def __unicode__(self):
        return "%s (%s)" % (self.qualify_for.id, self.side)

class Result(models.Model):
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    RESULT_CHOICES = (
        ('C', 'Competing'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    competing = models.ForeignKey(Team, related_name='competing_match',
                null=True)
    visiting  = models.ForeignKey(Team, related_name='visiting_match', 
                null=True)
    competing_goals = models.IntegerField()
    visiting_goals = models.IntegerField()
    winner = models.CharField(max_length=1, blank=False, choices=RESULT_CHOICES)
