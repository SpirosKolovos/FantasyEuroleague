# Load the libraries
from euroleague_api.EuroLeagueData import EuroLeagueData
from euroleague_api.boxscore_data import BoxScoreData

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

# Firstly, we need to do some Data processing
# First of all, we download the data which contain all statistics

previous_season = 2023
current_season = 2024
game_code = 1
competition_code = "E"

season_data = EuroLeagueData(competition_code)
df_season_data_previous = season_data.get_game_metadata_season(season=previous_season)
df_season_data_current = season_data.get_game_metadata_season(season=current_season)

df_season_data_previous['season'] = previous_season
df_season_data_current['season'] = current_season

df_season_data = pd.concat([df_season_data_previous, df_season_data_current])

# Combine the 'date' and 'time' columns into a single column
df_season_data['datetime'] = df_season_data['date'] + ' ' + df_season_data['time']

# Convert the combined column into a datetime object
df_season_data['datetime'] = pd.to_datetime(df_season_data['datetime'], format='%b %d, %Y %H:%M')

# drop date, time
df_season_data.drop(['date', 'time'], inplace=True, axis=1)

df_season_data = df_season_data.sort_values(by='datetime')

# Initialize an empty DataFrame to hold all player statistics
all_player_stats = pd.DataFrame()

boxscore = BoxScoreData(competition_code)

# Iterate over the matches DataFrame
for _, row in df_season_data.iterrows():
    season = row['season']
    gamenumber = row['gamenumber']
    
    # Fetch player statistics for the current game using boxscore.get_boxscore_data
    player_stats = boxscore.get_player_boxscore_stats_data(season=season, gamecode = gamenumber)
    
    # Assuming player_stats is already a DataFrame, or you can convert it to one
    # Append the fetched statistics to the all_player_stats DataFrame
    all_player_stats = pd.concat([all_player_stats, player_stats], ignore_index=True)
    
    print('Gamenumber: ', gamenumber, 'Season: ', season)

# Display the final DataFrame with all player statistics
print(all_player_stats)

# Next data processing steps:
# 1. Remove data that is not of a single player (i.e., Team, Total)
# 2. Add the team score and opponent score
# 3. Add the position of each player
# 4. Caclulate the fantasy points 
