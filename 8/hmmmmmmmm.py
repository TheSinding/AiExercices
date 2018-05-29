import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end] Columns: ["initial", "hot", "cold", "final"]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation] Columns: [0, 1, 2, 3]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(
            states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    qf = big_n + 1

    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    forward = 100 * np.ones((big_n + 2, big_t + 1))

    # +1 på den sidste variabel, fordi der bruges range() så det sidste tal kommer med
    for s in range(1, big_n+1):
        forward[s, 1] = transitions[0, s] * emissions[s, observations[1]]
    for t in range(2, big_t+1):
        for s in range(1, big_n+1):
            sum = 0
            for s_prime in range(1, big_n+1):
                sum += forward[s_prime, t-1]*transitions[s_prime,
                                                         s]*emissions[s, observations[t]]
            forward[s, t] = sum
    sum = 0
    for s in range(1, big_n+1):
        sum += forward[s, big_t]*transitions[s, qf]
    forward[qf, big_t] = sum
    return sum

    # COMPLETE THIS METHOD
    # Returns a probability (float)


def compute_viterbi(states, observations, transitions, emissions):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    qf = big_n + 1

    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    viterbi = 100 * np.ones((big_n + 2, big_t + 1))

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    backpointers = 100 * np.ones((big_n + 2, big_t + 1), dtype=int)

    for s in range(1, big_n+1):
        viterbi[s, 1] = transitions[0, s]*emissions[s, observations[1]]
        backpointers[s, 1] = 0
    for t in range(2, big_t+1):
        for s in range(1, big_n+1):
            for s_prime in range(1, big_n+1):
                viterbi[s, t] = max(
                    [viterbi[s_prime, t - 1] * transitions[s_prime, s] * emissions[s, observations[t]]])
                backpointers[s, t] = argmax(
                    [viterbi[s_prime, t - 1]*transitions[s_prime, s]])

    for s in range(1, big_n + 1):
        viterbi[qf, big_t] = max([viterbi[s, big_t] * transitions[s, qf]])
        backpointers[qf, big_t] = argmax(
            [viterbi[s, big_t] * transitions[s, qf]])

    out = []
    index = backpointers[big_n+1, big_t]
    for colum in reversed(range(1, big_t+1)):
        index = backpointers[index+1, colum]
        out.append(states[index+1])
    return out

    # COMPLETE THIS METHOD
    # Returns a path (list of strings indicating if it was hot or cold that day)


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))
    return max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
