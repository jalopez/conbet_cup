# -*- coding: utf-8 -*-

def same_goals(result1, result2):
    sides = 0
    if result1.home_goals == result2.home_goals:
        sides += 1
    if result1.visitor_goals == result2.visitor_goals:
        sides += 1
    return sides


def same_teams(result1, result2):
    sides = 0
    if result1.home == result2.home:
        sides += 1
    if result1.visitor == result2.visitor:
        sides += 1
    return sides


class WorldCupScoreRules:
    """
    Score Rules for the World Cup 2010.

    Reasons:
        * match.teams
        * match.goals
        * match.winner
        * match.all
        * group.all
        * group.team
        * cup.winner
    """

    def score_group_match(self, bet, match):
        """
        Score group matches.

        punctuation = [(<points>, <reason>)]
        """
        sides = same_goals(bet, match)
        if sides == 2:
            return [(3, 'match.goals')]
        elif sides == 1:
            return [(1, 'match.goals')]
        else: 
            return []



    def score_group_classification(self, bet_ranking, ranking):
        """
        Score group classification.

        punctuation = [(<points>, <reason>)]
        """
        matches = len(filter(lambda r: r[0] == r[1], 
                             zip(bet_ranking, ranking)))
        if matches == 4:
            return [(5, 'group.all')]
        else:
            return [(matches, 'group.team')]


    def score_round(self, bet, match):
        """
        Score round classification.

        punctuation = [(<points>, <reason>)]
        """
        
        points = []
        factor = 6 - match.stage

        # goals
        guessed_goals = same_goals(bet, match)
        if guessed_goals == 2:
            points.append((factor * 3, 'match.goals'))
        elif guessed_goals == 1:
            points.append((factor, 'match.goals'))
        
        # winner
        if bet.winner == match.winner:
            points.append((factor, 'match.winner'))

        # teams
        guessed_teams = same_teams(bet, match)
        if guessed_teams == 2:
            points.append((factor * 3, 'match.teams'))
        elif guessed_teams == 1:
            points.append((factor, 'match.teams'))

        # all together
        if guessed_teams == 2 and guessed_goals == 2 and bet.winner == match.winner:
            points.append((factor, 'match.all'))

        return points
    
    def score_cup_winner(self, bet, match):
        points = []
        if bet.winner == match.winner:
            if match.winner == 'H' and bet.home_team == match.home_team:
                points.append((20, 'cup.winner'))
            if match.winner == 'V' and bet.visitor_team == match.visitor_team: 
                points.append((20, 'cup.winner'))
        return points
