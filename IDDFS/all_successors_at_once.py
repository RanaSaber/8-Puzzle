import re

class EightPuzzleSolver:
    def __init__(self, initial, goal):
        self.initial = EightPuzzle(initial)
        self.goal = EightPuzzle(goal)
        self.max_depth = 0

    def iterative_deepening(self, state, depth=0):
        """Performs one iteration of iterative deepening at self.depth."""
        if depth == self.max_depth:
            print('(CHECK)')
            if state == self.goal:
                return ['GOAL']
        else:
            successors = []  # List to store all successors at once
            for operator in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                new_state = state.copy().move(operator)  # Use the copy method to generate all successors at once
                if new_state:
                    successors.append((operator, new_state))

            for operator, new_state in successors:
                print('(%d %s)' % (depth + 1, operator))
                path = self.iterative_deepening(new_state, depth + 1)
                if path:
                    return [operator] + path

    def solve(self):
        if self.initial == self.goal:
            return '\n(PATH-TO-GOAL ())\n'
        for i in range(1, 2 ** 15):
            self.max_depth = i
            path = self.iterative_deepening(self.initial)
            if path:
                return '\n(PATH-TO-GOAL (%s))\n' % (' '.join(path[0:-1]))


class EightPuzzle:
    def __init__(self, state):
        self.state = state
        self.a_rpos, self.a_cpos = self.asterisk_pos()
        self.operators = {'UP': self.up, 'DOWN': self.down, 'LEFT': self.left, 'RIGHT': self.right}

    def __eq__(self, other):
        return self.state == other.state

    def asterisk_pos(self):
        for rnum, row in enumerate(self.state):
            for cnum, col in enumerate(row):
                if col == '*':
                    return rnum, cnum

    def is_valid_apos(self, rpos, cpos):
        return rpos < len(self.state) and rpos >= 0 and cpos < len(self.state[0]) and cpos >= 0

    def swap_asterisk(self, rpos2, cpos2):
        new_state = [list(l) for l in self.state]
        tmp = new_state[self.a_rpos][self.a_cpos]
        new_state[self.a_rpos][self.a_cpos] = new_state[rpos2][cpos2]
        new_state[rpos2][cpos2] = tmp
        return new_state

    def copy(self):
        # Create a new instance with the same state
        return EightPuzzle([row[:] for row in self.state])

    def move(self, opstr):
        return self.operators[opstr]()

    def up(self):
        if self.is_valid_apos(self.a_rpos - 1, self.a_cpos):
            return EightPuzzle(self.swap_asterisk(self.a_rpos - 1, self.a_cpos))

    def down(self):
        if self.is_valid_apos(self.a_rpos + 1, self.a_cpos):
            return EightPuzzle(self.swap_asterisk(self.a_rpos + 1, self.a_cpos))

    def left(self):
        if self.is_valid_apos(self.a_rpos, self.a_cpos - 1):
            return EightPuzzle(self.swap_asterisk(self.a_rpos, self.a_cpos - 1))

    def right(self):
        if self.is_valid_apos(self.a_rpos, self.a_cpos + 1):
            return EightPuzzle(self.swap_asterisk(self.a_rpos, self.a_cpos + 1))


def parse_ep_input_line(line):
    inner_lists_re = re.compile(r"\((.*)\)")
    first_inner_re = re.compile(r"^\s*\((.*?)\)")
    inner = inner_lists_re.findall(line)
    if inner and len(inner) > 0:
        inner = inner[0]
    else:
        return []
    eplist = []
    firstinner = first_inner_re.findall(inner)
    while firstinner:
        eplist.append(firstinner[0].split())
        inner = first_inner_re.sub('', inner)
        firstinner = first_inner_re.findall(inner)
    return eplist


def main():
    initial = []
    goal = []
    f = open('in')
    for linenum, line in enumerate(f):
        if linenum == 1:
            initial = parse_ep_input_line(line)
        if linenum == 2:
            goal = parse_ep_input_line(line)
    f.close()

    solver = EightPuzzleSolver(initial, goal)
    print(solver.solve())


if __name__ == "__main__":
    main()