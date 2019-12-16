import statsapi
from dateutil.parser import *
from django.core.management import BaseCommand

from mlb.game.models import Game, Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        for game_year in range(2016, 2020):
            games = statsapi.schedule(start_date=f'03/01/{game_year}', end_date=f'11/30/{game_year}', team=117)
            for thisgame in games:
                if thisgame['status'] == 'Final' and thisgame['game_type'] != 'S':
                    gamedate = parse(thisgame['game_date'])
                    gamedatetime = parse(thisgame['game_datetime'])
                    home_obj = Team.objects.get(id=thisgame['home_id'])
                    away_obj = Team.objects.get(id=thisgame['away_id'])

                    if thisgame['winning_team'] == home_obj.club_full_name:
                        winning_team = home_obj
                        losing_team = away_obj
                    else:
                        winning_team = away_obj
                        losing_team = home_obj

                    game_id_str = f'{gamedate.year}_{gamedate.month:02}_{gamedate.day:02}_{away_obj.team_code}mlb_{home_obj.team_code}mlb_{thisgame["game_num"]}'

                    if not thisgame['save_pitcher']:
                        thisgame['save_pitcher'] = ''

                    print(thisgame['game_type'], game_id_str, thisgame['summary'])

                    obj, created = Game.objects.update_or_create(
                        id=thisgame['game_id'],
                        defaults={
                            'game_id': game_id_str,
                            'date': gamedatetime,
                            'home_team': home_obj,
                            'away_team': away_obj,
                            'w_team': winning_team,
                            'l_team': losing_team,
                            'home_team_runs': thisgame['home_score'],
                            'away_team_runs': thisgame['away_score'],
                            'w_pitcher': thisgame['winning_pitcher'],
                            'l_pitcher': thisgame['losing_pitcher'],
                            'sv_pitcher': thisgame['save_pitcher'],
                        }
                    )
                    obj.save()

        # print(BASE_URL.format(2017, 9, 22) + 'scoreboard.xml')

        # broadcast_info = mlbgame.games(2017, 9, 22, home='Astros', away='Astros')
        # print(broadcast_info)
