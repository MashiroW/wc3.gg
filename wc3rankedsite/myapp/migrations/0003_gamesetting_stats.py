# Generated by Django 5.0.1 on 2024-02-04 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_entry_player_remove_player_toonname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesetting',
            name='stats',
            field=models.JSONField(default=dict),
        ),
    ]