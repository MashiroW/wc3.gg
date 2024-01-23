import os
import json
import shutil
import pandas as pd
from tqdm import tqdm

def save_to_json(json_data):
    payload = json_data.get("payload", {})
    message = payload.get("message", {})

    mssageType = json_data.get("messageType", "")

    if mssageType != "UpdateLeaderboardData":
        raise ValueError("Invalid JSON data. MessageType isn't UpdateLeaderboardData")
    
    seasonId = message.get("seasonId", "")
    gameMode = message.get("gameMode", "")
    race = message.get("race", "NaN")
    
    leaderboard_data = message["rows"]
    min_rank = min(entry.get("rank", 0) for entry in leaderboard_data)
    max_rank = max(entry.get("rank", 0) for entry in leaderboard_data)

    # Create the JSON folder if it doesn't exist
    json_folder = "./databases/jsons/{0}_{1}_{2}/".format(seasonId, gameMode, race)
    os.makedirs(json_folder, exist_ok=True)

    # Save the JSON data in the folder
    json_save_path = os.path.join(json_folder, "{0}-{1}.json".format(min_rank, max_rank))

    with open(json_save_path, 'wb') as json_file:
        json_file.write(json.dumps(json_data, ensure_ascii=False, indent=2).encode('utf-8'))

def process_leaderboard_data_and_save(jsons_path="./databases/jsons/"):
    dataframes_save_paths = []

    # Iterate over the JSON files in the specified directory
    for folder_name in os.listdir(jsons_path):
        print("Processing JSONs inside:", folder_name)
        folder_path = os.path.join(jsons_path, folder_name)

        if os.path.isdir(folder_path):
            # Use tqdm to add a loading bar to the loop
            for file_name in tqdm(os.listdir(folder_path), desc=f"Processing {folder_name}", unit="file"):
                if file_name.endswith(".json"):
                    json_file_path = os.path.join(folder_path, file_name)

                    # Load the JSON data into a variable
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)

                        payload = json_data.get("payload", {})
                        message = payload.get("message", {})
                        mssageType = json_data.get("messageType", "")

                        if mssageType != "UpdateLeaderboardData":
                            raise ValueError("Invalid JSON data. MessageType isn't UpdateLeaderboardData")
                        
                        searchRace = message["race"]
                        season = message["seasonId"]
                        gamemode = message["gameMode"]

                        leaderboard_data = message["rows"]

                        #print("In current json - Min :", min(entry.get("rank", 0) for entry in leaderboard_data), "- Max :", max(entry.get("rank", 0) for entry in leaderboard_data))

                        dataframe_data = []
                        for entry in leaderboard_data:
                            players_data = entry.get("players", [])
                            toonnames = [player.get("toonName", "") for player in players_data]
                            battletags = [player.get("battleTag", "") for player in players_data]
                            avatarids = [player.get("avatarId", "") for player in players_data]

                            row_data = {
                                "rank": entry.get("rank", ""),
                                "mmr": entry.get("mmr", ""),
                                "searchRace": searchRace,
                                "race": entry.get("race", ""),
                                "toonname": toonnames,
                                "battleTag": battletags,
                                "avatarId": avatarids,
                                "division": entry.get("division", ""),
                                "wins": entry.get("wins", ""),
                                "losses": entry.get("losses", ""),
                                "draws": entry.get("draws", "")
                            }
                            dataframe_data.append(row_data)

                        dataframe = pd.DataFrame(dataframe_data)

                        # Save the DataFrame
                        save_path = "./databases/wc3_S{0}_{1}_{2}.csv".format(season, gamemode, "N-A" if searchRace == "" else searchRace)
                        dataframes_save_paths.append(save_path)
                        
                        # Check if the DataFrame file exists
                        if os.path.exists(save_path):
                            existing_dataframe = pd.read_csv(save_path)
                            
                            for row_data in dataframe_data:
                                # Check if a row with the same rank exists in the existing DataFrame
                                existing_row = existing_dataframe[existing_dataframe['rank'] == row_data['rank']]
                                
                                if not existing_row.empty:
                                    # If a row with the same rank exists, check if it's identical
                                    if not (existing_row.iloc[0] == pd.Series(row_data)).all():
                                        # If not identical, replace the row with the new data
                                        existing_dataframe = existing_dataframe[existing_dataframe['rank'] != row_data['rank']]
                                        existing_dataframe = pd.concat([existing_dataframe, pd.DataFrame([row_data])], ignore_index=True)
                                else:
                                    # If no row with the same rank, append the new data
                                    existing_dataframe = pd.concat([existing_dataframe, pd.DataFrame([row_data])], ignore_index=True)

                            # Sort the DataFrame by the "rank" column in ascending order
                            existing_dataframe['rank'] = pd.to_numeric(existing_dataframe['rank'], errors='coerce')
                            existing_dataframe = existing_dataframe.sort_values(by='rank')

                            # Save the updated DataFrame and overwrite the existing file
                            existing_dataframe.to_csv(save_path, index=False)
                        else:
                            # If the DataFrame file doesn't exist, create a new one
                            dataframe = dataframe.sort_values(by='rank')  # Sort the new DataFrame
                            dataframe.to_csv(save_path, index=False, mode='w')

    for save_path in dataframes_save_paths:
        duplicatas_correct_dataframe(dataframe_path=save_path)
    
def duplicatas_correct_dataframe(dataframe_path):
    print("Correcting duplicated values in:", dataframe_path)

    # Read the DataFrame from the CSV file
    df = pd.read_csv(dataframe_path)

    # Remove duplicates based on the "rank" field, keeping the one with the highest value
    df = df.sort_values(by='rank', ascending=False).drop_duplicates(subset=["mmr", "searchRace", "race", "toonname", "battleTag", "avatarId", "division", "wins", "losses", "draws"], keep='first').sort_index()

    # Adjust ranks to ensure continuity
    df['rank'] = range(1, len(df) + 1)

    # Save the processed DataFrame back to the CSV file
    df.to_csv(dataframe_path, index=False)

def determine_movement(df_path, latest_json_path="./databases/jsons/latest.json"):
    # Read DataFrame from the provided path
    df = pd.read_csv(df_path)

    # Extract actual ranks from the DataFrame
    actual_ranks = set(df['rank'])

    # Extract ranks from the latest JSON
    with open(latest_json_path, 'r', encoding='utf-8') as json_file:
        latest_json = json.load(json_file)
    latest_ranks = set(entry['rank'] for entry in latest_json['payload']['message']['rows'])

    # Find the missing ranks between the last two sets in your DataFrame
    missing_ranks = set(range(1, max(actual_ranks))) - actual_ranks

    # Check if you should go left or right
    go_left = min(missing_ranks) < min(latest_ranks)
    go_right = min(missing_ranks) > min(latest_ranks)

    print("Min latest:",  min(latest_ranks))
    print("Max latest:",  max(latest_ranks))

    # Determine the action based on the conditions
    if go_left:
        action = "previous"
    elif go_right:
        action = "next"
    else:
        action = "refresh"  # No movement needed

    return action

def dump_jsons_folder(folder_path="./databases/jsons/"):
    try:
        # Iterate over all the entries in the directory
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            
            # Check if it's a file or directory and delete accordingly
            if os.path.isfile(entry_path):
                os.unlink(entry_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                
        print(f"Contents of '{folder_path}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting contents of '{folder_path}': {e}")