import os
from timeit import default_timer as timer

# we start counting 0,0 from bottom left corner and increase x to right and y to up

X_DIF = {'R' : 1, 'U' : 0,  'D' : 0, 'L' : -1}
Y_DIF = {'R' : 0, 'U' : 1,  'D' : -1, 'L' : 0}

def sign(x):
    """
    Sign function:
    if x < 0: -1
    if x = 0: 0
    if x >0: 1
    """
    return (x > 0) - (x < 0)

def chebyshev_distance(x1, x2):
    return max([abs(sum(pair)) for pair in zip(x1, [-1 * x for x in x2])])

def manhattan_length(pair):
    return sum([abs(c) for c in pair])

def part1old(lines, verbose=False):
    head = (0,0)
    tail = (0,0)
    tail_positions = set([tail])
    for line in lines:
        direction, amount = line.split()            
        for _ in range(int(amount)):
            prev = head
            head = tuple(map(sum, zip(head, (X_DIF[direction], Y_DIF[direction]))))
            if chebyshev_distance(head, tail) > 1:
                tail = prev
                tail_positions.add(tail)
        if verbose:
            print(f"===== {direction} {amount} =====\nhead: {head}\ntail: {tail}")
    return len(tail_positions)


def simulate_rope(moves, length=10):
    """
    length includes H: H, 1, 2, ..., 9 has length 10
    Head is at position 0 in knots array
    """
    knots = [(0,0) for _ in range(length)]  # all of the knots
    tail_positions = set([knots[-1]])  # set to keep track of visited positions
    for direction, amount in moves:
        for _ in range (amount):
            # moving the head
            knots[0] = tuple(map(sum, zip(knots[0], (X_DIF[direction], Y_DIF[direction]))))  
            # moving the rest of the knots. once 1 not has not moved, all subsequent knots don't move either
            i = 1
            while i < length and chebyshev_distance(knots[i - 1], knots[i]) > 1:
                # knots move at most 1 in the direction of the previous one
                knots[i] = tuple(map(sum, zip(knots[i], 
                                              (sign(knots[i-1][0] - knots[i][0]),
                                               sign(knots[i-1][1] - knots[i][1])))))
                i += 1
            if i == length:
                # only add a new position if the tail has moved. we need a set because we can visit the same spot twice
                tail_positions.add(knots[-1])
    return len(tail_positions)

def get_moves(lines):
    return [(line.split()[0], int(line.split()[1])) for line in lines]

def part1(lines):
    start = timer()
    result = simulate_rope(get_moves(lines), 2)
    end = timer()
    print(end - start)
    return result

def part2(lines):
    start = timer()
    result = simulate_rope(get_moves(lines), 10)
    end = timer()
    print(end - start)
    return result

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-9.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))


if __name__ == "__main__":
    main()