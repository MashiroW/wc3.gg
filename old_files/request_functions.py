import os
import time
import asyncio
import websockets
import json
import time
import pyautogui
import pandas as pd
import traceback
import threading

local_url = "http://127.0.0.1:50915/webui/index.html?guid=13128299408618836118"

port = local_url.split(":")[2].split("/")[0]
guid = local_url.split("guid=")[1]

def process_leaderboard_data(json_data, dataframe_path):
    # Extract relevant information from JSON
    payload = json_data["payload"]
    message = payload["message"]
    leaderboard_data = message["rows"]

    # Check if the DataFrame file exists
    if os.path.exists(dataframe_path):
        existing_dataframe = pd.read_csv(dataframe_path)
    else:
        columns = ["toonname", "battleTag", "avatarId", "rank", "mmr", "division", "wins", "losses", "draws"]
        existing_dataframe = pd.DataFrame(columns=columns)

    # Extract player information and create a new DataFrame
    new_data = []
    for entry in leaderboard_data:
        for player_data in entry["players"]:
            toonname = player_data["toonName"]
            battleTag = player_data["battleTag"]
            avatarId = player_data.get("avatarId", "")
            rank = entry["rank"]
            mmr = entry["mmr"]
            division = entry["division"]
            wins = entry["wins"]
            losses = entry["losses"]
            draws = entry["draws"]

            new_data.append([toonname, battleTag, avatarId, rank, mmr, division, wins, losses, draws])

    # Check if the number of players is different from 25
    if len(new_data) != 25:
        raise ValueError(f"Expected 25 players, but found {len(new_data)} players.")

    # Create a new DataFrame with the extracted data
    new_dataframe = pd.DataFrame(new_data, columns=existing_dataframe.columns)

    # Concatenate the existing DataFrame with the new DataFrame
    updated_dataframe = pd.concat([existing_dataframe, new_dataframe], ignore_index=True)

    # Save the updated DataFrame and overwrite the existing file
    updated_dataframe.to_csv(dataframe_path, index=False)

    return updated_dataframe

def click_element_on_screen(element_image_path, confidence_threshold=0.8):

    #print(element_image_path)
    # Locate the element on the entire screen
    while True:
        try:
            element_location = pyautogui.locateOnScreen(element_image_path, confidence=confidence_threshold)

            if element_location:
                # Calculate the middle of the element
                middle_x = element_location.left + element_location.width / 2
                middle_y = element_location.top + element_location.height / 2

                # Click the middle of the element
                pyautogui.click(middle_x, middle_y)
                print("Clicked the middle of the element.")

                time.sleep(3)

                # Move the cursor to (0, 0) after clicking the element
                current_x, current_y = pyautogui.position()
                pyautogui.moveTo(current_x, current_y + 20)
                print(f"Moved cursor to ({current_x}, {current_y + 20}).")


                return
            else:
                print("Element not found on the screen.")

        except:
            pass

def get_formatted_timestamp():
    current_timestamp = int(time.time())
    formatted_timestamp = str(current_timestamp)

    return formatted_timestamp

async def send_websocket_message(message=""):
    while True:

        if message == "":
            message = {
                        "message": ""
                    }

        uri = "ws://127.0.0.1:{0}/webui-socket/{1}".format(port, guid)

        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(message))
            #print(f"Sent message: {message}")
            print(f"Sent message")

            response = await websocket.recv()
            print(f"Received response: {response}")
            #print(f"Received response")

            json_payload = json.loads(response)
        
            try:
                process_leaderboard_data(json_data=json_payload, 
                                                    dataframe_path="./wc31v1S3Database")
                print("Element inserted")

            except Exception as e:
                print("Wrong Response type")
                print(e)
                traceback.print_exc()
                pass

async def button_clicker():
    while True:
        click_element_on_screen("./ressources/next.png", confidence_threshold=0.8)
        print("Button clicked!")
        await asyncio.sleep(5)

async def main():
    await asyncio.gather(send_websocket_message(), button_clicker())


if __name__ == "__main__":

    send_websocket_message()
    print("test")

    while True:
        asyncio.run(main())

        
            
            
            
            







# Make sure it changes the name when the seasons changes












"""
# Get the list of players in the General chat
def get_general_chat():
    # Construct and send the message
    message = {
        "type": "webui",
        "message": "UpdateLeaderboardHighestRankData",
        "payload": {}  # You may need to provide specific data here
    }

    return send_websocket_message(message)


# Get Leaderboard informations
def get_leaderboard():
    # Construct and send the message
    message = {
        "type": "webui",
        "message": "UpdateLeaderboardData", 
        "payload": [{
                        "message": {
                            "region": "",
                            "gameMode": "1v1",
                            "race": "human",
                            "seasonId": 3,
                            "totalrows": 1,
                            "totalpages": 1,
                            "currentpage": 0,
                            "hasError": False,
                            "errorMessage": "",
                            "rows": [
                                {
                                    "race": "human",
                                    "players": [
                                        {
                                            "toonName": "Mashiro",
                                            "battleTag": "Mashiro#21915",
                                            "avatarId": "p004"
                                        }
                                    ],
                                    "region": "",
                                    "mmr": 3413,
                                    "gameMode": "",
                                    "rank": 9984,
                                    "wins": 7,
                                    "losses": 19,
                                    "draws": 0,
                                    "division": 2
                                }
                            ],
                            "lastAccessTime": 1705522448
                        }
                        
                    }]
    }

    return send_websocket_message(message)


# Get Leaderboard informations
def get_leaderboard():
    # Construct and send the message
    message = {
        "messageType": "UpdateLeaderboardHighestRankData",
        "message": 
            [{
                "currentpage": 0,
                "errorMessage": "",
                "gameMode": "1v1",
                "hasError": False,
                "lastAccessTime": get_formatted_timestamp(),
                "race": "human",
                "region": "",
                "seasonId": 3,
                "totalpages": 414,
                "totalrows": 10350
            }]
    }

    return send_websocket_message(message)
"""

