#!/usr/bin/env python3

import copy

def parse(file):
    map = []

    with open(file) as fd:
        for y, line in enumerate(fd):
            line = line.strip()
            for x, char in enumerate(line):
                if char == 'S':
                    # Account for halo of empty space
                    start = (x+1, y+1)
            # Use list of chars rather string for easier manipulation
            map.append(list('.'+line+'.'))

    # Add halo of empty space around the map 
    line_len = len(map[0])
    map = [list('.'*(line_len+2))] + map + [list('.'*(line_len+2))]
    return start, map

def print_map(map):
    for line in map:
        for char in line:
            print(char, end='')
        print()

def solve_p1(file):
    start, map = parse(file)

    dirs_d = {}
    dirs = {'S': (0, 1), 'E': (1, 0), 'N': (0, -1), 'W': (-1, 0)}
    dirs_d['S'] = dirs.values()
    dirs_d['#'] = []
    dirs_d['|'] = [dirs['S'], dirs['N']]
    dirs_d['-'] = [dirs['E'], dirs['W']]
    dirs_d['L'] = [dirs['N'], dirs['E']]
    dirs_d['J'] = [dirs['N'], dirs['W']]
    dirs_d['7'] = [dirs['S'], dirs['W']]
    dirs_d['F'] = [dirs['S'], dirs['E']]

    paths_d = {}
    paths = {'S': '|LJ', 'E': '-J7', 'N': '|7F', 'W': '-LF'}
    paths_d['S'] = paths.values()
    paths_d['#'] = []
    paths_d['|'] = [paths['S'], paths['N']]
    paths_d['-'] = [paths['E'], paths['W']]
    paths_d['L'] = [paths['N'], paths['E']]
    paths_d['J'] = [paths['N'], paths['W']]
    paths_d['7'] = [paths['S'], paths['W']]
    paths_d['F'] = [paths['S'], paths['E']]

    frontier = [start]
    length = -1
    while len(frontier) > 0:
        length += 1

        # Explore all paths one step at a time
        next_frontier = []
        for pos in frontier:
            cur_path = map[pos[1]][pos[0]]
            # Mark visited points to exclude them from frontier
            map[pos[1]][pos[0]] = '#'
            # Check next valid directions and paths
            for p, d in zip(paths_d[cur_path], dirs_d[cur_path]):
                pos_next = (pos[0]+d[0], pos[1]+d[1])
                map_next = map[pos_next[1]][pos_next[0]]
                # Check if the next path actually connects
                if map_next in p:
                    next_frontier.append(pos_next)
        frontier = next_frontier

    print(f'Part 1 - {file}: {length}')

# Mark everything in a line from side as 'I'nside
def mark_line_inside(map, dirs, sides_d, covered, pos, dir):
    if dir != 'A':
        t = sides_d[dir]
        pos_next = pos
        while True:
            pos_next = (pos_next[0]+dirs[t][0], pos_next[1]+dirs[t][1])
            if pos_next not in covered:
                map[pos_next[1]][pos_next[0]] = 'I'
            else:
                break

def explore_line(start, map, dirs_d, dirs, sides_d, paths_d, paths, covered, mark=False):
    frontier = [(start, 'A')]

    # Explore one path one step at a time
    # Optionally mark everything inside the pipe if mark is set
    while len(frontier) > 0:
        next_frontier = []
        for pos_dir in frontier:
            pos = pos_dir[0]
            dir = pos_dir[1]
            cur_path = map[pos[1]][pos[0]]

            covered[pos] = True

            if mark:
                mark_line_inside(map, dirs, sides_d, covered, pos, dir)

            # Mark visited points to exclude them from frontier
            map[pos[1]][pos[0]] = '#'
            # Check next valid directions and paths
            for p, d in zip(paths_d[cur_path], dirs_d[cur_path]):
                pos_next = (pos[0]+dirs[d][0], pos[1]+dirs[d][1])
                map_next = map[pos_next[1]][pos_next[0]]

                # Check if the next path actually connects
                if map_next in paths[p]:
                    next_frontier.append((pos_next, d))

                    if mark:
                        mark_line_inside(map, dirs, sides_d, covered, pos, d)

                    # Intentianally stop frontier from having multiple paths
                    # this makes it easier to track direction and which side
                    # is the inside of the pipe
                    if cur_path == 'S':
                        break
        frontier = next_frontier

def solve_p2(file, flip=False):
    start, map = parse(file)
    map_copy = copy.deepcopy(map)


    dirs_d = {}
    dirs = {'S': (0, 1), 'E': (1, 0), 'N': (0, -1), 'W': (-1, 0)}
    dirs_d['S'] = ['S', 'N', 'E', 'W']
    dirs_d['#'] = []
    dirs_d['|'] = ['S', 'N']
    dirs_d['-'] = ['E', 'W']
    dirs_d['L'] = ['N', 'E']
    dirs_d['J'] = ['N', 'W']
    dirs_d['7'] = ['S', 'W']
    dirs_d['F'] = ['S', 'E']

    # I'm not sure how to know which side of the pipe is the inside,
    # so there are two sides that can be swapped between *shrugs*
    # Ideally could check if out of bounds is reached somehow?
    sides_d = {}
    sides_d['E'] = 'S'
    sides_d['W'] = 'N'
    sides_d['S'] = 'W'
    sides_d['N'] = 'E'

    # Flip sides if needed, and for out of bounds errors :)
    if flip:
        sides_d['E'] = 'N'
        sides_d['W'] = 'S'
        sides_d['S'] = 'E'
        sides_d['N'] = 'W'

    paths_d = {}
    paths = {'S': '|LJ', 'E': '-J7', 'N': '|7F', 'W': '-LF'}
    paths_d['S'] = ['S', 'N', 'E', 'W']
    paths_d['#'] = []
    paths_d['|'] = ['S', 'N']
    paths_d['-'] = ['E', 'W']
    paths_d['L'] = ['N', 'E']
    paths_d['J'] = ['N', 'W']
    paths_d['7'] = ['S', 'W']
    paths_d['F'] = ['S', 'E']

    # First pass to mark the pipe in the covered dict
    covered = {}
    explore_line(start, map, dirs_d, dirs, sides_d, paths_d, paths, covered, False)

    # Second pass to mark everything inside the pipe
    map = map_copy
    explore_line(start, map, dirs_d, dirs, sides_d, paths_d, paths, covered, True)

    i_count = sum([line.count('I') for line in map])
    print(f'Part 2 - {file}: {i_count}')

solve_p1('./example.txt')
solve_p1('./example2.txt')
solve_p1('./input.txt')

solve_p2('./example3.txt')
solve_p2('./example4.txt', True)
solve_p2('./input.txt')
