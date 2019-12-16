from django.db import models


class Team(models.Model):
    team_pk = models.IntegerField(db_index=True)  # 147
    team_code = models.CharField(max_length=100)  # 'nya'
    club_id = models.IntegerField()  # 21
    club = models.CharField(max_length=100)  # 'nyy'
    club_common_name = models.CharField(max_length=100)  # 'Yankees'
    club_full_name = models.CharField(max_length=100)  # 'New York Yankees'
    name_display_long = models.CharField(max_length=100)  # 'The New York Yankees'
    name_display_short = models.CharField(max_length=100)  # 'NY Yankees'
    display_code = models.CharField(max_length=100)  # 'nyy'
    venue_id = models.IntegerField()  # 3313
    field = models.CharField(max_length=100)  # 'Yankee Stadium'
    league = models.CharField(max_length=100)  # 'American'
    location = models.CharField(max_length=100)  # 'New York'
    timezone = models.CharField(max_length=100)  # 'ET'
    aws_club_slug = models.CharField(max_length=100)  # 'yankees'
    youtube = models.CharField(max_length=100)  # 'UCmAQ_4ELJodnKuNqviK86Dg'

    def __str__(self):
        return self.club_common_name


class Player(models.Model):
    name_first_last = models.CharField(max_length=50)  # 'Jose Altuve'
    name_last_first = models.CharField(max_length=50)  # 'Altuve, Jose'
    player_first_last_html = models.CharField(max_length=50)  # 'José Altuve'
    player_html = models.CharField(max_length=50)  # 'Altuve, José'
    jersey_number = models.CharField(max_length=50)  # '27'
    primary_position = models.CharField(max_length=50)  # '2B'
    primary_position_cd = models.CharField(max_length=50)  # '4'
    position_desig = models.CharField(max_length=50)  # 'INFIELDER'
    throws = models.CharField(max_length=50)  # 'R'
    bats = models.CharField(max_length=50)  # 'R'
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_first_last


class Game(models.Model):
    EXHIBITION = 'E'
    SPRING_TRAINING = 'S'
    REGULAR_SEASON = 'R'
    WILD_CARD = 'F'
    DIVISIONAL_SERIES = 'D'
    LEAGUE_CHAMPIONSHIP_SERIES = 'L'
    WORLD_SERIES = 'W'

    GAME_TYPE_CHOICES = [
        (EXHIBITION, 'Exhibition'),
        (SPRING_TRAINING, 'Spring Training'),
        (REGULAR_SEASON, 'Regular Season'),
        (WILD_CARD, 'Wild Card'),
        (DIVISIONAL_SERIES, 'Divisional Series'),
        (LEAGUE_CHAMPIONSHIP_SERIES, 'League Championship Series'),
        (WORLD_SERIES, 'World Series'),
    ]

    game_id = models.CharField(max_length=100, db_index=True)  # '2017_09_22_anamlb_houmlb_1'
    game_type = models.CharField(max_length=30, choices=GAME_TYPE_CHOICES, default='R')
    date = models.DateTimeField()  # 2017-09-22 20:10:00
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team_team')
    w_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='w_team_team')
    l_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='l_team_team')
    home_team_runs = models.IntegerField()  # 3
    away_team_runs = models.IntegerField()  # 0
    w_pitcher = models.CharField(max_length=100, db_index=True)  # 'Justin Verlander'
    l_pitcher = models.CharField(max_length=100, db_index=True)  # 'Yusmeiro Petit'
    sv_pitcher = models.CharField(blank=True, max_length=100, db_index=True)  # 'Ken Giles'
    youtube_id = models.CharField(max_length=20, blank=True)
    youtube_downloaded = models.BooleanField(default=False)
    youtube_start_offset = models.IntegerField(default=0)
    original_video_filename = models.CharField(max_length=100, blank=True)
    original_audio_filename = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.game_id

    @property
    def first_pitch_time(self):
        first_pitch = Pitch.objects.filter(at_bat__inning__game__game_id=self.game_id).first()

        return first_pitch.pitch_datetime

    # def download_youtube(self):
    #     if not self.youtube_id:
    #         return


class Inning(models.Model):
    TOP = 'top'
    BOTTOM = 'bottom'
    TOP_BOTTOM_CHOICES = [
        (TOP, 'Top'),
        (BOTTOM, 'Bottom'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='innings')
    inning = models.IntegerField()
    top_bottom = models.CharField(max_length=10, choices=TOP_BOTTOM_CHOICES)

    def __str__(self):
        return f'{self.top_bottom} {self.inning}'

    class Meta:
        ordering = ['game__date', 'inning']


class AtBat(models.Model):
    play_guid = models.CharField(max_length=50, blank=True)
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, related_name='at_bat')
    at_bat_number = models.IntegerField()
    home_team_runs = models.IntegerField(default=0)
    away_team_runs = models.IntegerField(default=0)
    balls = models.IntegerField()
    strikes = models.IntegerField()
    outs = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    batter = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='at_bat_batter')
    pitcher = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='at_bat_pitcher')
    description = models.CharField(max_length=512, blank=True)
    event_number = models.IntegerField()
    event = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['start_time']


class Pitch(models.Model):
    BALL = 'B'
    STRIKE = 'S'
    IN_PLAY = 'X'

    PITCH_RESULT_CHOICES = [
        (BALL, 'ball'),
        (STRIKE, 'strike'),
        (IN_PLAY, 'in play'),
    ]
    CURVEBALL = 'CU'
    KNUCKLE_CURVE = 'KC'
    SCREWBALL = 'SC'
    SLIDER = 'SL'
    CHANGEUP = 'CH'
    KNUCKLEBALL = 'KN'
    EEPHUS = 'EP'
    CUTTER = 'FC'
    FOUR_SEAM_FASTBALL = 'FF'
    SPLITTER = 'FS'
    TWO_SEAM_FASTBALL = 'FT'
    SINKER = 'SI'
    PITCHOUT = 'FO'
    PITCHOUT_2 = 'PO'
    INTENTIONAL_BALL = 'IN'
    UNKNOWN = 'UN'
    UNIDENTIFIED = 'AB'
    UNIDENTIFIED_2 = 'FA'

    PITCH_TYPE_CHOICES = [
        (CURVEBALL, 'Curveball'),
        (KNUCKLE_CURVE, 'Knuckle Curve'),
        (SCREWBALL, 'Screwball'),
        (SLIDER, 'Slider'),
        (CHANGEUP, 'Changeup'),
        (KNUCKLEBALL, 'Knuckleball'),
        (EEPHUS, 'Eephus'),
        (CUTTER, 'Cutter'),
        (FOUR_SEAM_FASTBALL, 'Four-seam Fastball'),
        (SPLITTER, 'Splitter'),
        (TWO_SEAM_FASTBALL, 'Two-seam Fastball'),
        (SINKER, 'Sinker'),
        (PITCHOUT, 'Pitchout'),
        (PITCHOUT_2, 'Pitchout 2'),
        (INTENTIONAL_BALL, 'Intentional Ball'),
        (UNKNOWN, 'Unknown'),
        (UNIDENTIFIED, 'Unidentified'),
        (UNIDENTIFIED_2, 'Unidentified 2'),
    ]

    play_guid = models.CharField(max_length=50, blank=True)
    at_bat = models.ForeignKey(AtBat, on_delete=models.CASCADE, related_name='pitches')
    pitch_id = models.IntegerField()
    pitch_result = models.CharField(max_length=500, choices=PITCH_RESULT_CHOICES, verbose_name='pitch result')
    pitch_code = models.CharField(max_length=10)
    pitch_datetime = models.DateTimeField()
    game_pitch_id = models.CharField(max_length=30, blank=True)
    event_number = models.IntegerField()
    start_speed = models.DecimalField(max_digits=7, decimal_places=2)
    end_speed = models.DecimalField(max_digits=7, decimal_places=2)
    break_y = models.DecimalField(max_digits=6, decimal_places=2)
    break_angle = models.DecimalField(max_digits=6, decimal_places=2)
    break_length = models.DecimalField(max_digits=6, decimal_places=2)
    pitch_type = models.CharField(max_length=10, choices=PITCH_TYPE_CHOICES)
    pitch_type_confidence = models.DecimalField(max_digits=6, decimal_places=3)
    zone = models.IntegerField()
    nasty = models.IntegerField()
    spin_dir = models.DecimalField(max_digits=8, decimal_places=3)
    spin_rate = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        ordering = ['pitch_datetime']
