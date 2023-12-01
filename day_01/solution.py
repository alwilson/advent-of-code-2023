#!/usr/bin/env python3

def parse(file):
    nums = []
    with open(file) as fd:
        for line in fd:
            line = [int(x) for x in line.strip() if x.isnumeric()]
            nums.append(line)
    return nums

def parse_with_names(file):
    nums = []
    with open(file) as fd:
        for line in fd:
            pairs = [('one', '1'),
                     ('two', '2'),
                     ('three', '3'),
                     ('four', '4'),
                     ('five', '5'),
                     ('six', '6'),
                     ('seven', '7'),
                     ('eight', '8'),
                     ('nine', '9')]
            for name,val in pairs:
                # inject number into strings without breaking adjacent/overlapping numbers
                line = line.replace(name, name[0]+val+name[-1])
            line = [int(x) for x in line.strip() if x.isnumeric()]
            nums.append(line)
    return nums

def solve_p1(file):
    nums = parse(file)
    tot_nums = sum([n[0]*10 + n[-1] for n in nums])
    print(f'Part 1 - {file}: {tot_nums}')

def solve_p2(file):
    nums = parse_with_names(file)
    tot_nums = sum([n[0]*10 + n[-1] for n in nums])
    print(f'Part 2 - {file}: {tot_nums}')

solve_p1('./example.txt')
solve_p1('./input.txt')
solve_p2('./example_2.txt')
solve_p2('./input.txt')
