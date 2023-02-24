from __future__ import annotations

import logging
import sys
from copy import copy
from enum import Enum
from pprint import pformat


def load_level(filename: str) -> State:
    logger.info(f"Opening level {filename}")
    stones: dict[Stone, Destination] = {}
    stone_positions: dict[Stone, Position] = {}
    destination_positions: dict[Destination, Position] = {}
    level: list[list[str]] = []

    with open(filename) as file:
        for pair in file.readline().split():
            stones[pair[0]] = pair[1]

        for row_index, line in enumerate(file.readlines()):
            for column_index, character in enumerate(line):
                if character in stones.keys():
                    stone_positions[character] = (row_index, column_index)
                elif character in stones.values():
                    destination_positions[character] = (row_index, column_index)

            level.append([character if character not in stones.keys() | destination_positions.keys() else " " for character in line])

    return State(stones, stone_positions, destination_positions, level, [])


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __repr__(self):
        return self.name


class State:
    stones: dict[Stone, Destination]
    stone_positions: dict[Stone, Position]
    destination_positions: dict[Destination, Position]

    level: list[list[str]]
    moves_played: list[tuple[Stone, Direction]]

    def __init__(self,
                 stones: dict[Stone, Destination],
                 stone_positions: dict[Stone, Position],
                 destination_positions: dict[Destination, Position],
                 level: list[list[str]],
                 moves_played: list[tuple[Stone, Direction]]
                 ):
        self.stones = stones
        self.stone_positions = stone_positions
        self.destination_positions = destination_positions
        self.level = level
        self.moves_played = moves_played

    def __copy__(self):
        return type(self)(
            self.stones,
            copy(self.stone_positions),
            copy(self.destination_positions),
            self.level,
            self.moves_played[:]
        )

    def __hash__(self):
        return hash(frozenset(self.stone_positions.items()))

    def is_finished(self):
        for stone, destination in self.stones.items():
            if self.stone_positions[stone] != self.destination_positions[destination]:
                return False

        return True

    def find_new_states(self):
        new_states: list[State] = []

        for stone, position in self.stone_positions.items():
            for direction in Direction:
                final_position: Position = position
                distance = 0

                while True:
                    new_position = (
                        position[0] + direction.value[0] * (distance + 1),
                        position[1] + direction.value[1] * (distance + 1),
                    )

                    tile = self.level[new_position[0]][new_position[1]]

                    if tile == "X" or new_position in self.stone_positions.values():
                        if distance > 0:
                            new_state = copy(self)
                            new_state.stone_positions[stone] = final_position
                            new_state.moves_played.append((stone, direction))
                            new_states.append(new_state)

                        break

                    final_position = new_position
                    distance += 1

        return new_states


def run(filename) -> State:
    initial_state = load_level(filename)
    boundary: Boundary = [initial_state]
    visited: Visited = {hash(initial_state): initial_state}

    while boundary:
        new_states = []
        new_boundary = []

        for state in boundary:
            new_states += state.find_new_states()

        for state in new_states:
            if state.is_finished():
                return state

            if hash(state) not in visited.keys():
                visited[hash(state)] = state
                new_boundary.append(state)

        boundary = new_boundary
        logger.debug(f"Boundary size is {len(boundary)}, visited space is {len(visited)}")

    raise ValueError("No states left to explore and no solution found")


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    Stone = str
    Destination = str
    Boundary = list[State]
    Visited = dict[int, State]
    Position = tuple[int, int]

    solution = run(sys.argv[1])
    logger.info(pformat(solution.moves_played))
