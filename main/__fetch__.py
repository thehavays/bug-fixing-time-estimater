import json

from main.JiraWrapper import JiraWrapper

jiraWrapper = JiraWrapper()

issues = jiraWrapper.get_all_issues("SPARK")

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(issues, file, ensure_ascii=False, indent=4)

print("Fetching finished!")
