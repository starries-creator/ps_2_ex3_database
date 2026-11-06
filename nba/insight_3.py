"""Data analysis for Insight 3: close NBA games."""

import sqlite3
from pathlib import Path

import pandas as pd


INSIGHT_3_SQL = (
    Path(__file__).resolve().parent.parent / "queries" / "insight_3.sql"
)


def close_game_trend(
    connection: sqlite3.Connection,
    query: str | None = None,
) -> pd.DataFrame:
    """
    Calculate the share of close games in each NBA season.

    Parameters
    ----------
    connection : sqlite3.Connection
        Open NBA database connection.
    query : str
        SQL query for the season-level analysis.

    Returns
    -------
    pandas.DataFrame
        Season, game count, close-game count,
        close-game percentage, and average margin.
    """
    duplicate = connection.execute(
        """
        SELECT game_id
        FROM game
        WHERE season_type = 'Regular Season'
          AND season_id GLOB '2[0-9][0-9][0-9][0-9]'
          AND CAST(SUBSTR(season_id, 2, 4) AS INTEGER)
              BETWEEN 1980 AND 2022
          AND game_id IS NOT NULL
          AND pts_home IS NOT NULL
          AND pts_away IS NOT NULL
          AND pts_home != pts_away
        GROUP BY game_id
        HAVING COUNT(*) > 1
        LIMIT 1
        """
    ).fetchone()

    if duplicate is not None:
        raise ValueError(f"Duplicate eligible game ID: {duplicate[0]}")

    if query is None:
        query = INSIGHT_3_SQL.read_text(encoding="utf-8")

    result = pd.read_sql_query(query, connection)

    if result.empty:
        raise ValueError("No eligible NBA games found.")

    return result
