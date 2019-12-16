import mlbgame
from django.core.management import BaseCommand

from mlb.game.models import Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = mlbgame.teams()

        for team in teams:
            obj, created = Team.objects.update_or_create(
                id=team.team_id,
                defaults={
                    'team_pk': team.id,
                    'team_code': team.team_code,
                    'club_id': team.club_id,
                    'club': team.club,
                    'club_common_name': team.club_common_name,
                    'club_full_name': team.club_full_name,
                    'name_display_long': team.name_display_long,
                    'name_display_short': team.name_display_short,
                    'display_code': team.display_code,
                    'venue_id': team.venue_id,
                    'field': team.field,
                    'league': team.league,
                    'location': team.location,
                    'timezone': team.timezone,
                    'aws_club_slug': team.aws_club_slug,
                    'youtube': team.youtube,
                }
            )
            obj.save()
