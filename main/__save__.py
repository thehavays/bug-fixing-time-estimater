import json

from main.ElasticsearchAdapter import ElasticsearchAdapter
from main.PostgresAdapter import PostgresAdapter

elasticsearchAdapter = ElasticsearchAdapter()
postgresAdapter = PostgresAdapter()

elasticsearchAdapter.delete_index("project")
postgresAdapter.delete_tables()
postgresAdapter.create_tables()

with open('data.json', 'r') as data_file:
    json_data = data_file.read()

issues = json.loads(json_data)

for issue in issues:

    status = issue['fields']['status']['name']

    if status == 'Resolved' or status == 'Closed':
        elasticsearchAdapter.add_document(issue)
        postgresAdapter.issue_insert_query(issue)

print("Saving finished!")
