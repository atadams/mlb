import mlbgame
from django.core.management import BaseCommand
from mlbgame.data import INNINGS_URL, get_date_from_game_id

from mlb.game.models import Game, Inning, AtBat, Pitch


class Command(BaseCommand):
    def handle(self, *args, **options):
        Inning.objects.all().delete()
        games = Game.objects.filter(game_id='2017_09_21_chamlb_houmlb_1')
        for game in games:
            events = mlbgame.game_events(game.game_id, innings_endpoint=True)
            for inning in events:
                top_inning_obj, created = Inning.objects.get_or_create(
                    game=game,
                    inning=inning.num,
                    top_bottom='top',
                )
                top_inning_obj.save()

                for at_bat in inning.top:
                    add_at_bat(at_bat, top_inning_obj)

                bottom_inning_obj, created = Inning.objects.get_or_create(
                    game=game,
                    inning=inning.num,
                    top_bottom='bottom',
                )
                bottom_inning_obj.save()

                for at_bat in inning.bottom:
                    add_at_bat(at_bat, bottom_inning_obj)


def add_at_bat(at_bat, inning):
    if at_bat.tag == 'atbat':
        at_bat_obj, at_bat_created = AtBat.objects.update_or_create(
            play_guid=at_bat.play_guid,
            defaults={
                'inning': inning,
                'at_bat_number': at_bat.num,
                'home_team_runs': at_bat.home_team_runs,
                'away_team_runs': at_bat.away_team_runs,
                'balls': at_bat.b,
                'strikes': at_bat.s,
                'outs': at_bat.o,
                'start_time': at_bat.start_tfs_zulu,
                'end_time': at_bat.end_tfs_zulu,
                'batter_id': at_bat.batter,
                'pitcher_id': at_bat.pitcher,
                'description': at_bat.des,
                'event_number': at_bat.event_num,
                'event': at_bat.event,
            }
        )
        at_bat_obj.save()

        for pitch in at_bat.pitches:
            add_pitch(pitch, at_bat_obj)


def add_pitch(pitch, at_bat):
    obj, created = Pitch.objects.update_or_create(
        play_guid=pitch.play_guid,
        defaults={
            'at_bat': at_bat,
            'pitch_id': pitch.id,
            'pitch_result': pitch.des,
            'pitch_code': pitch.code,
            'pitch_datetime': pitch.tfs_zulu,
            'game_pitch_id': pitch.sv_id,
            'event_number': pitch.event_num,
            'start_speed': pitch.start_speed,
            'end_speed': pitch.end_speed,
            'break_y': pitch.break_y,
            'break_angle': pitch.break_angle,
            'break_length': pitch.break_length,
            'pitch_type': pitch.type,
            'pitch_type_confidence': pitch.type_confidence,
            'zone': pitch.zone,
            'nasty': pitch.nasty,
            'spin_dir': pitch.spin_dir,
            'spin_rate': pitch.spin_rate,
        }
    )
    obj.save()
