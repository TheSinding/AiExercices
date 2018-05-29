from math import ceil


def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state, "MAX")
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state, "MIN")
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s))
        return v

    state = min(successors_of(state), key=lambda a: max_value(a))
    return state


def is_terminal(state):
    for bunke in state:
        if bunke > 2:
            return False
    return True


def utility_of(state, player):
    if player in ['MIN', 'MAX']:
        return - 1 if player == 'MIN' else 1
    return 0


def successors_of(state):
    successors = []

    for index, bunke in enumerate(state):
        if bunke > 2:
            bunker = split_bunke(bunke)
            for par in bunker:
                new_state = state[:index] + par + state[index + 1:]
                successors.append(new_state)

    return successors


def split_bunke(bunke):
    out = []
    for i in range(1, int(ceil(bunke / 2))):
        rest = bunke - i
        if rest != bunke:
            out.append([i, rest])
    return out


def run():
    state = [7]
    print(state)
    while not is_terminal(state):
        state = minmax_decision(state)
        print(state)


if __name__ == '__main__':
    run()
