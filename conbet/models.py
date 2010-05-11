from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=False)


class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)


class Match(models.Model):
    competing = models.ForeignKey(Team, related_name='competing_match')
    visiting  = models.ForeignKey(Team, related_name='visiting_match')
    date = models.DateField()
    group = models.ForeignKey(Group, null=True)


class Final(models.Model):
    # 1 for the final, 2 for semi-final, 3 for quarter-finals
    order = models.IntegerField() 
    match = models.ForeignKey(Match)
    qualify_for = models.ForeignKey('self')


class GroupQualification(models.Model):
    group = models.ForeignKey(Group)
    position = models.IntegerField()
    qualify_for = models.ForeignKey(Final)


class Result(models.Model):
    owner = models.ForeignKey(User)
    RESULT_CHOICES = (
        ('C', 'Competing'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    competing_goals = models.IntegerField()
    visiting_goals = models.IntegerField()
    winner = models.CharField(max_length=1, blank=False, choices=RESULT_CHOICES)
