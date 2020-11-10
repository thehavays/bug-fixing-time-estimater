# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
import json

from jira import JIRA
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
options = {"server": "https://issues.apache.org/jira"}
jira = JIRA(options)

# Get all projects viewable by anonymous users.
projects = jira.projects()

print(projects)

# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted([project.key for project in projects])[0:]

print(keys)


def add_document_es(issue):
    res = es.index(index="project", doc_type='issue', id=issue['id'], body=issue)
    print(res['result'])

    res = es.get(index="project", id=issue['id'])
    print(res['_source'])

    es.indices.refresh(index="project")


def send_query(count):
    return jira.search_issues(
        jql_str="project = SPARK ORDER BY createdDate DESC",
        startAt=count,
        maxResults=1000,
        validate_query=True,
        fields="issuetype, summary, status, resolution, created, updated, estimated, priority, description,"
               "assignee, "
               "labels",
        expand="",
        json_result=True
    )


def search(key):
    json_array = []
    res = es.search(index="project", body={"query": {'match': {'fields.summary': key}}}, size=1000)
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        json_array.append(hit["_source"])
    return json_array


def get_result_ids(json_array):
    id_list = []
    for json_object in json_array:
        id_list.append(json_object['id'])
    return id_list


def get_words(text):
    return text.split()


words = get_words("NPE query verify")

for word in words:
    json_array_result = search(word)
    print(word, "\t", get_result_ids(json_array_result))

# get_result_ids(search("NPE"))
# search("query")

# for i in range(34):
#     result = send_query(i*1000)
#     issues = result['issues']
#     for issue in issues:
#         add_document_es(issue)

# with open('data.json', 'w') as outfile:
#     json.dump(result, outfile)
