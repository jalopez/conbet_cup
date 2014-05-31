from conbet.rules import WorldCupRules
from conbet.models import Team, GroupMatch
from django.test import TestCase
from conbet.prizes import WorldCupPrizes
import math

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
# rank_group test (for teams.txt.example)
#  Request: matches=[{"id":1, "home_goals":2, "visitor_goals": 0, "winner":"H"},
#  {"id":2, "home_goals":0, "visitor_goals":0, "winner":"T"}, {"id":5,
#  "home_goals":5, "visitor_goals":1, "winner":"H"}]
#  Expected_result: ["mx", "za", "fr", "uy"]

class WorldCupPrizesTest(TestCase):
    def test_one_user_per_prize(self):
        """ Usual case, one user per prize """
        prize = WorldCupPrizes(5)
        users = [
        {
            'position': 1
        },
        {
            'position': 2
        },
        {
            'position': 3
        },
        {
            'position': 4
        },
        {
            'position': 5
        },
        {
            'position': 6
        },
        ]
        third = math.floor((len(users)-1)*5*0.05)
        second = math.floor((len(users)-1)*5*0.25)
        first = (len(users)-1)*5 - second - third*3

        expected_result = [
        {
            'position': 1,
            'prize': first,
            'class_name': 'first'
        },
        {
            'position': 2,
            'prize': second,
            'class_name': 'second'
        },
        {
            'position': 3,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 4,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 5,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 6,
            'prize': 5,
            'class_name': 'last'
        },
        ]
        prize.set_prizes(users)
        self.assertEquals(users, expected_result)


    def test_two_first_prizes(self):
        """ Two users in the first place """
        prize = WorldCupPrizes(5)
        users = [
        {
            'position': 1
        },
        {
            'position': 1
        },
        {
            'position': 2
        },
        {
            'position': 3
        },
        {
            'position': 4
        },
        {
            'position': 5
        },
        ]
        third = float(math.floor((len(users)-1)*5*0.05))
        second = float(math.floor((len(users)-1)*5*0.25))
        first = float((len(users)-1)*5 - second - third*3)

        expected_result = [
        {
            'position': 1,
            'prize': (first + second)/2,
            'class_name': 'first'
        },
        {
            'position': 1,
            'prize': (first + second)/2,
            'class_name': 'first'
        },
        {
            'position': 2,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 3,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 4,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 5,
            'prize': 5,
            'class_name': 'last'
        },
        ]
        prize.set_prizes(users)
        self.assertEquals(users, expected_result)
    def test_two_first_two_second_prizes(self):
        """ Two users in the first place """
        prize = WorldCupPrizes(5)
        users = [
        {
            'position': 1
        },
        {
            'position': 1
        },
        {
            'position': 2
        },
        {
            'position': 2
        },
        {
            'position': 3
        },
        {
            'position': 4
        },
        ]
        third = float(math.floor((len(users)-1)*5*0.05))
        second = float(math.floor((len(users)-1)*5*0.25))
        first = float((len(users)-1)*5 - second - third*3)

        expected_result = [
        {
            'position': 1,
            'prize': (first + second)/2,
            'class_name': 'first'
        },
        {
            'position': 1,
            'prize': (first + second)/2,
            'class_name': 'first'
        },
        {
            'position': 2,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 2,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 3,
            'prize': third,
            'class_name': 'third'
        },
        {
            'position': 4,
            'prize': 5,
            'class_name': 'last'
        },
        ]
        prize.set_prizes(users)
        self.assertEquals(users, expected_result)
