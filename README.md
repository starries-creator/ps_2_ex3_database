# PS2 Exercise 3 — NBA database analysis

This repository analyses the NBA dataset specified for Exercise 3,
`wyattowalsh/basketball` on Kaggle. The completed warm-up and four SQL-based
analyses use the dataset's `nba.sqlite` database.

## Reproduce the analysis

Install Git and [Pixi](https://pixi.sh/latest/installation/) first. Run the
following commands in a terminal.

### 1. Clone the repository and install the environment

```bash
git clone https://github.com/starries-creator/ps_2_ex3_database.git
cd ps_2_ex3_database
pixi install --locked -e nba
pixi run -e nba python -m ensurepip
pixi run -e nba python -m pip install --no-deps --no-build-isolation .
pixi run -e nba pre-commit install
pixi run -e nba pre-commit run --all-files
```

Run the remaining commands from the repository root. The `nba` environment
uses Python 3.12 and the committed lock file. The setup and notebook execution
have been tested on macOS Apple Silicon. The lock file also resolves macOS Intel,
Linux x86-64 and Windows x86-64 dependencies.

### 2. Prepare the Kaggle database

Follow the course [Data Preparation instructions](https://jewel-scowl-daa.notion.site/Ex-3-Database-028a2a09d106833eb3728104e6ec9dd4)
to create a Kaggle account and generate API credentials in your
[account settings](https://www.kaggle.com/settings/api), following the
[official Kaggle CLI authentication instructions](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication).
To use the legacy credentials described in the course instructions, select
“Create Legacy API Key” and place the downloaded `kaggle.json` in `~/.kaggle/`.
The Kaggle CLI is installed in the Pixi environment. Keep credentials private
and outside the repository.

Download the course dataset's SQLite file using the authenticated Kaggle CLI.

```bash
mkdir -p data
pixi run -e nba kaggle datasets download wyattowalsh/basketball -f nba.sqlite -p data --unzip
```

The notebook expects the resulting file at `data/nba.sqlite`. Database and
CSV files are ignored by Git and must be obtained separately from the clone.

### 3. Verify the database and run the notebooks

```bash
pixi run -e nba validate --data data/nba.sqlite
pixi run -e nba python -m unittest discover -s tests -v
pixi run -e nba jupyter
```

The validation command reports the `game` row count and database SHA-256. The
snapshot used for the findings contains 65,698 game records and has SHA-256
`65b6412234d2d8817678d04f7cd2548aec82fec02b6c5b86679cade7572c21c7`.
A later Kaggle dataset version may produce a different hash and results.

In JupyterLab, select the `nba` environment's Python kernel. Run
[warm_up.ipynb](warm_up.ipynb) and then [analysis.ipynb](analysis.ipynb) from
top to bottom. The analysis notebook imports the packaged functions and shows
the four SQL-backed analyses, figures and interpretations.

## Work completed

- Completed the database warm-up covering schema, table names, game columns and
  recorded date range.
- Made the project installable with `pyproject.toml`, packaged its SQL queries,
  and configured the ignored data files and pre-commit hooks.
- Added reusable analysis and plotting functions, four SQL queries, figures
  and a combined notebook. The database connection is opened read-only.
- Documented the data loader, the `__main__` guard and Click in
  [data loader notes](docs/data_loader_notes.md).

## Findings

These findings describe the available database snapshot. The analyses use
different populations and periods.

- **Home wins.** The designated home team won 28,502 of 47,027 eligible
  regular-season games across 42 recorded seasons. The share was 62.1% in
  1980–81 and 58.0% in 2022–23.
  [Notebook](insight_1_home_wins.ipynb) · [SQL](queries/insight_1.sql)
- **Three-point attempts.** Recorded attempts rose from 2.3 to 34.2 per team
  per game between 1981–82 and 2022–23. Their share of field-goal attempts rose
  from 2.6% to 38.7% among games with complete attempt data. The first
  season's three-point attempt data covers 113 of 943 games.
  [Notebook](insight_2.ipynb) · [SQL](queries/insight_2.sql)
- **Close games.** Games decided by five points or fewer represented 32.77%
  of eligible games in 1980–81 and 27.56% in 2022–23. The rate fluctuated
  across seasons. Final margin is one measure of how competitive a game was.
  [Notebook](insight_3_close_games.ipynb) · [SQL](queries/insight_3.sql)
- **Games by month.** Across the 65,698 recorded games, March has the highest
  count at 11,269 and July the lowest at 16. Historical coverage and game
  types affect the distribution.
  [Notebook](insight_4_E.ipynb) · [SQL](queries/insight_4.sql)

The home-win and close-game analyses cover 42 available seasons between 1980–81
and 2022–23. The three-point analysis begins in 1981–82. The database has no
recorded regular-season games for 2012–13, which is shown as a gap in the
relevant charts.
