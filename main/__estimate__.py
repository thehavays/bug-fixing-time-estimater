from collections import Counter
import json

from main.ElasticsearchAdapter import ElasticsearchAdapter
from main.JiraWrapper import JiraWrapper
from main.PostgresAdapter import PostgresAdapter

jiraWrapper = JiraWrapper()
elasticsearchAdapter = ElasticsearchAdapter()
postgresAdapter = PostgresAdapter()

elasticsearchAdapter.delete_index("project")
postgresAdapter.delete_tables()
postgresAdapter.create_tables()

issues = jiraWrapper.get_all_issues("SPARK")
print(len(issues))

for issue in issues:
    elasticsearchAdapter.add_document(issue)
    postgresAdapter.issue_insert_query(issue)

print("Finished!")

# TO do ilk 10 çekilip
# def get_result_ids(json_array):
#     id_list = []
#     for json_object in json_array:
#         id_list.append(json_object['id'])
#     return id_list
#
#
# def get_words(text):
#     return text.split()
#
#
# words = get_words("NPE query data key the of product")
#
# big_array = []
#
# for word in words:
#     json_array_result = search_by_summary(word)
#     big_array.extend(get_result_ids(json_array_result))
#     print(len(big_array))
#
# counter = Counter(big_array)
# print(len(big_array))
#
# # most_common()
# most_common_element = counter.most_common(5)
# print(most_common_element)
#
# # for i in range(34):
# #     result = send_query(i*1000)
# #     issues = result['issues']
# #     for issue in issues:
# #         add_document_es(issue)
