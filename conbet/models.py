from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=False)
    coefficient = models.FloatField()


class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)


class Match(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    competing = models.ForeignKey(Team, related_name='competing_match',
                null=True)
    visiting  = models.ForeignKey(Team, related_name='visiting_match', 
                null=True)
    date = models.DateTimeField(null=True)
    group = models.ForeignKey(Group, null=True)
    location = models.CharField(max_length=50, null=True)


class Round(models.Model):
    # F for the final, S for semi-final, Q for quarter-finals...
    stage = models.CharField(max_length=1, blank=False)
    order = models.IntegerField() 
    match = models.ForeignKey(Match)
    qualify_for = models.ForeignKey('self', null=True)


class GroupQualification(models.Model):
    group = models.ForeignKey(Group)
    position = models.IntegerField()
    qualify_for = models.ForeignKey(Round)


class Result(models.Model):
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    RESULT_CHOICES = (
        ('C', 'Competing'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    competing_goals = models.IntegerField()
    visiting_goals = models.IntegerField()
    winner = models.CharField(max_length=1, blank=False, choices=RESULT_CHOICES)
