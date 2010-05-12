import sys

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from conbet import cup_templates
from conbet.models import Group, Match, Round, Qualification

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--template', '-t', dest='template',
            help='The template cup to use. Template "world_cup" by default'),
    )

    help='Creates the initial structure of matches and rounds'
    
    def handle(self, **options):
        template_name='world_cup'
        if options.get('template'):
            template_name = str(options.get('template'))
        try:
            self.template = getattr(cup_templates, template_name)
        except AttributeError, e:
            sys.stderr.write(self.style.ERROR(str('Unknown template "%s"\n' %
                template)))
            sys.exit(1)
        self.create_matches()


    def create_matches(self):
        for group in self.template['groups']:
            self.create_group(group)
        for r in self.template['rounds']:
            self.create_round(r)


    def create_group(self, group_name):
        group = Group(name=group_name)
        group.save()
        for i in range(1,7):
            match = Match(id="%s%d" % (group_name, i), group=group)
            match.save()

    def create_round(self, round_info):
        round_name = round_info[0]
        match = Match(id=round_name)
        match.save()

        round = Round(id=round_name, stage=round_name[0], order=int(round_name[1]),
                match=match)
        round.save()

        self.create_qualification (round, 'C', round_info[1])
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
            qualification.round = Round.objects.get(id=name)
        qualification.save()
