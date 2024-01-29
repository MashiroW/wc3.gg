# Create your views here.

from django.shortcuts import render
from .models import Book
from .models import Entry
from .models import GameSetting
from django.utils import timezone
from django.http import JsonResponse

def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books': books})

def home(request):
    return render(request, 'myapp/home.html')

def leaderboards(request):
    # Retrieve unique values for Season, Gamemode, and Race
    seasons = GameSetting.objects.values_list('season', flat=True).distinct()
    gamemodes = GameSetting.objects.values_list('gamemode', flat=True).distinct()
    races = ["All", "Human", "Orc", "Night Elf", "Undead", "Random"]

    context = {
        'seasons': seasons,
        'gamemodes': gamemodes,
        'races': races,
    }

    return render(request, 'myapp/leaderboards.html', context)

def contact(request):
    return render(request, 'myapp/contact.html')

def about(request):
    return render(request, 'myapp/about.html')

def get_filtered_leaderboard(request):
    season = request.GET.get('season')
    gamemode = request.GET.get('gamemode')
    race = request.GET.get('race')
    
    # Extract the range from the URL, default to 0-100
    range_param = request.GET.get('range', '0-100')
    start, end = map(int, range_param.split('-'))

    if race != 'all':
        # Perform filtering based on the selected criteria and range
        filtered_entries = Entry.objects.filter(
            game_setting__season=season,
            game_setting__gamemode=gamemode
        )

        filtered_entries = [entry for entry in filtered_entries if entry.race == race][start:end]

    else:
        # Perform filtering based on the selected criteria and range
        filtered_entries = Entry.objects.filter(
            game_setting__season=season,
            game_setting__gamemode=gamemode,
            game_setting__race=race
        )[start:end]        

    # Serialize the filtered data
    serialized_data = [
        {
            'rank': entry.rank,
            'division': entry.division,
            'avatarId': entry.avatarId,
            'player_battle_tags': entry.player_battle_tags,
            'mmr': entry.mmr,
            'race': entry.race,
            'wins': entry.wins,
            'losses': entry.losses,
            'draws': entry.draws,
            # Add more fields as needed
        }
        for entry in filtered_entries
    ]

    return JsonResponse(serialized_data, safe=False)

def get_total_count(request):
    season = request.GET.get('season')
    gamemode = request.GET.get('gamemode')
    race = request.GET.get('race')

    # Add any additional filters you need

    if race != "all":
        # Perform filtering based on the selected criteria and range
        filtered_entries = Entry.objects.filter(
            game_setting__season=season,
            game_setting__gamemode=gamemode
        )

        total_count = len([entry for entry in filtered_entries if entry.race == race])

    else:
        # Perform filtering based on the selected criteria and range
        total_count = Entry.objects.filter(
            game_setting__season=season,
            game_setting__gamemode=gamemode,
            game_setting__race=race
        ).count()

    # Fetch dataset datetime
    dataset_datetime = GameSetting.objects.filter(season=season, gamemode=gamemode).latest('created_at').created_at
    dataset_datetime_str = timezone.localtime(dataset_datetime).strftime('%Y-%m-%d %H:%M:%S')

    # Include dataset datetime in the response
    response_data = {
        'total_count': total_count,
        'dataset_datetime': dataset_datetime_str,
    }

    return JsonResponse(response_data)