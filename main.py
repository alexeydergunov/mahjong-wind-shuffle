import random
import time
from collections import defaultdict

import analysis
import load
from load import Game


def main():
    random.seed(time.time())
    old_games = load.read_games(filename="../mahjong-skill-private-files/shared/pantheon_old_games.txt")
    new_games = load.read_games(filename="../mahjong-skill-private-files/shared/pantheon_new_games__2024_12_02.txt")
    print(f"Read {len(old_games)} old games and {len(new_games)} new games")

    grouped_by_tournament: dict[tuple[str, int], list[Game]] = defaultdict(list)
    for game in old_games + new_games:
        key = (game.pantheon_type, game.event_id)
        grouped_by_tournament[key].append(game)
    print(f"Games grouped by {len(grouped_by_tournament)} tournaments")

    for key, tournament_games in grouped_by_tournament.items():
        game_counts: dict[int, int] = defaultdict(int)
        for game in tournament_games:
            for player in game.players:
                game_counts[player.id] += 1
        players_count = len(game_counts)
        table_count = players_count / 4.0
        round_count = len(tournament_games) / table_count
        if players_count >= 32 and round_count >= 8:
            print()
            print(f"Processing tournament {key}: {players_count} players, {round_count} rounds")
            analysis.analyze_tournament(games=tournament_games)


if __name__ == "__main__":
    main()
