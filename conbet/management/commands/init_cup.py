import sys

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from conbet import cup_templates
from conbet.models import Group, GroupMatch, Round, Qualification, Team


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--template', '-t', dest='template',
            help='The template cup to use. Template "world_cup" by default'),
    )

    help='Creates the initial structure of matches and rounds'
    args='teams_file'
    
    def handle(self, *args, **options):
        template_name='world_cup'
        if options.get('template'):
            template_name = str(options.get('template'))
        try:
            self.template = getattr(cup_templates, template_name)
        except AttributeError, e:
            raise CommandError('Unknown template "%s"\n' % template)

        if not args:
            raise CommandError('Usage is init_cup %s' % self.args)
        else:
            self.teams = self.parse_teams(args[0])

        self.create_matches()


    def create_matches(self):
        for group in self.template['groups']:
            if type(group) == tuple:
                group_name = group[0]
                group_order = self.template['group_matches'][group[1]]
            else:
                group_name = group
                group_order = self.template['group_matches'].values()[0]
            self.create_group(group_name, group_order)
        for r in self.template['rounds']:
            self.create_round(r)


    def create_group(self, group_name, group_order):
        group = Group(name=group_name)
        group.save()

        teams = []
        i = 0
        for (team_code, team_name) in self.teams[group_name]:
            team = Team(code=team_code, name=team_name, group=group,
                        group_order=++i)
            team.save()
            teams.append(team)

        for sel in group_order:
            match = GroupMatch(group=group,
                home=teams[sel[0] - 1],
                visitor=teams[sel[1] - 1])
            match.save()


    def create_round(self, round_info):
        round_name = round_info[0]
        round = Round(stage=round_name[0], order=int(round_name[1]))
        round.save()

        self.create_qualification (round, 'H', round_info[1])
        self.create_qualification (round, 'V', round_info[2])


    def create_qualification(self, round, side, origin):
        if type(origin) == tuple:
            name = origin[0]
            position = origin[1]
        else:
            name = origin
            position = 1

        qualification = Qualification(position=position, qualify_for=round,
                side=side)
        if name in self.template['groups']:
            qualification.group = Group.objects.get(name=name)
        else:
            qualification.round = Round.objects.get(stage=name[0],
                                                    order=int(name[1]))
        qualification.save()

    def parse_teams(self, teams_file):
        import re
        try:
            fd = open(teams_file, 'r')

            teams = {}
            current_group = None
            for line in fd.readlines():
                header_match = re.match(r'\[(?P<group>.)\]', line)
                team_match = re.match(r'(?P<code>..) (?P<name>.*)', line)
                if header_match:
                    current_group = header_match.group('group')
                    teams[current_group] = []
                    if not (current_group in self.template['groups']):
                        raise CommandError('Unknown group "%s"' % current_group)
                elif team_match:
                    if not current_group:
                        raise CommandError('Bad teams file format')
                    teams[current_group] += [(team_match.group('code'),
                                              team_match.group('name'))]
                else:
                    raise CommandError('Bad teams file format')

            fd.close()
            return teams
        except IOError, e:
            raise CommandError(str(e))
