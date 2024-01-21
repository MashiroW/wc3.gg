import os
import asyncio
import websockets
import json
import time
import pandas as pd

local_url = "http://127.0.0.1:31039/webui/index.html?guid=16750297169692417202"

port = local_url.split(":")[2].split("/")[0]
guid = local_url.split("guid=")[1]

import os
import pandas as pd
import json
import traceback

def process_leaderboard_data_and_save(json_data):
    payload = json_data.get("payload", {})
    message = payload.get("message", {})

    mssageType = json_data.get("messageType", "")
    #print(mssageType)

    if mssageType != "UpdateLeaderboardData":
        raise ValueError("Invalid JSON data. MessageType isn't UpdateLeaderboardData")
    
    #print(json_data)

    # Check if the required keys are present
    if "race" not in message or "rows" not in message:
        raise ValueError("Invalid JSON data. Missing 'race' or 'rows' key.")
    
    searchRace = message["race"]
    season = message["seasonId"]
    gamemode = message["gameMode"]

    leaderboard_data = message["rows"]

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

    # Save the JSON data in the "./databases/jsons" folder
    json_folder = "./databases/jsons"
    json_save_path = os.path.join(json_folder, "latest.json")
    with open(json_save_path, 'wb') as json_file:
        json_file.write(json.dumps(json_data, ensure_ascii=False, indent=2).encode('utf-8'))

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

async def get_websocket_message(message=""):
    if message == "":
        message = {
            "message": ""
        }

    uri = "ws://127.0.0.1:{0}/webui-socket/{1}".format(port, guid)

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))
        #print(f"Sent message")

        response = await websocket.recv()
        #print(f"Received response")

        json_payload = json.loads(response)

        return json_payload

async def main():

    while True:
        try:
            json_payload = await get_websocket_message()
            process_leaderboard_data_and_save(json_data=json_payload)
            print("Inserted Data !")

        except Exception as e:
            print(e)
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())