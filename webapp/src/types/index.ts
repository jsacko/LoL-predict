export interface Match {
  bo_id: string
  index?: string 
  teamname_a?: string 
  teamname_b?: string 
  date?: string 
  playoffs?: string 
  bo_type?: number 
  monsterkillsownjungle_diff?: number 
  opp_xpat15_diff?: number 
  opp_deathsat25_diff?: number 
  earned_gpm_diff?: number 
  win_rate_last_5_diff?: number 
  opp_assistsat15_diff?: number 
  csdiffat15_diff?: number 
  firstbaron_diff?: number 
  goldspent_diff?: number 
  win_rate_last_3_diff?: number 
  wardsplaced_diff?: number 
  triplekills_diff?: number 
  assists_diff?: number 
  monsterkills_diff?: number 
  firstblood_diff?: number 
  elo_diff?: number 
  win_rate_diff?: number 
  h2h_win_rate_AvsB?: number 
  wardskilled_diff?: number 
  team_kpm_diff?: number 
  ckpm_diff?: number 
  controlwardsbought_diff?: number 
  totalgold_diff?: number 
  damagetakenperminute_diff?: number 
  gamelength_diff?: number 
  wcpm_diff?: number 
  win_rate_bo_diff?: number 
  nb_games_diff?: number 
  win_streak_diff?: number 
  prediction?: number  // corresponds to smallint in SQL
  prediction_proba?: number 
  result?: number | null
}

export interface Prediction {
  id: string
  user_id: string
  bo_id: string
  prediction: number 
  createdAt: string
  matches: Match
}

export type Leaderboard = {
  user_id: string;       // UUID of the user
  pseudo: string;        // Username or alias
  score: number;   // Computed total score
  rank: number;   
  accuracy: number;       // Computed leaderboard rank (e.g., with RANK())
  nb_predictions: number;
};

export type User = {
  id: string;
  email: string | null;
  pseudo: string;
  created_at: string;
};
