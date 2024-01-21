
import time
import pyautogui
import pygetwindow as gw
import os
from pathlib import Path

from old_files.dataframe_saver import process_leaderboard_data

def collect_image_paths(root_folder):
    image_paths = {}

    root_path = Path(root_folder)

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                file_path = Path(foldername) / filename
                relative_path = str(file_path.relative_to(root_path.parent)).replace(os.path.sep, '_').replace('.', '_')
                key = relative_path.split('_')[1:-1]  # Remove the root folder name
                image_paths['_'.join(key)] = str(file_path)

    return image_paths

def check_element_in_warcraft_window(element_image_path, confidence_threshold=0.8):
    # Find the Warcraft III window
    warcraft_window = gw.getWindowsWithTitle("Warcraft III")
    
    if not warcraft_window:
        print("Warcraft III window not found.")
        return
    
    warcraft_window = warcraft_window[0]

    # Locate the element within the Warcraft III window
    try:
        element_location = pyautogui.locateOnScreen(
            element_image_path,
            confidence=confidence_threshold,
            region=(
                warcraft_window.left, 
                warcraft_window.top, 
                warcraft_window.width, 
                warcraft_window.height
            )
        )

        if element_location:
            return True

    except Exception as e:
        return False
    
def click_element_in_warcraft_window(element_image_path, confidence_threshold=0.8, sleeping_time=1):
    #print("Searching for {}".format(element_image_path))
    
    # Find the Warcraft III window
    warcraft_window = gw.getWindowsWithTitle("Warcraft III")
    
    if not warcraft_window:
        print("Warcraft III window not found.")
        return False
    
    warcraft_window = warcraft_window[0]

    # Locate the element within the Warcraft III window
    try:
        element_location = pyautogui.locateOnScreen(
            element_image_path,
            confidence=confidence_threshold,
            region=(
                warcraft_window.left, 
                warcraft_window.top, 
                warcraft_window.width, 
                warcraft_window.height
            )
        )

        if element_location:
            # Calculate the middle of the element
            middle_x = element_location.left + element_location.width / 2
            middle_y = element_location.top + element_location.height / 2

            # Click the middle of the element
            pyautogui.click(middle_x, middle_y)
            print("Clicked {}".format(element_image_path))

            # Move the cursor to (0, 0) relative to the Warcraft III window
            pyautogui.moveTo(
                warcraft_window.left,
                warcraft_window.top + 20
            )
            #print(f"Moved cursor to ({warcraft_window.left}, {warcraft_window.top + 20}).")
            time.sleep(sleeping_time)
            return True
        
        else:
            print("Element not found in the Warcraft III window.")
            return False

    except Exception as e:
        #print(f"Error: {e}")
        return False

def set_race(TargetRace, sleeping_time=1): # - You can't set a race when a confrontation mode is active

    timeout_seconds = 10
    races = ["all", "random", "human", "nightelf", "orc", "undead"]

    def get_current_race():
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            for race in races:
                current_race_img_path = ressources_paths["race_selected_{0}".format(race)]
                if check_element_in_warcraft_window(current_race_img_path):
                    return race
                
        return None
    
    def set_current_race(CurrentRace, TargetRace):

        current_race_img_path = ressources_paths["race_selected_{0}".format(CurrentRace)]
        target_race_img_path = ressources_paths["race_droplist_{0}".format(TargetRace)]

        # Open list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=current_race_img_path, sleeping_time=sleeping_time) == True:
                break

        # Select in list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=target_race_img_path, sleeping_time=sleeping_time) == True:
                return True

        return False                    
    
    #print("Selecting Race: {0}".format(TargetRace))
    
    try:
        CurrentRace = get_current_race()
        if set_current_race(CurrentRace=CurrentRace, TargetRace=TargetRace) == True:
            #time.sleep(1)
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def set_gamemode(TargetGamemode, sleeping_time=1):

    timeout_seconds = 10
    gamemodes = ["confrontation_2v2", "confrontation_3v3", "confrontation_4v4", "1v1", "2v2", "3v3", "4v4", "cps"]
        
    def get_current_gamemode():
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            for gamemode in gamemodes:
                current_race_img_path = ressources_paths["gamemode_selected_{0}".format(gamemode)]
                if check_element_in_warcraft_window(current_race_img_path, confidence_threshold=0.99):
                    return gamemode
                
        return None
    
    def set_current_gamemode(CurrentGamemode, TargetGamemode):
        current_gamemode_img_path = ressources_paths["gamemode_selected_{0}".format(CurrentGamemode)]
        target_gamemode_img_path = ressources_paths["gamemode_droplist_{0}".format(TargetGamemode)]

        # Open list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=current_gamemode_img_path, confidence_threshold=0.99, sleeping_time=sleeping_time) == True:
                break

        # Select in list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=target_gamemode_img_path, confidence_threshold=0.99, sleeping_time=sleeping_time) == True:
                return True

        return False  

    #print("Selecting Gamemode: {0}".format(TargetGamemode))
    
    try:
        CurrentGamemode = get_current_gamemode()
        #print(CurrentGamemode)
        if set_current_gamemode(CurrentGamemode=CurrentGamemode, TargetGamemode=TargetGamemode) == True:
            #time.sleep(1)
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def set_season(TargetSeason, sleeping_time=1):

    timeout_seconds = 10
    seasons = ["current", "previous"]
        
    def get_current_season():
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            for season in seasons:
                current_race_img_path = ressources_paths["season_selected_{0}".format(season)]
                if check_element_in_warcraft_window(current_race_img_path, confidence_threshold=0.99):
                    return season
                
        return None
    
    def set_current_season(CurrentSeason, TargetSeason):
        current_season_img_path = ressources_paths["season_selected_{0}".format(CurrentSeason)]
        target_season_img_path = ressources_paths["season_droplist_{0}".format(TargetSeason)]

        # Open list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=current_season_img_path, confidence_threshold=0.99, sleeping_time=sleeping_time) == True:
                break

        # Select in list
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if click_element_in_warcraft_window(element_image_path=target_season_img_path, confidence_threshold=0.99, sleeping_time=sleeping_time) == True:
                return True

        return False  

    #print("Selecting Season: {0}".format(TargetSeason))
    
    try:
        CurrentSeason = get_current_season()
        print(CurrentSeason)
        if set_current_season(CurrentSeason=CurrentSeason, TargetSeason=TargetSeason) == True:
            #time.sleep(1)
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def startup_sequence():

    sequence = [ressources_paths["multiplayer"],
                ressources_paths["ladderboard"]]

    return sequence

def sequence_player(sequence): # Plays a sequence of images to click in an array. If some element isn't found it will try the previous action.
    timeout_seconds = 10
    idx = 0

    while idx < len(sequence):

        is_found = False
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            is_found = click_element_in_warcraft_window(element_image_path=sequence[idx], sleeping_time=2)
            if is_found:
                break

        # In case the element has not been found for timeout_seconds duration, try again with the previous one
        if not is_found and idx != 0 and len(sequence) != 1:
            print("Trying the previous element of the sequence")
            idx -= 1
        else:
            idx += 1

def press_next_till_end(sleeping_time=0):
    timeout_seconds = 5

    while check_element_in_warcraft_window(element_image_path=ressources_paths["right_end"], confidence_threshold=0.99) != True:
        click_element_in_warcraft_window(element_image_path=ressources_paths["next"], confidence_threshold=0.8, sleeping_time=sleeping_time)

        start_time = time.time()
        while time.time() - start_time < timeout_seconds and check_element_in_warcraft_window(element_image_path=ressources_paths["not_ready_for_click_checker"], confidence_threshold=0.8) == False:
            pass
        
        while check_element_in_warcraft_window(element_image_path=ressources_paths["not_ready_for_click_checker"], confidence_threshold=0.8) == True:
            pass

def leaderboard_parser():

    for season in ["previous"]:
        for gamemode in ["confrontation_2v2", "confrontation_3v3", "confrontation_4v4"]:

            print("Settings - Season: {0} - Race {1} - Gamemode {2}".format(season, "N/A", gamemode))

            set_season(TargetSeason=season, sleeping_time=0.5)
            set_gamemode(TargetGamemode=gamemode, sleeping_time=0.5)

            # Faire le next
            press_next_till_end()

    for season in ["previous"]:
        for gamemode in ["1v1", "2v2", "3v3", "4v4", "cps"]: # Possibilities: ["1v1", "2v2", "3v3", "4v4", "cps"]
            for race in ["all", "random"]: # Possibilities: ["all", "random", "human", "nightelf", "orc", "undead"]

                print("Settings - Season: {0} - Race {1} - Gamemode {2}".format(season, race, gamemode))

                set_season(TargetSeason=season, sleeping_time=0.5)
                set_gamemode(TargetGamemode=gamemode, sleeping_time=0.5)
                set_race(TargetRace=race, sleeping_time=0.5)

                # Faire le next
                press_next_till_end()
    
    click_element_in_warcraft_window(ressources_paths["back"], confidence_threshold=0.8, sleeping_time=1)



if __name__ == "__main__":

    ressources_paths = collect_image_paths("./ressources/")

    sequence_player(sequence=startup_sequence())
    leaderboard_parser()