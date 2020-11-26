from elasticsearch import Elasticsearch


class ElasticsearchAdapter:
    es = Elasticsearch()

    def add_document(self, issue):
        res = self.es.index(index="project", doc_type='issue', id=issue['id'], body=issue)
        if res['result'] != "created":
            print("error")
        self.es.indices.refresh(index="project")

    def search_by_summary(self, key):
        json_array = []
        res = self.es.search(index="project", body={
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"fields.summary": key}}
                    ],
                    "tie_breaker": 0.3
                }
            }
        },
                             size=10000)
        for hit in res['hits']['hits']:
            json_array.append(hit["_source"])
        return json_array

    def search_by_id(self, key):
        json_array = []
        res = self.es.search(index="project", body={"query": {'match': {'_id': key}}}, size=1)
        for hit in res['hits']['hits']:
            json_array.append(hit["_source"])
        return json_array

    def delete_index(self, index_name):
        index_name = index_name if index_name is not None else None
        self.es.indices.delete(index=index_name, ignore=[400, 404])
