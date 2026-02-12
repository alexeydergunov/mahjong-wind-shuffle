import itertools
import random


class Shuffler:
    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        raise NotImplemented()


class RandomShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        shuffled_ids = list(player_ids)
        random.shuffle(shuffled_ids)
        return shuffled_ids


class TotalLinearPenaltyShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        best_penalty = 10 ** 9
        best_sequences = []
        for shuffled_ids in itertools.permutations(player_ids):
            totals = [1] * 4
            for p_id in shuffled_ids:
                for i in range(4):
                    totals[i] += existing_counts[p_id][i]
            penalty = 0
            for i in range(4):
                for j in range(i + 1, 4):
                    penalty += abs(totals[i] - totals[j])
            if penalty < best_penalty:
                best_penalty = penalty
                best_sequences.clear()
                best_sequences.append(list(shuffled_ids))
            elif penalty == best_penalty:
                best_sequences.append(list(shuffled_ids))
        return random.choice(best_sequences)


class TotalSquaredPenaltyShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        best_penalty = 10 ** 9
        best_sequences = []
        for shuffled_ids in itertools.permutations(player_ids):
            totals = [1] * 4
            for p_id in shuffled_ids:
                for i in range(4):
                    totals[i] += existing_counts[p_id][i]
            penalty = 0
            for i in range(4):
                for j in range(i + 1, 4):
                    penalty += abs(totals[i] - totals[j]) ** 2
            if penalty < best_penalty:
                best_penalty = penalty
                best_sequences.clear()
                best_sequences.append(list(shuffled_ids))
            elif penalty == best_penalty:
                best_sequences.append(list(shuffled_ids))
        return random.choice(best_sequences)


class SeparateLinearPenaltyShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        best_penalty = 10 ** 9
        best_sequences = []
        for shuffled_ids in itertools.permutations(player_ids):
            penalty = 0
            for wind, p_id in enumerate(shuffled_ids):
                counts = list(existing_counts[p_id])
                counts[wind] += 1
                for i in range(4):
                    for j in range(i + 1, 4):
                        penalty += abs(counts[i] - counts[j])
            if penalty < best_penalty:
                best_penalty = penalty
                best_sequences.clear()
                best_sequences.append(list(shuffled_ids))
            elif penalty == best_penalty:
                best_sequences.append(list(shuffled_ids))
        return random.choice(best_sequences)


class SeparateSquarePenaltyShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        best_penalty = 10 ** 9
        best_sequences = []
        for shuffled_ids in itertools.permutations(player_ids):
            penalty = 0
            for wind, p_id in enumerate(shuffled_ids):
                counts = list(existing_counts[p_id])
                counts[wind] += 1
                for i in range(4):
                    for j in range(i + 1, 4):
                        penalty += abs(counts[i] - counts[j]) ** 2
            if penalty < best_penalty:
                best_penalty = penalty
                best_sequences.clear()
                best_sequences.append(list(shuffled_ids))
            elif penalty == best_penalty:
                best_sequences.append(list(shuffled_ids))
        return random.choice(best_sequences)


class LexMinListShuffler(Shuffler):
    def shuffle(self, player_ids: list[int], existing_counts: dict[int, list[int]]) -> list[int]:
        best_penalty = None
        best_sequences = []
        for shuffled_ids in itertools.permutations(player_ids):
            counts = [list(existing_counts[p_id]) for p_id in shuffled_ids]
            for i in range(4):
                counts[i][i] += 1
            a = []
            for i in range(4):
                for j in range(4):
                    a.append(counts[i][j])
            a.sort(reverse=True)
            t = tuple(a)
            if (best_penalty is None) or (t < best_penalty):
                best_penalty = t
                best_sequences.clear()
                best_sequences.append(list(shuffled_ids))
            elif t == best_penalty:
                best_sequences.append(list(shuffled_ids))
        return random.choice(best_sequences)


SHUFFLERS: list[Shuffler] = [
    RandomShuffler(),
    TotalLinearPenaltyShuffler(),
    TotalSquaredPenaltyShuffler(),
    SeparateLinearPenaltyShuffler(),
    SeparateSquarePenaltyShuffler(),
    LexMinListShuffler(),
]
