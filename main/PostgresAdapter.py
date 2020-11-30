import psycopg2


class PostgresAdapter:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="postgres",
                                           host="127.0.0.1",
                                           port="3002",
                                           database="bug_tracker")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        create_query = ("\n"
                        "        CREATE TABLE  IF NOT EXISTS issues ( id VARCHAR(255), \n"
                        "         summary VARCHAR,\n"
                        "         status VARCHAR(48),\n"
                        "         key VARCHAR, \n"
                        "         resolution VARCHAR(48),\n"
                        "         created TIMESTAMP,\n"
                        "         updated TIMESTAMP,\n"
                        "         resolved TIMESTAMP,\n"
                        "         estimated TIMESTAMP,\n"
                        "         issueType VARCHAR (48),\n"
                        "         priority VARCHAR (48),\n"
                        "         assignee VARCHAR (255),\n"
                        "         labels VARCHAR,\n"
                        "         PRIMARY KEY (id) )")
        self.cursor.execute(create_query)
        self.connection.commit()

    def delete_tables(self):
        delete_query = "DROP TABLE IF EXISTS issues"
        try:
            self.cursor.execute(delete_query)
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Table not exist!")

    def add_issues(self, issues):
        for issue in issues:
            self.add_issue(issue)
        self.connection.commit()

    def add_issue(self, issue):
        self.cursor.execute(self.issue_insert_query(issue))

    def normalize_dates(self):
        query = "UPDATE issues SET created = created + INTERVAL '2000' YEAR" \
                "WHERE created::DATE <= '2000-01-01 00:00:00.000000'::DATE;"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_issues_by_rate(self, rate):
        rate = rate / 10
        query = f"SELECT * FROM issues ORDER BY created DESC LIMIT (SELECT (count(*) / 10 * {rate})" \
                f" AS selnum FROM issues);"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_issue_count_by_rate(self, rate):
        rate = rate / 10
        query = f"SELECT count(*) from(SELECT * FROM issues ORDER BY created DESC " \
                f"LIMIT (SELECT (count( *) / 10 * {rate}) AS selnum FROM issues)) as sub;"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_issue_fixed_time(self, id):
        query = f"SELECT resolved-created FROM issues WHERE id = {id}::varchar;"

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return 0
        time_delta = result[0][0]
        return time_delta.total_seconds()

    def get_issue_array_fixed_time(self, element_array):
        where_clause = ""
        for element in element_array[:-1]:
            where_clause = where_clause + f"id = {element[0]}::varchar" + " or "
        where_clause += f"id = {element_array[-1][0]}::varchar"

        query = f"SELECT id, resolved-created FROM issues WHERE {where_clause};"

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def issue_insert_query(self, row_issue):

        id = None if row_issue['id'] is None else row_issue['id']
        summary = row_issue['fields']['summary']
        key = None if row_issue['key'] is None else row_issue['key']
        created = row_issue['fields']['created']
        updated = row_issue['fields']['updated']
        issueType = None if row_issue['fields']['issuetype'] is None else row_issue['fields']['issuetype']['name']
        status = row_issue['fields']['status']['name']
        priority = None if row_issue['fields']['priority'] is None else row_issue['fields']['priority']['name']
        label = None if row_issue['fields']['labels'] is None else row_issue['fields']['labels']
        resolution = None if row_issue['fields']['resolution'] is None else row_issue['fields']['resolution']['name']
        assignee = None if row_issue['fields']['assignee'] is None else row_issue['fields']['assignee']['name']
        resolved = None if row_issue['fields']['resolutiondate'] is None else row_issue['fields']['resolutiondate']

        query = """INSERT INTO issues ( id, summary, status, key, resolution, created, updated, resolved, \
                estimated, issueType, priority, assignee, labels) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        record_to_insert = (id, summary, status, key, resolution, created, updated, resolved,
                            None, issueType, priority, assignee, label)

        # query = f"INSERT INTO issues ( id, summary, status, key, resolution, created, updated, resolved, \
        #         issueType, priority, assignee, labels) VALUES({issue_id}, {summary}, {status}, {key}, \
        #         {resolution}, {created}, {updated}, {resolved},{issueType}, {priority}, {assignee}, {label});"

        self.cursor.execute(query, record_to_insert)
        self.connection.commit()
