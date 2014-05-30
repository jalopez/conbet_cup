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

def unordered_qualifying_teams(bet_ranking, ranking):
    teams = 0
    if ranking[0] == bet_ranking[1]:
        teams += 1
    if ranking[1] == bet_ranking[0]:
        teams += 1
    return teams

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
        * group.unordered
        * cup.winner
    """

    def score_group_match(self, bet, match):
        """
        Score group matches.

        punctuation = [(<points>, <reason>)]
        """
        sides = same_goals(bet, match)
        points = []
        if sides == 2:
            points.append((3, 'match.goals'))
        elif sides == 1:
            points.append((1, 'match.goals'))

        # winner
        if bet.winner == match.winner:
            points.append((2, 'match.winner'))
        
        if len(points) == 0:
            points.append((0, 'match.none'))

        return points


    def score_group_classification(self, bet_ranking, ranking):
        """
        Score group classification.

        punctuation = [(<points>, <reason>)]
        """
        matches = len(filter(lambda r: r[0] == r[1], 
                             zip(bet_ranking, ranking)))

        points = []
        if matches == 4:
            points.append((10, 'group.all'))
        else:
            points.append((matches*2, 'group.team'))

        # unordered qualifyed teams
        #teams = unordered_qualifying_teams(bet_ranking, ranking)

        #if teams == 2:
        #    points.append((3, 'group.unordered'))
        #elif teams == 1:
        #    points.append((1, 'group.unordered'))

        return points

    def score_teams_round(self, stage, bet_teams, teams):
        """
        Score guessed teams in a given round

        punctuation = [(<points>, <reason>)]
        """
        factor = 6 - stage

        set_teams = set(teams)
        guessed_teams_len = len([x for x in bet_teams if x in set_teams])

        points = guessed_teams_len * factor

        if guessed_teams_len == len(teams):
            points += factor

        return [(points, 'round.teams')]


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

        if len(points) == 0:
            points.append((0, 'match.none'))
        return points
    
    def score_cup_winner(self, bet, match):
        points = []
        if match.winner_team() != None and bet.winner_team() == match.winner_team():
                points.append((20, 'cup.winner'))
        return points
