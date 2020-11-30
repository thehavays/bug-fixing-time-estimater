import dataclasses
import datetime
from collections import Counter

import matplotlib.pyplot as plot
import numpy as np
from sklearn.linear_model import LinearRegression

from main.ElasticsearchAdapter import ElasticsearchAdapter
from main.PostgresAdapter import PostgresAdapter

elasticsearchAdapter = ElasticsearchAdapter()
postgresAdapter = PostgresAdapter()


@dataclasses.dataclass
class Issue:
    issue: tuple = None
    id: str = None
    summary: str = None
    assignee: str = None
    created: datetime.datetime = None
    resolved: datetime.datetime = None
    fixed_time: float = None
    type: str = None
    priority: str = None
    words: [] = None

    def __post_init__(self):
        self.id: str = str(issue[0])
        self.summary: str = str(issue[1])
        self.assignee: str = str(issue[11])
        self.created: datetime.datetime = issue[5]
        self.resolved: datetime.datetime = issue[7]
        self.fixed_time: float = (self.resolved - self.created).total_seconds()
        self.type: str = str(issue[9])
        self.priority: str = str(issue[10])
        self.words: [] = self.summary.split()


def get_result_ids(json_array):
    id_list = []
    for json_object in json_array:
        id_list.append(json_object['id'])
    return id_list


def get_fixed_time(issue_id):
    return postgresAdapter.get_issue_fixed_time(issue_id)


def get_array_fixed_time(issue_id_array):
    return postgresAdapter.get_issue_array_fixed_time(issue_id_array)


def get_most_common(searched_issue, is_cluster, is_assignee):
    big_array = []
    for word in searched_issue.words:
        json_array_result = elasticsearchAdapter.search_by_summary(word, is_cluster, is_assignee, searched_issue)
        temp = get_result_ids(json_array_result)
        big_array.extend(temp)
    counter = Counter(big_array)
    return counter.most_common(10)


def find_max_time(lst3):
    max_time = 0.0
    for element in lst3:
        current = element[2].total_seconds()
        if max_time < current:
            max_time = current
    return max_time


def get_mean(most_common, strategy):
    total_second = 0
    count = 0
    if len(most_common) == 0:
        return 0

    fixed_times = get_array_fixed_time(most_common)

    dict1 = dict(most_common)
    dict2 = dict(fixed_times)
    lst3 = [(k, dict1[k], dict2[k]) for k in sorted(dict1)]

    max_time = find_max_time(lst3)

    for element in lst3:
        repetition_count = element[1]
        time = element[2].total_seconds()
        if time != 0:
            if strategy == "weighted":
                total_second += time * repetition_count
                count += repetition_count
            elif strategy == "arithmetic":
                total_second += time
                count += 1
            elif strategy == "time_oriented":
                coefficient = pow(max_time / time, 2)
                total_second += time * coefficient
                count += coefficient
    return total_second / count


def estimate_strategy_one(most_common):
    return get_mean(most_common, "arithmetic")


def estimate_strategy_two(most_common):
    return get_mean(most_common, "weighted")


def estimate_strategy_three(most_common):
    return get_mean(most_common, "weighted")


def estimate_strategy_four(most_common):
    return get_mean(most_common, "arithmetic")


def estimate_strategy_five(most_common):
    return get_mean(most_common, "weighted")


def estimate_strategy_six(most_common):
    return get_mean(most_common, "time_oriented")


def plot_regression(train, pred):
    test_x = np.array(train)
    pred_y = np.array(pred)
    plot.plot(test_x, pred_y, 'o')

    print_regression(test_x.reshape(-1, 1), pred_y)
    m, b = np.polyfit(test_x, pred_y, 1)

    plot.plot(test_x, m * test_x + b)
    plot.show()


def print_regression(train, pred):
    model = LinearRegression()
    model.fit(train, pred)
    model = LinearRegression().fit(train, pred)
    r_sq = model.score(train, pred)
    print('coefficient of determination:', r_sq)


actual_fixed_times_one = []
actual_fixed_times_two = []
actual_fixed_times_three = []
actual_fixed_times_four = []
actual_fixed_times_five = []
actual_fixed_times_six = []
estimate_strategy_one_fixed_times = []
estimate_strategy_two_fixed_times = []
estimate_strategy_three_fixed_times = []
estimate_strategy_four_fixed_times = []
estimate_strategy_five_fixed_times = []
estimate_strategy_six_fixed_times = []

for x in range(3):
    actual_fixed_times_one.clear()
    actual_fixed_times_two.clear()
    actual_fixed_times_three.clear()
    actual_fixed_times_four.clear()
    actual_fixed_times_five.clear()
    actual_fixed_times_six.clear()
    estimate_strategy_one_fixed_times.clear()
    estimate_strategy_two_fixed_times.clear()
    estimate_strategy_three_fixed_times.clear()
    estimate_strategy_four_fixed_times.clear()
    estimate_strategy_five_fixed_times.clear()
    estimate_strategy_six_fixed_times.clear()

    test = postgresAdapter.get_issues_by_rate((x + 1) * 10)

    for issue in test[:200]:
        var = Issue(issue)

        most_common = get_most_common(var, is_cluster=False, is_assignee=False)
        most_common_assignee = get_most_common(var, is_cluster=True, is_assignee=True)
        most_common_clustered = get_most_common(var, is_cluster=True, is_assignee=False)

        fixed_time = var.fixed_time
        strategy_one_fixed_time = estimate_strategy_one(most_common)
        strategy_two_fixed_time = estimate_strategy_two(most_common)
        strategy_three_fixed_time = estimate_strategy_three(most_common_clustered)
        strategy_four_fixed_time = estimate_strategy_four(most_common_assignee)
        strategy_five_fixed_time = estimate_strategy_five(most_common_assignee)
        strategy_six_fixed_time = estimate_strategy_six(most_common_clustered)
        result_json = {"id": var.id, "fixed_time": fixed_time,
                       "one": strategy_one_fixed_time,
                       "two": strategy_two_fixed_time,
                       "three": strategy_three_fixed_time,
                       "four": strategy_four_fixed_time,
                       "five": strategy_five_fixed_time,
                       "six": strategy_six_fixed_time}
        print(result_json)

        if fixed_time != 0:
            if strategy_one_fixed_time != 0:
                actual_fixed_times_one.append(fixed_time)
                estimate_strategy_one_fixed_times.append(strategy_one_fixed_time)
            if strategy_two_fixed_time != 0:
                actual_fixed_times_two.append(fixed_time)
                estimate_strategy_two_fixed_times.append(strategy_two_fixed_time)
            if strategy_three_fixed_time != 0:
                actual_fixed_times_three.append(fixed_time)
                estimate_strategy_three_fixed_times.append(strategy_three_fixed_time)
            if strategy_four_fixed_time != 0:
                actual_fixed_times_four.append(fixed_time)
                estimate_strategy_four_fixed_times.append(strategy_four_fixed_time)
            if strategy_five_fixed_time != 0:
                actual_fixed_times_five.append(fixed_time)
                estimate_strategy_five_fixed_times.append(strategy_five_fixed_time)
            if strategy_six_fixed_time != 0:
                actual_fixed_times_six.append(fixed_time)
                estimate_strategy_six_fixed_times.append(strategy_six_fixed_time)

    plot_regression(actual_fixed_times_one, actual_fixed_times_one)
    plot_regression(actual_fixed_times_one, estimate_strategy_one_fixed_times)
    plot_regression(actual_fixed_times_two, estimate_strategy_two_fixed_times)
    plot_regression(actual_fixed_times_three, estimate_strategy_three_fixed_times)
    plot_regression(actual_fixed_times_four, estimate_strategy_four_fixed_times)
    plot_regression(actual_fixed_times_five, estimate_strategy_five_fixed_times)
    plot_regression(actual_fixed_times_six, estimate_strategy_six_fixed_times)

    print("Step for %", (x + 1) * 10, "test and %", (9 - x) * 10, "train data", " completed!")
