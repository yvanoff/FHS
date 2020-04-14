# -*- coding: utf-8 -*-
""" This module contains a round-robin tournament generator.

Constants
---------
    T       Generic unbounded TypeVar for create_schedule.
    Team    Represents a team for type checking purposes.
    Game    Represents a game for type checking purposes.

Functions
---------
    create_schedule     generates a schedule for a round-robin tournament.
"""
import itertools
from collections import deque
from typing import Deque, List, Tuple, TypeVar, Union

# Generic TypeVar for games
T = TypeVar("T")

# Team type: Union of a TypeVar with str (for "BYE" with odd team counts)
Team = Union[T, str]

# Game type: Tuple of teams
Game = Tuple[Team, Team]


def create_schedule(base_team_list: List[T], return_game: bool) -> List[List[Game]]:
    """ Generates a round-robin tournament schedule based on the team list.

    The schedule is generated based on the circle method given at:
     https://en.wikipedia.org/wiki/Round-robin_tournament

    Parameters
    ----------
    base_team_list : List[T]
        List of teams. Any type can be given.
    return_game : bool
        Whether to generate return games.

    Returns
    -------
    List[List[Game]]
        Returns a full round-robin tournament schedule for the given team list.
        The schedule contains a list for all tournament rounds, further divided
        in games.

    See Also
    --------
    Game : game type helper for type checking.
    Team : team type helper for type checking.

    """
    schedule: List[List[Game]] = []
    schedule_return: List[List[Game]] = []

    # Contains the team list, possibly with "BYE" added if the count is odd.
    # Note: the incoming team list is first copied.
    team_list: List[Team] = list(base_team_list)
    # Add dummy team if the team count is odd
    if len(base_team_list) % 2 == 1:
        team_list.append("BYE")

    # Create a deque without the non-moving competitor
    circle: Deque[Team] = deque(team_list[1:])

    current_round: int
    for current_round in range(len(team_list) - 1):
        # First row in the algorithm -- home teams
        # Contains the non-moving competitor and the first half of the circle
        home_teams: List[Team] = [team_list[0]] + list(
            itertools.islice(circle, len(circle) // 2)
        )
        # Second row in the algorithm -- away teams
        # Contains the reversed second half of the circle (here, we instead
        # take the first half of the reversed circle)
        away_teams: List[Team] = list(
            itertools.islice(reversed(circle), len(circle) // 2 + 1)
        )
        round_games: List[Game] = list(zip(home_teams, away_teams))
        # Exchange home and away teams for the non-moving competitor to improve
        # fairness (i.e. ensure that no team is away or home too many times)
        if current_round % 2 == 1:
            print(round_games[0])
            round_games[0] = (round_games[0][1], round_games[0][0])
        schedule.append(round_games)
        if return_game:
            schedule_return.append([(game[1], game[0]) for game in round_games])
        # Rotate the deque without the non-moving competitor for the next round
        circle.rotate(1)

    if return_game:
        schedule.extend(schedule_return)

    return schedule
