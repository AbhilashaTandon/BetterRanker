import numpy as np
from itertools import combinations


class Tournament:
    # Elo tournament manager
    def __init__(self, entries):
        self.entries = {entry: 1200 for entry in entries}
        items = list(self.entries.items())
        np.random.shuffle(items)
        self.entries = dict(items)

        self.k = 16
        self.reset()

    def reset(self):
        items = list(self.entries.items())
        # np.random.shuffle(items)
        self.entries = dict(items)
        self.matches = np.random.shuffle(list(combinations(items, 2)))
        if len(self.matches[-1]) == 1:
            self.matches.pop()
        self.k = self.k + 1
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

        score_exchange = (10 / self.k + 16) * (result - expected_score)
        self.entries[entry1] += score_exchange
        self.entries[entry2] -= score_exchange


def is_sorted(l):
    return all(l[i] <= l[i + 1] for i in range(len(l) - 1))


def run_experiment(num_values, max_comp):
    tour = Tournament(list(range(num_values)))
    for i in range(max_comp):
        pair = tour.next_match()
        if abs(pair[0][0] - pair[1][0]) < np.sqrt(num_values):
            tour.update(pair[0][0], pair[1][0], 0.5)
        elif pair[0][0] < pair[1][0]:
            # print(pair, 0)
            tour.update(pair[0][0], pair[1][0], 0)
        elif pair[0][0] > pair[1][0]:
            # print(pair, 1)
            tour.update(pair[0][0], pair[1][0], 1)
        if is_sorted(list(tour.entries.keys())):
            return i
        sorted_entries = sorted(tour.entries.items(), key=lambda item: item[1])
        print([x[0] for x in sorted_entries])
    return max_comp


def main():
    for num_values in range(3, 40):
        num_tests = 100
        sum_iter = 0
        for test in range(num_tests):
            sum_iter += run_experiment(num_values, 10000)
        print(num_values, sum_iter / num_tests)


if __name__ == "__main__":
    run_experiment(100, 100)
