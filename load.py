import dataclasses
import datetime
import json
import os.path
from typing import Any, Self


@dataclasses.dataclass
class Player:
    name: str
    old_ids: list[int] | None
    new_ids: list[int] | None

    @property
    def id(self) -> int:
        if self.old_ids is not None:
            return self.old_ids[-1]
        elif self.new_ids is not None:
            return self.new_ids[-1]
        else:
            raise ValueError("Player must have at least one id")

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Self:
        return Player(
            name=d["name"],
            old_ids=d.get("old_ids"),
            new_ids=d.get("new_ids"),
        )


@dataclasses.dataclass
class Game:
    pantheon_type: str
    event_id: int
    session_id: int
    session_date: datetime.datetime
    players: list[Player]
    places: list[int]
    scores: list[float]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Self:
        return Game(
            pantheon_type=d["pantheon_type"],
            event_id=d["event_id"],
            session_id=d["session_id"],
            session_date=datetime.datetime.fromisoformat(d["session_date"]),
            players=[Player.from_json(x) for x in d["players"]],
            places=d["places"],
            scores=d["scores"],
        )


def read_games(filename: str) -> list[Game]:
    if not os.path.exists(filename):
        raise Exception(f"File {filename} doesn't exist")
    games: list[Game] = []
    with open(filename) as f:
        for line in f:
            game = Game.from_json(json.loads(line))
            games.append(game)
    return games
