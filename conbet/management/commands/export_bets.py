import csv

from django.core.management.base import BaseCommand, CommandError

from django.contrib.admin.models import User
from conbet.models import Bet


class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help='Export all bets in a CSV file'
    args='out_file'

    field_names = ['Usuario', 'Partido', 'Equipo Casa', 'Equpo Visitante', 'Goles 1', 'Goles Visitante', 'Ganador']
    
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Usage is export_bets %s' % self.args)
        else:
            with open(args[0], 'wb') as csvfile:
                csvwriter = csv.writer(csvfile)

                csvwriter.writerow(self.field_names)

                for user in User.objects.all():
                    for bet in Bet.objects.filter(owner=user):
                        if bet.match.groupname():
                            match = 'Grupo ' + bet.match.groupname()
                        else:
                            match = bet.match.round_obj()

                        home = bet.match.home
                        visitor = bet.match.visitor
                        home_goals = bet.match.home_goals
                        visitor_goals = bet.match.visitor_goals
                        winner = bet.match.winner

                        if winner == 'H':
                            winner = home
                        elif winner == 'V':
                            winner = visitor
                        elif winner == 'T':
                            winner = 'Empate'

                        line = [user, match, home, visitor, home_goals, visitor_goals, winner]
                        csvwriter.writerow(line)
