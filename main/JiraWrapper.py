from jira import JIRA


class JiraWrapper:
    options = {"server": "https://issues.apache.org/jira"}
    jira = JIRA(options)

    def get_projects(self):
        return self.jira.projects()

    def get_project_range(self, from_index, to_index):
        return sorted([project.key for project in self.get_projects()])[from_index:to_index]

    def get_necessary_field(self, project, start_at, result_count):
        return self.jira.search_issues(
            jql_str=f"project = {project} ORDER BY createdDate DESC",
            startAt=start_at,
            maxResults=result_count,
            validate_query=True,
            fields="issuetype, summary, status, resolution, created, updated, resolved, estimated, priority, "
                   "description, "
                   "assignee, "
                   "labels",
            expand="",
            json_result=True
        )

    def get_all_field(self, project, start_at, result_count):
        return self.jira.search_issues(
            jql_str=f"project = {project} ORDER BY createdDate DESC",
            startAt=start_at,
            maxResults=result_count,
            validate_query=True,
            expand="",
            json_result=True
        )

    def get_all_issues(self, project_name):
        issues = []
        i = 0
        chunk_size = 500
        while True:
            chunk = self.jira.search_issues(f'project = {project_name}', startAt=i, maxResults=chunk_size,
                                            json_result=True)
            i += len(chunk['issues'])
            issues += chunk['issues']
            print(len(issues))
            if chunk_size > len(chunk['issues']):
                break
        return issues
