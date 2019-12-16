import json
from urllib.error import HTTPError
from urllib.request import urlopen

from config.settings.base import APPS_DIR

START_YEAR = 2016
END_YEAR = 2019
ROSTER_ALLTIME_URL = 'http://mlb.mlb.com/lookup/json/named.roster_team_alltime.bam?team_id={0}&start_season={1}&end_season={2}'
ORIGINAL_VIDEO_DIR = str(APPS_DIR.path('data/videos/original'))


def get_roster_alltime(team_id, start_year=START_YEAR, end_year=END_YEAR):
    """Return the roster file of team with matching id."""
    try:
        return urlopen(ROSTER_ALLTIME_URL.format(team_id, start_year, end_year))
    except HTTPError:
        raise ValueError('Could not find a roster for a team with that id.')


def roster_alltime(team_id, start_year=START_YEAR, end_year=END_YEAR):
    """Returns a dictionary of roster information for team id"""
    data = get_roster_alltime(team_id, start_year, end_year)
    parsed = json.loads(data.read().decode('latin-1'))
    players = parsed['roster_team_alltime']['queryResults']['row']
    return {'players': players, 'team_id': team_id}
