import numpy as np
from itertools import combinations


class Tournament:
    # Elo tournament manager
    def __init__(self, entries):
        self.entries = {entry: 1200 + np.random.random() for entry in entries}
        items = list(self.entries.items())
        np.random.shuffle(items)
        self.entries = dict(items)

        self.k = 16
        self.reset()

    def reset(self):
        items = list(self.entries.items())
        # np.random.shuffle(items)
        self.entries = dict(items)
        self.matches = list(combinations(items, 2))
        np.random.shuffle(self.matches)
        if len(self.matches[-1]) == 1:
            self.matches.pop()
        self.k += 1
        # gradually increase k as scores become more accurate

    def next_match(self):
        if len(self.matches) == 0:
            self.reset()
        return self.matches.pop()

    def update(self, entry1, entry2, result):
        score_diff = self.entries[entry1] - self.entries[entry2]
        if score_diff > 400 * 30:
            expected_score = 0
        elif score_diff < -400 * 30:
            expected_score = 1
        else:
            expected_score = 1.0 / (
                1.0 + 10.0 ** ((self.entries[entry1] - self.entries[entry2]) / 400.0)
            )

        score_exchange = (20 / self.k + 10) * (result - expected_score)
        self.entries[entry1] += score_exchange
        self.entries[entry2] -= score_exchange

        # print(self.entries.values())


def sortedness(l):
    # assumes l is a permutation of range(n) for some n
    n = len(l)
    scores = []
    for idx, value in enumerate(l):
        delta_pos = idx - value
        # how far off the item is from the correct place
        scores.append(delta_pos)
    return np.std(scores), max(scores)


def is_sorted(l):
    return all(l[i] <= l[i + 1] for i in range(len(l) - 1))


def run_experiment(num_values, max_comp):
    tour = Tournament(list(range(num_values)))
    sortedness_vals = []
    for i in range(max_comp):
        pair = tour.next_match()
        # if abs(pair[0][0] - pair[1][0]) < np.sqrt(num_values):
        # tour.update(pair[0][0], pair[1][0], 0.5)
        if pair[0][0] < pair[1][0]:
            # print(pair, 0)
            tour.update(pair[0][0], pair[1][0], 0)
        elif pair[0][0] > pair[1][0]:
            # print(pair, 1)
            tour.update(pair[0][0], pair[1][0], 1)

        sorted_entries = sorted(tour.entries.items(), key=lambda item: item[1])
        sortedness_vals.append(sortedness([x[0] for x in sorted_entries]))
    return np.array(sortedness_vals)


def main():
    for num_values in range(3, 40, 2):
        num_tests = 100
        max_comp = 2 * num_values
        sum_iter = np.zeros((max_comp, 2))
        for test in range(num_tests):
            sum_iter += run_experiment(num_values, max_comp)
        print(num_values, sum_iter[0] / num_tests, sum_iter[-1] / num_tests, sep="\t")


if __name__ == "__main__":
    main()
