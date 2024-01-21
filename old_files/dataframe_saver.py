import os
import pandas as pd

def process_leaderboard_data(json_data, dataframe_path):
    # Check if the messageType is "UpdateLeaderboardData"
    if json_data.get("messageType") != "UpdateLeaderboardData":
        raise ValueError("Invalid messageType. Expected 'UpdateLeaderboardData'.")

    # Check if the payload key is present
    if 'payload' not in json_data:
        raise ValueError("Invalid JSON data. Missing 'payload' key.")

    payload = json_data["payload"]

    # Check if the message key is present
    if 'message' not in payload:
        raise ValueError("Invalid payload. Missing 'message' key.")

    message = payload["message"]
    leaderboard_data = message.get("rows", [])

    # Check if the DataFrame file exists
    if os.path.exists(dataframe_path):
        existing_dataframe = pd.read_csv(dataframe_path)
    else:
        columns = ["toonname", "battleTag", "avatarId", "rank", "mmr", "division", "wins", "losses", "draws"]
        existing_dataframe = pd.DataFrame(columns=columns)

    # Extract player information and create a new DataFrame
    new_data = []
    for entry in leaderboard_data:
        for player_data in entry.get("players", []):
            toonname = player_data.get("toonName", "")
            battleTag = player_data.get("battleTag", "")
            avatarId = player_data.get("avatarId", "")
            rank = entry.get("rank", "")
            mmr = entry.get("mmr", "")
            division = entry.get("division", "")
            wins = entry.get("wins", "")
            losses = entry.get("losses", "")
            draws = entry.get("draws", "")

            new_data.append([toonname, battleTag, avatarId, rank, mmr, division, wins, losses, draws])

    # Create a new DataFrame with the extracted data
    new_dataframe = pd.DataFrame(new_data, columns=existing_dataframe.columns)

    # Concatenate the existing DataFrame with the new DataFrame
    updated_dataframe = pd.concat([existing_dataframe, new_dataframe], ignore_index=True)

    # Save the updated DataFrame and overwrite the existing file
    updated_dataframe.to_csv(dataframe_path, index=False)

    return updated_dataframe