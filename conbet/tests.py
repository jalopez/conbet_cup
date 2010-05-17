"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from conbet.rules import WorldCupRules
from conbet.models import Team, GroupMatch
from django.test import TestCase

#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.failUnlessEqual(1 + 1, 2)
#
#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.
#
#>>> 1 + 1 == 2
#True
#"""}


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

    
