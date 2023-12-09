#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
import pprint as pp
import multiprocessing as mp
import math

@dataclass
class Node:
    L: str
    R: str

def parse(file):
    path = ''
    map = {}
    with open(file) as fd:
        for line in fd:
            line = line.strip()
            if len(line) == 0:
                continue
            elif '=' in line:
                split = line.split('=')
                name = split[0].strip()
                left_right = split[1].strip().split(',')
                left = left_right[0][1:]
                right = left_right[1][1:-1]
                map[name] = Node(left, right)
            else:
                path = line
    return path, map

def solve_p1(file):
    path, map = parse(file)

    node = 'AAA'
    finished = False
    steps = 0
    while True:
        for p in path:
            if node == 'ZZZ':
                finished = True
                break
            if p == 'R':
                node = map[node].R
            else:
                node = map[node].L
            steps += 1
        if finished:
            break

    print(f'Part 1 - {file}: {steps}')

def solve_p2(file):
    path, map = parse(file)

    tot_steps = []
    for n in map:
        if n[-1] != 'A':
            continue
        node = n
        finished = False
        steps = 0
        while True:
            for p in path:
                if node[-1] == 'Z':
                    finished = True
                    break
                if p == 'R':
                    node = map[node].R
                else:
                    node = map[node].L
                steps += 1
            if finished:
                break

        tot_steps.append(steps)

    print(f'Part 2 - {file}: {math.lcm(*tot_steps)}')

solve_p1('./example.txt')
solve_p1('./example2.txt')
solve_p1('./input.txt')
solve_p2('./example3.txt')
solve_p2('./input.txt')