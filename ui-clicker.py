
import time
import pyautogui
import pygetwindow as gw
import psutil
import subprocess
import os
import signal
from pathlib import Path

from debug_tools import *
from dataframe_manager import *

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
        #print("Warcraft III window not found.")
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

    def execute_command(exe_path, args):
        try:
            subprocess.Popen([exe_path] + args, shell=True)
            print(f"Executable '{exe_path}' started successfully.")
        except Exception as e:
            print(f"Error starting '{exe_path}': {e}")

    def get_pid(process_name):
        pid = None

        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                pid = process.info['pid']
                return pid

    def kill_process_by_pid(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Process with PID {pid} terminated successfully.")
        except ProcessLookupError:
            print(f"No process found with PID {pid}.")
        except Exception as e:
            print(f"Error terminating process with PID {pid}: {e}")
    
    def execute_game():       
        process_name = "Warcraft III.exe"
        exe_path = r'H:\Program Files (x86)\Battle.net\Battle.net.exe'
        command_args = ['--exec=launch W3']

        if get_pid(process_name=process_name) == None:
            execute_command(exe_path, command_args)
        else:
            kill_process_by_pid(pid=get_pid(process_name=process_name))
            execute_command(exe_path, command_args)
        
        print("Waiting for War3 PID...")
        while get_pid(process_name=process_name) == None:
            pass
        
        print("Waiting for Main Menu...")
        while check_element_in_warcraft_window(ressources_paths["multiplayer"], confidence_threshold=0.8) != True:
            pass

        time.sleep(2) 
        print("Startup over")

    execute_game()

    global packets_sniffer
    packets_sniffer = subprocess.Popen("python ./packets_sniffer.py", shell=True)
    
    sequence = [ressources_paths["multiplayer"],
                ressources_paths["ladderboard"]]
    
    sequence_player(sequence=sequence)

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

def click_arrow(arrow_name, timeout_seconds=5, sleeping_time=0): # "next" or "previous"
    
    click_element_in_warcraft_window(element_image_path=ressources_paths[arrow_name], confidence_threshold=0.8, sleeping_time=sleeping_time)

    start_time = time.time()
    while time.time() - start_time < timeout_seconds and check_element_in_warcraft_window(element_image_path=ressources_paths["not_ready_for_click_checker"], confidence_threshold=0.8) == False:
        pass

    if arrow_name == "previous":
        sequence_player([ressources_paths["refresh"]])
    
    while check_element_in_warcraft_window(element_image_path=ressources_paths["not_ready_for_click_checker"], confidence_threshold=0.8) == True:
        pass

def press_next_till_end(race, gamemode):

    save_path = "./databases/wc3_S{0}_{1}_{2}.csv".format(3, gamemode, race)

    while check_element_in_warcraft_window(element_image_path=ressources_paths["right_end"], confidence_threshold=0.99) != True:
        click_arrow("next")

        """
        try:
            limit = 5
            while check_duplicate_rows(save_path) == True:
                click_arrow("previous")

                limit -= 1
                if limit == 0:
                    break

            while check_discontinuous_ranks(save_path) == True:
                movement = determine_movement(df_path=save_path)
                #print("Decision is {0}".format(movement))
                click_arrow(movement)
        except Exception as e:
            # In case where the csv file doesn't exist yet.
            print("no file yet")
            print(e)
            pass
        """

def leaderboard_parser():

    global packets_sniffer
    startup_sequence()

    
    for season in ["previous"]:
        for gamemode in ["1v1", "2v2", "3v3", "4v4", "cps"]: # Possibilities: ["1v1", "2v2", "3v3", "4v4", "cps"]
            for race in ["all"]: # Possibilities: ["all", "random", "human", "night_elf", "orc", "undead"]

                print("Settings - Season: {0} - Race {1} - Gamemode {2}".format(season, race, gamemode))

                set_season(TargetSeason=season, sleeping_time=0.5)
                set_gamemode(TargetGamemode=gamemode, sleeping_time=0.5)
                set_race(TargetRace=race, sleeping_time=0.5)

                # Go through every page
                press_next_till_end(race=race, gamemode=gamemode)

                # Kill process
                packets_sniffer.terminate()

                # Reboot for fluidity
                startup_sequence()

    """
    for season in ["previous"]:
        for gamemode in ["confrontation_2v2", "confrontation_3v3", "confrontation_4v4"]:

            print("Settings - Season: {0} - Race {1} - Gamemode {2}".format(season, "N/A", gamemode))

            set_season(TargetSeason=season, sleeping_time=0.5)
            set_gamemode(TargetGamemode=gamemode, sleeping_time=0.5)

            # Go through every page
            press_next_till_end(race="NaN", gamemode=gamemode)

            # Reboot for fluidity
            startup_sequence()
    """

    click_element_in_warcraft_window(ressources_paths["back"], confidence_threshold=0.8, sleeping_time=1)

if __name__ == "__main__":

    global packets_sniffer

    ressources_paths = collect_image_paths("./ressources/")
    leaderboard_parser()