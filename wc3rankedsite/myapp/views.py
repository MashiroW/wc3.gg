# Create your views here.

from django.shortcuts import render
from .models import Book
from .models import Entry
from .models import GameSetting
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
    races = GameSetting.objects.values_list('race', flat=True).distinct()

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