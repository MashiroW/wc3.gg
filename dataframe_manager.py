import os
import json
import pandas as pd

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



def process_leaderboard_data_and_save(json_data):
    
    payload = json_data.get("payload", {})
    message = payload.get("message", {})

    mssageType = json_data.get("messageType", "")
    #print(mssageType)

    if mssageType != "UpdateLeaderboardData":
        raise ValueError("Invalid JSON data. MessageType isn't UpdateLeaderboardData")
    
    #print(json_data)

    # Check if the required keys are present
    """
    if "race" not in message or "rows" not in message:
        raise ValueError("Invalid JSON data. Missing 'race' or 'rows' key.")
    """
    
    # Save the JSON data in the "./databases/jsons" folder
    json_folder = "./databases/jsons"
    json_save_path = os.path.join(json_folder, "latest.json")
    with open(json_save_path, 'wb') as json_file:
        json_file.write(json.dumps(json_data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    searchRace = message["race"]
    season = message["seasonId"]
    gamemode = message["gameMode"]

    leaderboard_data = message["rows"]

    print("In packet - Min :", min(entry.get("rank", 0) for entry in leaderboard_data), "- Max :", max(entry.get("rank", 0) for entry in leaderboard_data))

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

        # Clear the JSON folder if the DataFrame is created for the first time
        if os.path.exists(json_folder):
            for file_name in os.listdir(json_folder):
                file_path = os.path.join(json_folder, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

    return dataframe

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