import dataclasses
from collections import Counter

import matplotlib.pyplot as plot
import numpy as np
from sklearn.metrics import mean_squared_error

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
    type: str = None
    priority: str = None
    words: [] = None

    def __post_init__(self):
        self.id: str = str(issue[0])
        self.summary: str = str(issue[1])
        self.assignee: str = str(issue[11])
        self.type: str = str(issue[9])
        self.priority: str = str(issue[10])
        self.words: [] = self.summary.split()


def get_result_ids(json_array):
    id_list = []
    for json_object in json_array:
        id_list.append(json_object['id'])
    return id_list


def get_fixed_time(id):
    return postgresAdapter.get_issue_fixed_time(id)


def get_most_common(issue, is_cluster, is_assignee):
    big_array = []
    for word in issue.words:
        json_array_result = elasticsearchAdapter.search_by_summary(word, is_cluster, is_assignee, issue)
        temp = get_result_ids(json_array_result)
        big_array.extend(temp)
    counter = Counter(big_array)
    return counter.most_common(10)


def get_arithmetic_mean(most_common):
    total_second = 0
    count = 0
    if len(most_common) == 0:
        return 0
    for element in most_common:
        time = get_fixed_time(element[0])
        if time != 0:
            count = count + 1
            total_second += time
    return total_second / count


def get_weighted_mean(most_common):
    total_second = 0
    count = 0
    if len(most_common) == 0:
        return 0
    for element in most_common:
        element_id = element[0]
        element_count = element[1]
        time = get_fixed_time(element_id)
        if time != 0:
            count = count + element_count
            total_second += time * element_count
    return total_second / count


def estimate_strategy_one(most_common):
    return get_arithmetic_mean(most_common)


def estimate_strategy_two(most_common):
    return get_weighted_mean(most_common)


def estimate_strategy_three(most_common):
    return get_weighted_mean(most_common)


def estimate_strategy_four(most_common):
    return get_arithmetic_mean(most_common)


def estimate_strategy_five(most_common):
    return get_weighted_mean(most_common)


actual_fixed_times = []
estimate_strategy_one_fixed_times = []
estimate_strategy_two_fixed_times = []
estimate_strategy_three_fixed_times = []
estimate_strategy_four_fixed_times = []
estimate_strategy_five_fixed_times = []


def plot_regression(train, pred):
    test_x = np.array(train)
    pred_y = np.array(pred)
    plot.plot(test_x, pred_y, 'o')

    m, b = np.polyfit(test_x, pred_y, 1)

    plot.plot(test_x, m * test_x + b)
    plot.show()


for x in range(3):
    actual_fixed_times.clear()
    estimate_strategy_one_fixed_times.clear()
    estimate_strategy_two_fixed_times.clear()
    estimate_strategy_three_fixed_times.clear()
    estimate_strategy_four_fixed_times.clear()
    estimate_strategy_five_fixed_times.clear()

    test = postgresAdapter.get_issues_by_rate((x + 1) * 10)

    for issue in test:
        var = Issue(issue)

        most_common = get_most_common(var, is_cluster=False, is_assignee=False)
        most_common_assignee = get_most_common(var, is_cluster=True, is_assignee=True)
        most_common_clustered = get_most_common(var, is_cluster=True, is_assignee=False)

        fixed_time = get_fixed_time(var.id)
        strategy_one_fixed_time = estimate_strategy_one(most_common)
        strategy_two_fixed_time = estimate_strategy_two(most_common)
        strategy_three_fixed_time = estimate_strategy_three(most_common_clustered)
        strategy_four_fixed_time = estimate_strategy_four(most_common_assignee)
        strategy_five_fixed_time = estimate_strategy_five(most_common_assignee)
        result_json = {"id": var.id, "fixed_time": fixed_time,
                       "one": strategy_one_fixed_time,
                       "two": strategy_two_fixed_time,
                       "three": strategy_three_fixed_time,
                       "four": strategy_four_fixed_time,
                       "five": strategy_five_fixed_time}
        print(result_json)

        actual_fixed_times.append(fixed_time)
        estimate_strategy_one_fixed_times.append(strategy_one_fixed_time)
        estimate_strategy_two_fixed_times.append(strategy_two_fixed_time)
        estimate_strategy_three_fixed_times.append(strategy_three_fixed_time)
        estimate_strategy_four_fixed_times.append(strategy_four_fixed_time)
        estimate_strategy_five_fixed_times.append(strategy_five_fixed_time)

    print("Mean square error for one = ", mean_squared_error(actual_fixed_times, estimate_strategy_one_fixed_times))
    print("Mean square error for two = ", mean_squared_error(actual_fixed_times, estimate_strategy_two_fixed_times))
    print("Mean square error for three = ", mean_squared_error(actual_fixed_times, estimate_strategy_three_fixed_times))
    print("Mean square error for four = ", mean_squared_error(actual_fixed_times, estimate_strategy_four_fixed_times))
    print("Mean square error for five = ", mean_squared_error(actual_fixed_times, estimate_strategy_five_fixed_times))

    plot_regression(actual_fixed_times, estimate_strategy_one_fixed_times)
    plot_regression(actual_fixed_times, estimate_strategy_two_fixed_times)
    plot_regression(actual_fixed_times, estimate_strategy_three_fixed_times)
    plot_regression(actual_fixed_times, estimate_strategy_four_fixed_times)
    plot_regression(actual_fixed_times, estimate_strategy_five_fixed_times)

    print("Step for %", (x + 1) * 10, "test and %", (9 - x) * 10, "train data", " completed!")
