#!/usr/bin/env python3

import copy
import pprint as pp

def print_image(map):
    for line in map:
        print(''.join(line))

def old_parse(file):
    image = []
    with open(file) as fd:
        for line in fd:
            image.append(list(line.strip()))
            # Add in row expansion
            if '#' not in line:
                image.append(list(line.strip()))

    # Add in column expansion
    new_image = copy.deepcopy(image)
    inserts = 0
    for x in range(len(image[0])):
        found = False
        for y in range(len(image)):
            if image[y][x] == '#':
                found = True
                break
        if not found:
            for y in range(len(image)):
                new_image[y].insert(x+inserts, '.')
            inserts += 1
    image = new_image

    # Convert to coordinate dict
    map = {}
    for y in range(len(image)):
        for x in range(len(image[0])):
            if image[y][x] == '#':
                map[(x, y)] = True

    return  map

def parse_p2(file, size=1):
    image = []
    with open(file) as fd:
        for line in fd:
            image.append(list(line.strip()))

    # Create coordinate dict with new expandaed coordinates as value
    map = {}
    for y in range(len(image)):
        for x in range(len(image[0])):
            if image[y][x] == '#':
                map[(x, y)] = (x, y)

    # Insert row expansion
    inserts = 0
    for x in range(len(image[0])):
        found = False
        for y in range(len(image)):
            if image[y][x] == '#':
                found = True
                break
        if not found:
            for k in map:
                if map[k][0] > x+inserts:
                    map[k] = (map[k][0]+size, map[k][1])
            inserts += size

    # Insert column expansion
    inserts = 0
    for y in range(len(image)):
        found = False
        for x in range(len(image[0])):
            if image[y][x] == '#':
                found = True
                break
        if not found:
            for k in map:
                if map[k][1] > y+inserts:
                    map[k] = (map[k][0], map[k][1]+size)
            inserts += size

    # Convert expanded coordinates into new coordinate map
    new_map = {}
    for v in map.values():
        new_map[v] = True

    return  new_map

def solve(file, size=1):
    map = parse_p2(file, size)

    galaxies = list(map.keys())
    tot_dist = 0
    for gx, g in enumerate(galaxies):
        for gp in galaxies[gx+1:]:
            distance = abs(g[0] - gp[0]) + abs(g[1] - gp[1])
            tot_dist += distance

    print(f'Part {("1" if size == 1 else "2")} - {file}: {tot_dist}')

solve('./example.txt')
solve('./input.txt')
solve('./example.txt', 10-1)
solve('./example.txt', 100-1)
solve('./input.txt', 1_000_000-1)
