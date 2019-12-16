import mlbgame
from django.core.management import BaseCommand

from mlb.game import data
from mlb.game.models import Team, Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = Team.objects.all()
        for team in teams:
            players = data.roster_alltime(team.id)
            for player in players['players']:
                obj, created = Player.objects.update_or_create(
                    id=player['player_id'],
                    defaults={
                        'name_first_last': player['name_first_last'],
                        'name_last_first': player['name_last_first'],
                        'player_first_last_html': player['player_first_last_html'],
                        'player_html': player['player_html'],
                        'jersey_number': player['jersey_number'],
                        'primary_position': player['primary_position'],
                        'primary_position_cd': player['primary_position_cd'],
                        'position_desig': player['position_desig'],
                        'throws': player['throws'],
                        'bats': player['bats'],
                        'team_id': team.id,
                    }
                )
                obj.team = team
                obj.save()
                print(team, ' - ', player)
