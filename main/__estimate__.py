from collections import Counter
import json
import sys
import dataclasses

from main.ElasticsearchAdapter import ElasticsearchAdapter

from main.PostgresAdapter import PostgresAdapter

elasticsearchAdapter = ElasticsearchAdapter()
postgresAdapter = PostgresAdapter()


@dataclasses.dataclass
class Issue:
    issue: tuple = None
    id: str = None
    summary: str = None
    type: str = None
    priority: str = None
    words: [] = None

    def __post_init__(self):
        self.id: str = str(issue[0])
        self.summary: str = str(issue[1])
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


def get_most_common(issue):
    big_array = []
    for word in issue.words:
        json_array_result = elasticsearchAdapter.search_by_summary(word)
        big_array.extend(get_result_ids(json_array_result))
    counter = Counter(big_array)
    return counter.most_common(10)


def estimate_strategy_one(issue):
    counter_array = get_most_common(issue)
    total_second = 0
    count = 0
    for element in counter_array:
        time = get_fixed_time(element[0])
        if time != 0:
            count = count + 1
            total_second += get_fixed_time(element[0])
    return total_second / count


def estimate_strategy_two(issue):
    counter_array = get_most_common(issue)
    total_second = 0
    count = 0
    for element in counter_array:
        element_id = element[0]
        element_count = element[1]
        time = get_fixed_time(element_id)
        if time != 0:
            count = count + element_count
            total_second += get_fixed_time(element_id) * element_count
    return total_second / count


actual_fixed_times = []
estimate_strategy_one_fixed_times = []
estimate_strategy_two_fixed_times = []
estimate_strategy_three_fixed_times = []
estimate_strategy_four_fixed_times = []

for x in range(3):
    actual_fixed_times.clear()
    estimate_strategy_one_fixed_times.clear()
    estimate_strategy_two_fixed_times.clear()
    estimate_strategy_three_fixed_times.clear()
    estimate_strategy_four_fixed_times.clear()

    test = postgresAdapter.get_issues_by_rate((x + 1) * 10)

    for issue in test:
        var = Issue(issue)
        actual_fixed_times.append(get_fixed_time(var.id))
        estimate_strategy_one_fixed_times.append(estimate_strategy_one(var))
        estimate_strategy_two_fixed_times.append(estimate_strategy_two(var))
        # estimate_strategy_three_fixed_times.append(estimate_strategy_three(var))
        # estimate_strategy_four_fixed_times.append(estimate_strategy_four(var))

    print(len(actual_fixed_times))
