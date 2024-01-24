import os
import csv
import ast
from django.core.management.base import BaseCommand
from myapp.models import Entry, GameSetting, Player
from datetime import datetime

class Command(BaseCommand):
    help = 'Load players from CSV file'

    def handle(self, *args, **options):
        csv_file_path = './wc3_S3_1v1_all.csv'
        #csv_file_path = "wc3_S3_2v2arranged_N-A.csv"

        # Extract season, gamemode, and race from the file name
        _, filename = os.path.split(csv_file_path)
        parts = filename.split('_')
        season_str = parts[1][1:]
        season = int(season_str)

        gamemode = parts[2]
        race = parts[3][:-4]

        # Create a new GameSetting instance with the current datetime
        current_datetime = datetime.now()
        game_setting = GameSetting.objects.create(
            season=season,
            gamemode=gamemode,
            race=race,
            created_at=current_datetime
        )

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert string representations of lists to actual lists using ast.literal_eval
                battleTag_list = ast.literal_eval(row['battleTag'])
                avatarId_list = ast.literal_eval(row['avatarId'])

                # Assuming the battleTag, toonname, and avatarId lists have the same length
                players = []

                for i in range(len(battleTag_list)):
                    try:
                        # Get or create the Player
                        player, created = Player.objects.get_or_create(
                            battleTag=battleTag_list[i]
                        )

                        # If the player exists, update last_avatarId
                        player.last_avatarId = avatarId_list[i]
                        player.save()

                    except Player.DoesNotExist:
                        # If the player does not exist, create a new one
                        player = Player.objects.create(
                            battleTag=battleTag_list[i],
                            last_avatarId=avatarId_list[i]
                        )                      

                    # Append the player and avatarId to their respective lists
                    players.append(player)

                row.pop('toonname', None)
                row.pop('battleTag', None)

                entry = Entry.objects.create(
                    game_setting=game_setting,
                    **row  # Include other fields from the row
                )
                
                entry.players.set(players)