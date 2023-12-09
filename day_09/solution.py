#!/usr/bin/env python3

def parse(file):
    seqs = []
    with open(file) as fd:
        for line in fd:
            line = line.strip()
            seq = [int(x) for x in line.split()]
            seqs.append(seq)
    return seqs

def solve_p1(file):
    seqs = parse(file)

    tot_sum = 0
    for seq in seqs:
        lasts = [seq[-1]]
        while not all([s == 0 for s in seq]):
            seq = [i - j for i, j in zip(seq[1:], seq[:-1])]
            lasts.append(seq[-1])
        tot_sum += sum(lasts)

    print(f'Part 1 - {file}: {tot_sum}')

def solve_p2(file):
    seqs = parse(file)

    tot_sum = 0
    for seq in seqs:
        seq = seq[::-1]
        lasts = [seq[-1]]
        while not all([s == 0 for s in seq]):
            seq = [i - j for i, j in zip(seq[1:], seq[:-1])]
            lasts.append(seq[-1])
        tot_sum += sum(lasts)

    print(f'Part 2 - {file}: {tot_sum}')

solve_p1('./example.txt')
solve_p1('./input.txt')
solve_p2('./example.txt')
solve_p2('./input.txt')
