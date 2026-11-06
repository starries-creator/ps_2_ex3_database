
-- Insight 3: Close NBA games by regular season.
-- A close game has a final point margin of 5 or fewer.

WITH eligible_games AS (
    SELECT
        CAST(SUBSTR(season_id, 2, 4) AS INTEGER)
            AS season_start_year,
        ABS(pts_home - pts_away) AS point_margin
    FROM game
    WHERE season_type = 'Regular Season'
      AND season_id GLOB '2[0-9][0-9][0-9][0-9]'
      AND CAST(SUBSTR(season_id, 2, 4) AS INTEGER)
          BETWEEN 1980 AND 2022
      AND game_id IS NOT NULL
      AND pts_home IS NOT NULL
      AND pts_away IS NOT NULL
      AND pts_home != pts_away
)

SELECT
    season_start_year,
    COUNT(*) AS games,
    SUM(
        CASE WHEN point_margin <= 5 THEN 1 ELSE 0 END
    ) AS close_games,
    ROUND(
        100.0 * SUM(
            CASE WHEN point_margin <= 5 THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS close_game_pct,
    ROUND(AVG(point_margin), 2) AS mean_margin

FROM eligible_games
GROUP BY season_start_year
ORDER BY season_start_year;
