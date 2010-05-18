"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from conbet.rules import WorldCupRules
from conbet.models import Team, GroupMatch
from django.test import TestCase

class WorldCupRulesTest(TestCase):
    def test_rank_by_points(self):
        """Usual case: the points speak by themselves"""
        teams = (
            Team(code='es', name='es'), # 2
            Team(code='en', name='en'), # 4
            Team(code='pt', name='pt'), # 1
            Team(code='fi', name='fi'), # 3
        )
        matches = (
            # es 0 - en 0
            GroupMatch(
                home=teams[0], home_goals=0,
                visitor=teams[1], visitor_goals=0,
                winner='T'),

            # pt 0 - fi 5
            GroupMatch(
                home=teams[2], home_goals=0,
                visitor=teams[3], visitor_goals=5,
                winner='V'),

            # es 0 - pt 0
            GroupMatch(
                home=teams[0], home_goals=0,
                visitor=teams[2], visitor_goals=0,
                winner='T'),

            # en 3 - pt 0
            GroupMatch(
                home=teams[1], home_goals=3,
                visitor=teams[2], visitor_goals=0,
                winner='H'),
        )
        instance = WorldCupRules()
        rank = instance.rank_group(teams, matches)
        self.assertEquals(rank, [teams[1], teams[3], teams[0], teams[2]])

    
    def test_rank_by_goals(self):
        """Total goals and goal difference"""
        teams = (
            Team(code='es', name='es'), # 3  2 T: 2
            Team(code='en', name='en'), # 3  2 T: 5
            Team(code='pt', name='pt'), # 1  -4
            Team(code='fi', name='fi'), # 1  0
        )
        matches = (
            # es 2 - en 0
            GroupMatch(
                home=teams[0], home_goals=2,
                visitor=teams[1], visitor_goals=0,
                winner='H'),

            # pt 0 - fi 0
            GroupMatch(
                home=teams[2], home_goals=0,
                visitor=teams[3], visitor_goals=0,
                winner='T'),

            # en 5 - pt 1
            GroupMatch(
                home=teams[1], home_goals=5,
                visitor=teams[2], visitor_goals=1,
                winner='H'),
        )
        instance = WorldCupRules()
        rank = instance.rank_group(teams, matches)
        self.assertEquals(rank, [teams[1], teams[0], teams[3], teams[2]])
