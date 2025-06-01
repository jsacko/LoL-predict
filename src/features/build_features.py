
# Feature engineering for the dataset
import pandas as pd
import logging
import yaml
import json
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import requests
import hydra
from omegaconf import DictConfig
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def winner_series_filtering(df, cols_to_be_unique):
    # Load configuration
    # Drop games not complete
    new_df = df[df["datacompleteness"] == "complete"]

    # Define columns to be removed and drop them (useless columns)
    useless_columns = (
        ["participantid", "side", "position", "teamid", "teamkills", "teamdeaths","url"] +
        [f"ban{b}" for b in range(1, 6)] +
        [f"pick{p}" for p in range(1, 6)]
    )
    
    new_df = new_df.drop(columns=useless_columns)
        # Colonnes à garder même si elles ont une seule valeur
    exceptions = set(cols_to_be_unique)
    
    # Colonnes à supprimer : elles ont une seule valeur et ne sont pas dans exceptions
    cols_to_drop = [col for col in new_df.columns if new_df[col].nunique() <= 1 and col not in exceptions]
    
    # On les supprime
    new_df = new_df.drop(columns=cols_to_drop)
    
    return new_df

def select_teams_rows(df):
    
    new_df = df[df["playername"].isnull()] # Select only team's row with aggregate data
    series_empty = new_df.isna().sum()
    columns_with_all_rows_empty = series_empty[series_empty == new_df.shape[0]].index.tolist()
    columns_to_drop = ["firstbloodkill","firstbloodassist","firstbloodvictim","champion"]
    new_df = new_df.drop(columns=columns_with_all_rows_empty+ columns_to_drop, axis=1) # Drop full columns empty
    new_df = new_df[(new_df.game.isnull() == False) & (new_df.teamname.isnull() == False)] 
    series_empty = new_df.isna().sum()
    
    #print(set(series_empty[series_empty != 0].index.tolist())-set(columns_mean)-set(columns_to_let_xgb)-set(columns_to_set_0))
    
    #print("\n".join(series_empty[series_empty != 0].index.astype(str)))
    #print(len(series_empty[series_empty != 0].index))
    #print("\n".join(f"{index}: {value}" for index, value in series_empty[series_empty != 0].items()))

    #print(series_empty[series_empty != 0])
    #new_df = new_df.dropna(axis=1)
    return new_df

def aggregate_bo(df, cols_to_be_unique, include_objects_columns=False):
    """
    This function processes the given dataframe `df`, which contains match data, 
    by cleaning, grouping, and calculating statistics for each Best-of (Bo) series 
    and each team within the series.
    """
    # Load configuration
    #assert not df.isnull().values.any(), "Dataset contains missing values, cannot aggregate BO"
    
    # Step 1: Sort the data by date and team name to organize the games
    team_games = df.sort_values(by=["date", "gameid","teamname"]).copy()
    counts_index = team_games.index.value_counts()
    
    #team_games = team_games[team_games.index.isin(counts_index[counts_index > 1].index)]
    #display(team_games[team_games.index== "ESPORTSTMNT02_2342149"])
    #display(team_games[team_games["date"]=="2025-01-23 16:22:48"])
    
    # Step 2: Separate the team data for left and right teams based on row order
    teams_stats_left = team_games.iloc[::2]  # Select rows for team A
    teams_stats_right = team_games.iloc[1::2]  # Select rows for team B
    #print("List of columns before creating A and B",team_games.columns.tolist())
    # Step 3: Join the stats of the two teams (team A and team B) into one DataFrame
    teams_group = teams_stats_left.join(teams_stats_right, lsuffix="A", rsuffix="B")
    # Make a unique column for same value between match 
    cols_b_drop = [col + 'B' for col in cols_to_be_unique]
    teams_group = teams_group.drop(columns=cols_b_drop, axis=1) 
    teams_group.rename(columns={col+"A":col for col in cols_to_be_unique }, inplace=True) 
    
    teams_group = teams_group[(teams_group["teamnameA"]!="unknown team") & (teams_group["teamnameB"] !="unknown team")]
    teams_group = teams_group.dropna(subset=["teamnameA","teamnameB"],axis=0)
    # Step 4: Initialize the dictionary to store unique Bo IDs and track the count
    dict_bo = {"id": 0}
    # Step 5: Define a function to identify the Bo series ID (`bo_id`) for each match
    def identify_bo_id(row):
        # Define a unique key for each Bo series based on the team names
        if (isinstance(row.teamnameA, float) | isinstance(row.teamnameB, float)):
            print("teamA",row.teamnameA)
            print("teamB", row.teamnameB)
            print("game",row)
            
        key = row.teamnameA + "_" + row.teamnameB if row.teamnameA < row.teamnameB else row.teamnameB + "_" + row.teamnameA
        
        # Check if this is the first game of a Bo series
        if row["game"] == 1:  # If this is the first game of the Bo series
            # Assign a new Bo ID for this series and increment the counter
            dict_bo[key] = dict_bo["id"] #row.name
            dict_bo["id"] += 1
            return dict_bo[key]
        else:
            # If the Bo series already exists, return the existing Bo ID
            return dict_bo.get(key)  # Return the Bo ID, if already exists
    
    # Step 6: Apply the `identify_bo_id` function to each row and add the Bo ID to the DataFrame
    teams_group["bo_id"] = teams_group.apply(identify_bo_id, axis=1)
    # Step 7: Drop rows where `bo_id` is missing (if any) and convert `bo_id` to integer type
    #teams_group.dropna(axis=0, inplace=True)
    teams_group = teams_group[teams_group["bo_id"].isnull() == False]
    teams_group["bo_id"] = teams_group["bo_id"].astype(int)
    # Step 8: Calculate the Bo type (Bo1, Bo3, Bo5) based on the number of games in the series
    def get_type_bo(df):
        nb_games = df.game.count()
        if nb_games == 1:
            return 1  # Bo1
        elif nb_games == 2:
            return 3  # Bo3
        elif nb_games == 3:
            # If Bo3, check if there was a winner by 3 games in a row
            if df.resultA.mean() == 1 or df.resultB.mean() == 1:
                return 5  # Bo5 won by 3 victories in a row
            else:
                return 3  # Bo3 with 1 defeat
        else:
            return 5  # Bo5 (4 or 5 games)

    # Step 9: Calculate the mean statistics for each group (Bo series) while keeping 4 decimal precision
    nums_cols = teams_group.select_dtypes(include=["number"]).columns  # Get all numeric columns
    X = teams_group.groupby("bo_id")[nums_cols].mean().round(4)
    
    # Add object columns by taking the first value for each group
    object_cols = teams_group.select_dtypes(include=["object"]).columns.tolist()
    if ("bo_id" in object_cols):
        object_cols.remove("bo_id")
    # Use .transform to get the first value for each group for object columns
    if (not include_objects_columns):
        object_cols = ["teamnameA","teamnameB"]

    # Step 10: Add `teamnameA`, `teamnameB`, and `bo_type` for each group (Bo series)
    X[["bo_type"]+object_cols] = teams_group.groupby("bo_id").apply(
        lambda df: pd.Series({
            "bo_type": get_type_bo(df),
            **{col: df[col].iloc[0] for col in object_cols}
        }),
        include_groups=False
    ).reset_index(drop=True)  # Reset the index to align the results correctly
    
    # Step 11: Clean up the resulting DataFrame by dropping unnecessary columns
    X.drop(columns=["game"], inplace=True)

    # Return the final DataFrame with team statistics by Bo series
    return X

def create_features_from_df(df, cols_to_be_unique, include_objects_columns=False):
    # Load configuration
    BASE_ELO = 1500  # Starting ELO for new teams
    K_FACTOR = 45  # ELO adjustment speed
    WINDOW_SIZE = 1  # Number of past matches to compute rolling averages
    WINDOW_RECENT = 5

    new_df = winner_series_filtering(df, cols_to_be_unique)
    new_df = select_teams_rows(new_df)

    nums_cols_avg_stats = new_df.select_dtypes(include="number").columns.tolist()
    cols_to_remove = ["game","participantid","teamkills","teamdeaths","result"] + cols_to_be_unique
    nums_cols_avg_stats = [x for x in nums_cols_avg_stats if x not in cols_to_remove]
    league_avg = {stats: new_df[stats].mean() for stats in nums_cols_avg_stats} # Mean stats for the first game of team's

    dict_stats = {team: {col:[] for col in nums_cols_avg_stats } | {"h2h":[], "result":[], "bo_1":[],"bo_3":[],"bo_5":[], "win_streak":[], "elo":[BASE_ELO]} for team in set(new_df.teamname) }

    # Initialize the first team with the base ELO 
    #1. S'assurer que la date est bien en format datetime
    new_df['dateparsed'] = pd.to_datetime(new_df['date'])
    
    # 2. Calculer la limite de 6 mois depuis la date min
    date_limite = new_df['dateparsed'].min() + pd.DateOffset(months=6)
    
    # 3. Identifier les équipes présentes pendant cette période
    teams_initial_elo = new_df[new_df['dateparsed'] <= date_limite]['teamname'].unique()
    
    # 4. Initialiser leur ELO à 1500 dans dict_stats
    for team in teams_initial_elo:
        dict_stats[team]['elo'].append(BASE_ELO)
    
    new_df = aggregate_bo(new_df, cols_to_be_unique, True)    
    new_df["result"] = new_df.resultB.map(lambda row: 1 if row >0.5 else 0) # 0 if TeamA win , 1 if TeamB win
    new_df = new_df.drop(columns=["resultA","resultB"])

    # Constants
    
    
    league_avg["elo"] = BASE_ELO
    
    
    #Function to calculate ELO updates
    def calculate_elo(elo_A, elo_B, result_B, K):
        expected_A = 1 / (1 + 10 ** ((elo_B - elo_A) / 400))
        expected_B = 1 - expected_A
        new_elo_A = elo_A + K * ((1-result_B) - expected_A)
        new_elo_B = elo_B + K * (result_B - expected_B)
        return new_elo_A, new_elo_B
    
    # Initialize empty DataFrame
    # team_stats_df = pd.DataFrame(columns=["team","elo"] + nums_cols_avg_stats + ["result"])
    
    # # Function to get rolling averages safely
    # def get_team_stat(team, col):
    #     team_data = team_stats_df[team_stats_df["team"] == team]
    #     if len(team_data) >= WINDOW_SIZE:
    #         return team_data[col].rolling(WINDOW_SIZE).mean().iloc[-1]
    #     return league_avg[col]  # Default to league average if not enough data
    
    # Process each match
    # Buffer pour stocker les valeurs calculées
    data_buffer = []
    
    for i, row in new_df.iterrows():
        team_A, team_B = row["teamnameA"], row["teamnameB"]
        row_result = {}
    
        # ELO pré-match
        # if (len(dict_stats[team_A]["elo"]) == 0):
        #     elos = [stats["elo"] for stats in dict_stats.values() if isinstance(stats, dict)]
        #     mean_elo = np.percentile([e for sublist in elos for e in sublist], 75)
        #     dict_stats[team_A]["elo"].append(mean_elo)
        # if (len(dict_stats[team_B]["elo"]) == 0):
        #     elos = [stats["elo"] for stats in dict_stats.values() if isinstance(stats, dict)]
        #     mean_elo = np.percentile([e for sublist in elos for e in sublist], 75)
        #     dict_stats[team_B]["elo"].append(mean_elo)
        pre_game_elo_A = dict_stats[team_A]["elo"][-1]
        pre_game_elo_B = dict_stats[team_B]["elo"][-1]
        row_result["elo_diff"] = pre_game_elo_A - pre_game_elo_B
    
        # H2H win rate
        h2h_key = team_A + team_B
        values = dict_stats.get(h2h_key)
        if isinstance(values, list):
            h2h_win_rate_AvsB = np.mean(values) if values else 0.5
        else:
            h2h_win_rate_AvsB = 0.5  # fallback
        row_result["h2h_win_rate_AvsB"] = h2h_win_rate_AvsB
        dict_stats[team_A]["h2h"].append(h2h_win_rate_AvsB)
        dict_stats[team_B]["h2h"].append(1 - h2h_win_rate_AvsB)

        # Nb games diff
        row_result["nb_games_diff"] = len(dict_stats[team_A]["result"]) - len(dict_stats[team_B]["result"])

        # new games
        row_result["new_games"] = (len(dict_stats[team_A]["result"]) <= 5 | len(dict_stats[team_B]["result"]) <=5)

        # Win streaks
        def compute_win_streak(results):
            win_streak = 0
            idx = len(results) - 1
            while idx >= 0 and results[idx] == 1:
                win_streak += 1
                idx -= 1
            return win_streak
        
        # Utilisation
        win_streak_A = compute_win_streak(dict_stats[team_A]["result"])
        win_streak_B = compute_win_streak(dict_stats[team_B]["result"])
        dict_stats[team_A]["win_streak"].append(win_streak_A)
        dict_stats[team_B]["win_streak"].append(win_streak_B)
        # row_result["win_streakA"] = win_streak_A
        # row_result["win_streakB"] = win_streak_B
        row_result["win_streak_diff"]  = win_streak_A - win_streak_B
        
        # Win rates globaux et par BO
        team_A_res, team_B_res = dict_stats[team_A]["result"], dict_stats[team_B]["result"]
        row_result["team_A_win_rate"] = np.mean(team_A_res) if len(team_A_res) >= WINDOW_SIZE else 0.5
        row_result["team_B_win_rate"] = np.mean(team_B_res) if len(team_B_res) >= WINDOW_SIZE else 0.5

        # Win rate BO Diff
        win_rate_bo_A = np.mean(dict_stats[team_A][f"bo_{row['bo_type']}"]) if len(dict_stats[team_A][f"bo_{row['bo_type']}"]) >= WINDOW_SIZE else row_result["team_A_win_rate"]
        win_rate_bo_B = np.mean(dict_stats[team_B][f"bo_{row['bo_type']}"]) if len(dict_stats[team_B][f"bo_{row['bo_type']}"]) >= WINDOW_SIZE else row_result["team_B_win_rate"]
        row_result["win_rate_bo_diff"] = win_rate_bo_A - win_rate_bo_B
        for window in [3, 5, 10]:
            win_rate_A = np.mean(team_A_res[-window:]) if len(team_A_res) >= window else row_result["team_A_win_rate"]
            win_rate_B = np.mean(team_B_res[-window:]) if len(team_B_res) >= window else row_result["team_B_win_rate"]
            row_result[f"win_rate_last_{window}_diff"] = win_rate_A - win_rate_B
    
        # Moyennes de stats
        for col in nums_cols_avg_stats:
            stat_A = np.mean(dict_stats[team_A][col]) if len(dict_stats[team_A][col]) >= WINDOW_SIZE else league_avg[col]
            stat_B = np.mean(dict_stats[team_B][col]) if len(dict_stats[team_B][col]) >= WINDOW_SIZE else league_avg[col]
            row_result[col + "_diff"] = stat_A - stat_B
            dict_stats[team_A][col].append(row[col + "A"])
            dict_stats[team_B][col].append(row[col + "B"])
    
        # Append dans le buffer
        data_buffer.append(row_result)
    
        # Mise à jour ELO & résultats
        new_elo_A, new_elo_B = calculate_elo(pre_game_elo_A, pre_game_elo_B, row["result"], K_FACTOR)
        dict_stats[team_A]["elo"].append(new_elo_A)
        dict_stats[team_B]["elo"].append(new_elo_B)
    
        for key in ["result", f"bo_{row['bo_type']}"]:
            dict_stats[team_A][key].append(1 - row["result"])
            dict_stats[team_B][key].append(row["result"])
    
        dict_stats.setdefault(h2h_key, []).append(1 - row["result"]) # type: ignore
    
    # Fusion des colonnes calculées avec new_df
    stats_df = pd.DataFrame(data_buffer)
    new_df.reset_index(drop=True, inplace=True)
    new_df = pd.concat([new_df, stats_df], axis=1)
    new_df.index.name = "bo_id"
    
    # Calcul win_rate_diff final
    new_df["win_rate_diff"] = new_df["team_A_win_rate"] - new_df["team_B_win_rate"]
    
    return new_df, dict_stats

def create_features_from_tomorrow_game(dict_stats, cfg) -> pd.DataFrame: 
    url_leaguepedia = cfg["data"]["url_leaguepedia_api"]
    features = cfg["data"]["features"]
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    

    # Prepare the parameters for the API request
    params = {
    "action": "cargoquery",
    "format": "json",
    "tables": "MatchSchedule",
    "fields": "MatchSchedule.Team1,MatchSchedule.Team2,MatchSchedule.DateTime_UTC,MatchSchedule.OverviewPage,MatchSchedule.BestOf,MatchSchedule.Round",
    "where": f"MatchSchedule.DateTime_UTC >= '{tomorrow}'",
    "order_by": "MatchSchedule.DateTime_UTC ASC",
    "limit": "500"  # Augmente si nécessaire
    }
    response = requests.get(url=url_leaguepedia, params=params)

    if response.status_code == 200:
        results = response.json()["cargoquery"]
        # Étape 2 : Grouper les matchs par date (UTC, sans l'heure)
        match_data = [
            {
                "teamnameA": m["title"]["Team1"],
                "teamnameB": m["title"]["Team2"],
                "date": m["title"]["DateTime UTC"],
                "playoffs": 0 if m["title"]["Round"] is None else 1,
                "bo_type": m["title"]["BestOf"],
                "league": m["title"]["OverviewPage"].split("/")[0]
            }
            for m in results
        ]
        df = pd.DataFrame(match_data)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        
        # Étape 3 : Trouver la date de la prochaine journée (la première date du DataFrame)
        if not df.empty:
            next_match_day = df["date"].min()
            df_next_day = df[df["date"] == next_match_day]
        else:
            logging.info("No matches upcoming for")
            df_next_day = pd.DataFrame()
    else:
        logging.error(f"Failed to fetch data from Leaguepedia API: {response.status_code}")
        return pd.DataFrame()
    
    def create_feature_by_teamname(row, dict_stats=dict_stats):
        for col in features:
            if (col.endswith("_diff")):
                if (col.startswith("win_rate_last_")):
                    window = int(col.split("_")[3])
                    row[col] = np.mean(dict_stats.get(row.teamnameA).get("result")[-window:]) - np.mean(dict_stats.get(row.teamnameB).get("result")[-window:])
                elif (col == "win_rate_diff"):
                    row[col] = np.mean(dict_stats.get(row.teamnameA).get("result")) - np.mean(dict_stats.get(row.teamnameB).get("result"))
                elif (col == "win_rate_bo_diff"):
                    win_rate_bo_A = np.mean(dict_stats[row.teamnameA][f"bo_{row['bo_type']}"]) if len(dict_stats[row.teamnameA][f"bo_{row['bo_type']}"]) >= 1 else np.mean(dict_stats.get(row.teamnameA).get("result"))
                    win_rate_bo_B = np.mean(dict_stats[row.teamnameB][f"bo_{row['bo_type']}"]) if len(dict_stats[row.teamnameB][f"bo_{row['bo_type']}"]) >= 1 else np.mean(dict_stats.get(row.teamnameB).get("result"))
                    row[col] = win_rate_bo_A - win_rate_bo_B
                elif (col == "nb_games_diff"):
                    row[col] = len(dict_stats.get(row.teamnameA).get("result")) - len(dict_stats.get(row.teamnameB).get("result"))
                elif (col == "win_streak_diff"):
                    row[col] = dict_stats.get(row.teamnameA).get("win_streak")[-1] - dict_stats.get(row.teamnameB).get("win_streak")[-1]
                else:
                    row[col] = np.mean(dict_stats.get(row.teamnameA).get(col[:-5])) - np.mean(dict_stats.get(row.teamnameB).get(col[:-5]))
            elif (col == "h2h_win_rate_AvsB"):
                if (row.teamnameA < row.teamnameB):
                    h2h_key = row.teamnameA + row.teamnameB
                    h2h_win_rate_AvsB = np.mean(dict_stats[h2h_key]) if dict_stats.get(h2h_key) else 0.5
                else:
                    h2h_key = row.teamnameB + row.teamnameA 
                    h2h_win_rate_AvsB = (1 - np.mean(dict_stats[h2h_key])) if dict_stats.get(h2h_key) else 0.5
                row["h2h_win_rate_AvsB"] = h2h_win_rate_AvsB
        return row
    df_next_day = df_next_day[df_next_day.teamnameA.isin(dict_stats) & (df_next_day.teamnameB.isin(dict_stats)) ]
    df_next_day = df_next_day.apply(create_feature_by_teamname, axis=1).reset_index()
    df_next_day = df_next_day.drop(columns=["index"])
    return df_next_day


@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore
def main(cfg: DictConfig):
    
    df_prev_and_actual_season_data = pd.read_csv(f"{cfg['paths']['prev_and_actual_season_data']}", index_col="gameid", parse_dates=True, low_memory=False)
    logging.info("Creating features from the training data and new match downloaded...")
    cols_to_be_unique = list(cfg["data"]["unique_features"])
    X, teams_stats = create_features_from_df(df_prev_and_actual_season_data, cols_to_be_unique, include_objects_columns=True)
    logging.info(f"Features created with shape: {X.shape}")
    path_x = cfg["paths"]["processed_x"]
    X.to_csv(f"{path_x}")
    logging.info(f"""Features created and saved to {path_x} successfully. 
                    Now creating features for the next day matches...""")
    df_next_day = create_features_from_tomorrow_game(teams_stats, cfg)
    path_x_next_days = cfg["paths"]["processed_x_next_days"]
    df_next_day.to_csv(f"{path_x_next_days}")
    logging.info(f"Next day features created with shape: {df_next_day.shape} and saved to {path_x_next_days}")
    json.dump(teams_stats, open(cfg["paths"]["teams_stats"], "w"), indent=4)
    logging.info(f"Teams stats saved to {cfg['paths']['teams_stats']} successfully.")
    logging.info("Feature creation completed successfully.")

if __name__ == "__main__":
    main()