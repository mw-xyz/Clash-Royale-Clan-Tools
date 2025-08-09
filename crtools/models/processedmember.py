from datetime import datetime
from html import escape

import logging

from pyroyale import ClanMember

from crtools import leagueinfo
from crtools.scorecalc import ScoreCalculator
from crtools.models.warparticipation import WarParticipation

logger = logging.getLogger(__name__)

class ProcessedMember:
    """
    Represents a processed clan member with calculated and display-ready attributes.

    Attributes:
        tag (str): Player tag.
        name (str): Escaped player name for HTML.
        exp_level (int): Player experience level.
        trophies (int): Number of trophies.
        role (str): Clan role (e.g., member, elder).
        last_seen (datetime): Last seen timestamp.
        clan_rank (int): Current clan rank.
        previous_clan_rank (int): Previous clan rank.
        donations (int): Cards donated.
        donations_received (int): Cards received.
        clan_chest_points (int): Clan chest points.
        war_readiness (float or None): Calculated war readiness percentage.
        war_readiness_status (str): Readiness status ('good', 'normal', 'bad').
        arena_league (str): Arena league name.
        score (int): Calculated member score.
        vacation (bool): If the member is on vacation.
        safe (bool): If the member is marked as safe.
        blacklist (bool): If the member is blacklisted.
        no_promote (bool): If the member should not be promoted.
    """
    def __init__(self, member, war_readiness=None):
        self.tag = member.tag
        self.name = escape(member.name)
        self.exp_level = member.exp_level
        self.trophies = member.trophies
        self.role = member.role
        self.last_seen = member.last_seen
        self.clan_rank = member.clan_rank
        self.previous_clan_rank = member.previous_clan_rank
        self.donations = member.donations
        self.donations_received = member.donations_received
        self.clan_chest_points = member.clan_chest_points

        self.war_readiness = war_readiness

        self.war_readiness_status = 'normal'
        if war_readiness:
            if war_readiness > 75:
                self.war_readiness_status = 'good'
            elif war_readiness < 33:
                self.war_readiness_status = 'bad'

        self.arena_league = leagueinfo.get_arena_league_from_trophies(self.trophies)

        self.score = 0
        self.vacation = False
        self.safe = False
        self.blacklist = False
        self.no_promote = False

