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
