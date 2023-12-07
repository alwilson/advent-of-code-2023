#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
import pprint as pp
import multiprocessing as mp

@dataclass
class Map:
    map: list
    next_map: str

def parse(file):
    seeds = []
    maps = {}
    with open(file) as fd:
        new_map = []
        map_name = ''
        next_map = ''
        for line in fd:
            line = line.strip()
            split = line.split()
            if len(split) == 0:
                if map_name != '':
                    maps[map_name] = Map(new_map, next_map)
                new_map = []
                map_name = ''
                next_map = ''
            elif split[0] == 'seeds:':
                seeds = [int(i) for i in split[1:]]
            elif split[1] == 'map:':
                name_split = split[0].split('-')
                map_name = name_split[0]
                next_map = name_split[2]
            else:
                new_map.append([int(i) for i in split])
    return seeds, maps

def find_min(seed_start, seed_width, maps, return_dict):
    print(f'{seed_start=} {seed_width=} Started...')
    min_location = 10000000000000000000
    for s in range(seed_start, seed_start+seed_width):
        cur_map = 'seed'
        while cur_map != 'location':
            for m in maps[cur_map].map:
                if s >= m[1] and s < m[1] + m[2]:
                    s += (m[0]-m[1])
                    break
            cur_map = maps[cur_map].next_map

        min_location = min(s, min_location)
    print(f'{seed_start=} {seed_width=} {min_location=} Finished!')
    return_dict[str(seed_start)+'-'+str(seed_width)] = min_location
    print(f'{seed_start=} {seed_width=} {return_dict.values()=}')

def solve(file):
    seeds, maps = parse(file)

    locations = []
    for s in seeds:
        cur_map = 'seed'
        while cur_map != 'location':
            for m in maps[cur_map].map:
                if s >= m[1] and s < m[1] + m[2]:
                    s += (m[0]-m[1])
                    break
            cur_map = maps[cur_map].next_map

        locations.append(s)

    print(f'Part 1 - {file}: {min(locations)}')

    seed_starts = seeds[::2]
    seed_widths = seeds[1::2]
    locations = []
    procs = []
    manager = mp.Manager()
    # Special dictionary for min location return value
    return_dict = manager.dict()
    seed_width_max = 10_000_000
    for seed_start, seed_width in zip(seed_starts, seed_widths):
        # Breakdown processes into smaller chunks to make use of more threads
        while seed_width > seed_width_max:
            proc = mp.Process(target=find_min, args=(seed_start, seed_width_max, maps, return_dict))
            procs.append(proc)
            # TODO Could use a pool or queue instead of spawning ~200 processes
            proc.start()
            seed_start += seed_width_max
            seed_width -= seed_width_max
        if seed_width >= 0:
            proc = mp.Process(target=find_min, args=(seed_start, seed_width, maps, return_dict))
            procs.append(proc)
            proc.start()

    for proc in procs:
        proc.join()

    min_loc = min(return_dict.values())
    print(f'Part 2 - {file}: {min_loc}')

solve('./example.txt')
solve('./input.txt')
