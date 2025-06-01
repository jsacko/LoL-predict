import pandas as pd
import numpy as np
import logging
import json
from omegaconf import DictConfig


#@hydra.main(config_path="../configs", config_name="config", version_base="1.3") # type: ignore
def build_features_from_teamnames(cfg:DictConfig, teamnameA:str, teamnameB:str, bo_type:str = "1") -> pd.DataFrame:
    features = cfg["data"]["features"]
    row = pd.DataFrame(columns=features)
    teams_stats_path = cfg["paths"]["teams_stats"]
    with open(teams_stats_path, "r") as f:
        teams_stats = json.load(f) 
    logging.info(f"Loaded teams stats from {teams_stats_path}")
    if teamnameA not in teams_stats or teamnameB not in teams_stats:
        logging.warning(f"One of the teams {teamnameA} or {teamnameB} is not found in the teams stats. Returning empty features.")
        return row
    for col in features:
        if (col.endswith("_diff")):
            if (col.startswith("win_rate_last_")):
                window = int(col.split("_")[3])
                row.at[0, col] = np.mean(teams_stats.get(teamnameA).get("result")[-window:]) - np.mean(teams_stats.get(teamnameB).get("result")[-window:])
            elif (col == "win_rate_diff"):
                row.at[0, col] = np.mean(teams_stats.get(teamnameA).get("result")) - np.mean(teams_stats.get(teamnameB).get("result"))
            elif (col == "win_rate_bo_diff"):
                win_rate_bo_A = np.mean(teams_stats[teamnameA][f"bo_{bo_type}"]) if len(teams_stats[teamnameA][f"bo_{bo_type}"]) >= 1 else np.mean(teams_stats.get(teamnameA).get("result"))
                win_rate_bo_B = np.mean(teams_stats[teamnameB][f"bo_{bo_type}"]) if len(teams_stats[teamnameB][f"bo_{bo_type}"]) >= 1 else np.mean(teams_stats.get(teamnameB).get("result"))
                row.at[0, col] = win_rate_bo_A - win_rate_bo_B
            elif (col == "nb_games_diff"):
                row.at[0, col] = len(teams_stats.get(teamnameA).get("result")) - len(teams_stats.get(teamnameB).get("result"))
            elif (col == "win_streak_diff"):
                row.at[0, col] = teams_stats.get(teamnameA).get("win_streak")[-1] - teams_stats.get(teamnameB).get("win_streak")[-1]
            else:
                row.at[0, col] = np.mean(teams_stats.get(teamnameA).get(col[:-5])) - np.mean(teams_stats.get(teamnameB).get(col[:-5]))
        elif (col == "h2h_win_rate_AvsB"):
            if (teamnameA < teamnameB):
                h2h_key = teamnameA + teamnameB
                h2h_win_rate_AvsB = np.mean(teams_stats[h2h_key]) if teams_stats.get(h2h_key) else 0.5
            else:
                h2h_key = teamnameB + teamnameA 
                h2h_win_rate_AvsB = (1 - np.mean(teams_stats[h2h_key])) if teams_stats.get(h2h_key) else 0.5
            row["h2h_win_rate_AvsB"] = h2h_win_rate_AvsB
    return row