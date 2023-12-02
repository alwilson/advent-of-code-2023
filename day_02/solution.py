#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod

@dataclass
class Game:
    id: int
    plays: list

def parse(file):
    games = []
    with open(file) as fd:
        for line in fd:
            line = line.strip()
            split = line.split(':')
            game = split[0]
            game_id = int(game.split(' ')[-1])

            plays_l = split[-1].split(';')
            plays = []
            for play in plays_l:
                hand = []
                for cube in play.split(','):
                    cube = cube.strip()
                    cube_split = cube.split(' ')
                    hand.append((int(cube_split[0]), cube_split[1]))
                plays.append(hand)
            game_i = Game(game_id, plays)
            games.append(game_i)
    return games

def solve(file):
    games = parse(file)

    good_games = []
    game_powers = []
    for game in games:
        cube_tots = {'red': 0, 'green': 0, 'blue': 0}
        for play in game.plays:
            for cube in play:
                cube_tots[cube[1]] = max(cube_tots[cube[1]], cube[0])

        if cube_tots['red'] <= 12 and cube_tots['green'] <= 13 and cube_tots['blue'] <= 14:
            good_games.append(game.id)

        game_powers.append(prod(cube_tots.values()))

    print(f'Part 1 - {file}: {sum(good_games)}')
    print(f'Part 2 - {file}: {sum(game_powers)}')

solve('./example.txt')
solve('./input.txt')
