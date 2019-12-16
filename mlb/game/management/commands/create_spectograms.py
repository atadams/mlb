import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import librosa
from django.core.management import BaseCommand

from mlb.game.data import ORIGINAL_VIDEO_DIR
from mlb.game.models import Pitch, Game


class Command(BaseCommand):
    def handle(self, *args, **options):
        # first_pitch = Pitch.objects.filter(at_bat__inning__game__game_id='2017_09_21_chamlb_houmlb_1').first()
        games = Game.objects.exclude(youtube_id__exact='')
        for game in games:
            for inning in game.innings.filter(top_bottom='bottom').order_by('inning'):
                print(inning)
                for at_bat in inning.at_bat.all():
                    for pitch in at_bat.pitches.all()[0:1]:
                        print(f'{ORIGINAL_VIDEO_DIR}/{game.game_id}_{pitch.pitch_id:003}')
                        pitch_time_offset = (pitch.pitch_datetime - game.first_pitch_time).total_seconds() + game.youtube_start_offset - 1
                        y, sr = librosa.load(f'{ORIGINAL_VIDEO_DIR}/{game.original_video_filename}', offset=pitch_time_offset, duration=10)
                        window_size = 1024
                        window = np.hanning(window_size)
                        stft = librosa.core.spectrum.stft(y, n_fft=window_size, hop_length=512, window=window)
                        out = 2 * np.abs(stft) / np.sum(window)

                        # For plotting headlessly
                        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

                        fig = plt.Figure()
                        canvas = FigureCanvas(fig)
                        ax = fig.add_subplot(111)
                        p = librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, y_axis='log',
                                                     x_axis='time')
                        fig.savefig(f'{ORIGINAL_VIDEO_DIR}/{game.game_id}_{pitch.pitch_id:003}.png')
                        print(pitch_time_offset, pitch.pitch_datetime, pitch.pitch_result)

            print()
            # pitches = Pitch.objects.first()
            # print(pitches.at_bat.inning.game.date)
            # print(pitches.pitch_datetime)
            # print()
            # for pitch in pitches:
            #     print(pitch.at_bat.inning.game.date)
            #     print(pitch.pitch_datetime)
            #     print()
