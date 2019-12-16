import youtube_dl
from django.core.management import BaseCommand
from pytube import YouTube
from pytube.cli import on_progress

from mlb.game.data import ORIGINAL_VIDEO_DIR
from mlb.game.models import Game, Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        games = Game.objects.exclude(youtube_id__exact='')
        for game in games:
            ydl_video_opts = {
                'format': 'bestaudio[ext=aac]',
                'outtmpl': f'{ORIGINAL_VIDEO_DIR}/{game.game_id}.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_video_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={game.youtube_id}'])

        print('COMPLETE')
