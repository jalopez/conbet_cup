from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    
    def __unicode__(self):
        return self.name

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
        return self.name


class Result(models.Model):
    RESULT_CHOICES = (
        ('H', 'Home'),
        ('V', 'Visitor'),
        ('T', 'Tie'),
    )
    home_goals = models.IntegerField(null=True, blank=True)
    visitor_goals = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=1, null=True, blank=True, choices=RESULT_CHOICES)

    class Meta:
        abstract = True


class Match(Result):
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    home = models.ForeignKey(Team, null=True, related_name='home_match')
    visitor = models.ForeignKey(Team, null=True, related_name='visitor_match')

    def winner_team(self):
        if self.winner == 'H':
            return self.home
        elif self.winner == 'V':
            return self.visitor
        else:
            return None

    def __unicode__(self):
        return str(self.id)


class GroupMatch(Match):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "%s - %s" % (self.home, self.visitor)
    
    @staticmethod
    def before_save(sender, **kwargs):
        instance = kwargs['instance']
        if instance.home_goals != None and instance.visitor_goals != None:
            if instance.home_goals > instance.visitor_goals:
                instance.winner = 'H'
            elif instance.visitor_goals > instance.home_goals:
                instance.winner = 'V'
            else:
                instance.winner = 'T'

    @staticmethod
    def on_save(sender, **kwargs):
        instance = kwargs['instance']
        ranking = settings.RULES.rank_group(
            instance.group.team_set.all(),
            instance.group.groupmatch_set.all())
        for i, team in enumerate(ranking):
            team.group_order = i + 1
            team.save()

        for q in Qualification.objects.filter(group=instance.group):
            round = q.qualify_for
            team = instance.group.get_position(q.position) 
            if q.side == 'H':
                round.home = team
            else:
                round.visitor = team
            round.save()


pre_save.connect(GroupMatch.before_save, sender=GroupMatch)
post_save.connect(GroupMatch.on_save, sender=GroupMatch)

class Round(Match):
    # 1 for the final, 2 for semi-final, 3 for quarter-finals...
    stage = models.IntegerField()
    order = models.IntegerField() 

    STAGE_NAMES={
        1: 'Final',
        2: 'Semifinal',
        3: 'Quarter-final',
        4: 'Round-of-16',
    }

    def __unicode__(self):
        return "%s %d" % (self.STAGE_NAMES[self.stage], self.order)

    @staticmethod
    def before_save(sender, **kwargs):
        instance = kwargs['instance']
        if instance.home_goals != None and instance.visitor_goals != None:
            if instance.home_goals > instance.visitor_goals:
                instance.winner = 'H'
            elif instance.visitor_goals > instance.home_goals:
                instance.winner = 'V'
            else:
                pass # Don't force a winner 

pre_save.connect(Round.before_save, sender=Round)


class Bet(Result):
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)

    def __unicode__(self):
        return "%s (%s)" % (self.match, self.owner)

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
