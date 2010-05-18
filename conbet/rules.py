class WorldCupRules:
    class Criterion:
        def rank(self, teams, matches):
            pass

        def firsts(self, teams, matches):
            points = self.rank(teams, matches)
            max_points = max(points.values())
            firsts = []
            for team in teams:
                if points[team] == max_points:
                    firsts.append(team)
            return firsts


    class PointsCriterion(Criterion):
        def rank(self, teams, matches):
            points = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.winner != None:
                    if match.winner == 'T':
                        if points.has_key(match.home):
                            points[match.home] += 1
                        if points.has_key(match.visitor):
                            points[match.visitor] += 1
                    else:
                        if points.has_key(match.winner_team()):
                            points[match.winner_team()] += 3

            return points
    
    class GoalDifferenceCriterion(Criterion):
        def rank(self, teams, matches):
            goal_diff = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.home in goal_diff:
                    goal_diff[match.home] += match.home_goals - match.visitor_goals
                if match.visitor in goal_diff:
                    goal_diff[match.visitor] += match.visitor_goals - match.home_goals
            return goal_diff


    class ScoredGoalsCriterion(Criterion):
        def rank(self, teams, matches):
            goals = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.home in goals:
                    goals[match.home] += match.home_goals
                if match.visitor in goals:
                    goals[match.visitor] += match.visitor_goals
            return goals


    class TiedPointsCriterion(Criterion):
        def rank(self, teams, matches):
            points = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.winner != None:
                    if match.home in points and match.visitor in points: 
                        if match.winner == 'T':
                            points[match.home] += 1
                            points[match.visitor] += 1
                        else:
                            points[match.winner_team()] += 3
            return points
    

    class TiedGoalDifferenceCriterion(Criterion):
        def rank(self, teams, matches):
            goal_diff = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.home in goal_diff and match.visitor in goal_diff:
                    goal_diff[match.home] += match.home_goals - match.visitor_goals
                    goal_diff[match.visitor] += match.visitor_goals - match.home_goals
            return goal_diff


    class TiedScoredGoalsCriterion(Criterion):
        def rank(self, teams, matches):
            goals = dict(zip(teams, [0,0,0,0]))
            for match in matches:
                if match.home in goals and match.visitor in goals:
                    goals[match.home] += match.home_goals
                    goals[match.visitor] += match.visitor_goals
            return goals

    class FIFACoefCriterion(Criterion):
        def rank(self, teams, matches):
            coefficients = {}
            for team in teams:
                coefficients[team] = team.coefficient
            return coefficients


    group_criteria = (
        PointsCriterion(), 
        GoalDifferenceCriterion(),
        ScoredGoalsCriterion(),
        TiedPointsCriterion(), 
        TiedGoalDifferenceCriterion(),
        TiedScoredGoalsCriterion(),
        FIFACoefCriterion(),
    )

    def first(self, criteria, teams, matches):
        unranked_teams = teams
        for criterion in criteria:
            unranked_teams = criterion.firsts(unranked_teams, matches)
            if len(unranked_teams) == 1:
                return unranked_teams[0]
        
        print("WARNING: criteria does not provide a deterministic ranking " + 
              "(conflicting: %s)" % unranked_teams)
        return unranked_teams[0]


    def rank_group(self, teams, matches):
        ranking = []
        unranked_teams = teams

        while unranked_teams:
            first = self.first(self.group_criteria, unranked_teams, matches)
            ranking.append(first)
            unranked_teams = filter(lambda x: x != first, unranked_teams)

        return ranking
         
