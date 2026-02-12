import math

import shuffle
from load import Game
from shuffle import Shuffler


def calculate_tournament_penalty(existing_counts: dict[int, list[int]]) -> float:
    result = 0.0
    for counts in existing_counts.values():
        round_count = sum(counts)
        ideal = [0] * 4
        for i in range(round_count):
            ideal[i % 4] += 1
        ideal.sort()
        existing = sorted(counts)
        for i in range(4):
            result += abs(ideal[i] - existing[i])
    return result


def analyze_tournament_single(games: list[Game], shuffler: Shuffler) -> float:
    existing_counts: dict[int, list[int]] = {}
    for game in games:
        for player in game.players:
            existing_counts[player.id] = [0] * 4

    for game in games:
        player_ids = [p.id for p in game.players]
        shuffled_players = shuffler.shuffle(player_ids=player_ids, existing_counts=existing_counts)
        for i, player_id in enumerate(shuffled_players):
            existing_counts[player_id][i] += 1

    total_penalty = calculate_tournament_penalty(existing_counts=existing_counts)
    return total_penalty


def analyze_tournament(games: list[Game]):
    iterations_count = 100
    for shuffler in shuffle.SHUFFLERS:
        results: list[float] = []
        for iteration in range(iterations_count):
            penalty = analyze_tournament_single(games=games, shuffler=shuffler)
            results.append(penalty)
        mean = sum(results) / len(results)
        diff_sum = 0.0
        for x in results:
            diff_sum += abs(x - mean)
        stddev = math.sqrt(diff_sum / len(results))
        print(f"Shuffler {shuffler.name()}: "
              f"min: {min(results)}, max: {max(results)}, "
              f"mean {mean:.6f}, stddev {stddev:.6f}")
