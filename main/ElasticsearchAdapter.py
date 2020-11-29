from elasticsearch import Elasticsearch


class ElasticsearchAdapter:
    es = Elasticsearch()

    def add_document(self, issue):
        res = self.es.index(index="project", doc_type='issue', id=issue['id'], body=issue)
        if res['result'] != "created":
            print("error")
        self.es.indices.refresh(index="project")

    def search_by_summary(self, key, is_cluster, is_assignee, issue):
        json_array = []

        if is_cluster and is_assignee:
            query = {
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "filter": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "match": {
                                                            "fields.summary": key
                                                        }
                                                    }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                        },
                                        {
                                            "bool": {
                                                "filter": [
                                                    {
                                                        "bool": {
                                                            "should": [
                                                                {
                                                                    "match": {
                                                                        "fields.priority.name": issue.priority
                                                                    }
                                                                }
                                                            ],
                                                            "minimum_should_match": 1
                                                        }
                                                    },
                                                    {
                                                        "bool": {
                                                            "filter": [
                                                                {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match": {
                                                                                    "fields.issuetype.name": issue.type
                                                                                }
                                                                            }
                                                                        ],
                                                                        "minimum_should_match": 1
                                                                    }
                                                                },
                                                                {
                                                                    "bool": {
                                                                        "filter": [
                                                                            {
                                                                                "bool": {
                                                                                    "should": [
                                                                                        {
                                                                                            "match": {
                                                                                                "fields.resolution.name": "Fixed"
                                                                                            }
                                                                                        }
                                                                                    ],
                                                                                    "minimum_should_match": 1
                                                                                }
                                                                            },
                                                                            {
                                                                                "bool": {
                                                                                    "should": [
                                                                                        {
                                                                                            "match": {
                                                                                                "fields.assignee.name": issue.assignee
                                                                                            }
                                                                                        }
                                                                                    ],
                                                                                    "minimum_should_match": 1
                                                                                }
                                                                            }
                                                                        ]
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        elif is_cluster and not is_assignee:
            query = {
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "filter": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "match": {
                                                            "fields.summary": key
                                                        }
                                                    }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                        },
                                        {
                                            "bool": {
                                                "filter": [
                                                    {
                                                        "bool": {
                                                            "should": [
                                                                {
                                                                    "match": {
                                                                        "fields.priority.name": issue.priority
                                                                    }
                                                                }
                                                            ],
                                                            "minimum_should_match": 1
                                                        }
                                                    },
                                                    {
                                                        "bool": {
                                                            "filter": [
                                                                {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match": {
                                                                                    "fields.issuetype.name": issue.type
                                                                                }
                                                                            }
                                                                        ],
                                                                        "minimum_should_match": 1
                                                                    }
                                                                },
                                                                {
                                                                    "bool": {
                                                                        "filter": [
                                                                            {
                                                                                "bool": {
                                                                                    "should": [
                                                                                        {
                                                                                            "match": {
                                                                                                "fields.resolution.name": "Fixed"
                                                                                            }
                                                                                        }
                                                                                    ],
                                                                                    "minimum_should_match": 1
                                                                                }
                                                                            }
                                                                        ]
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        elif not is_cluster and is_assignee:
            query = {
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "filter": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "match": {
                                                            "fields.summary": key
                                                        }
                                                    }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                        },
                                        {
                                            "bool": {
                                                "filter": [
                                                    {
                                                        "bool": {
                                                            "should": [
                                                                {
                                                                    "match": {
                                                                        "fields.assignee.name": issue.assignee
                                                                    }
                                                                }
                                                            ],
                                                            "minimum_should_match": 1
                                                        }
                                                    },
                                                    {
                                                        "bool": {
                                                            "filter": [
                                                                {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match": {
                                                                                    "fields.resolution.name": "Fixed"
                                                                                }
                                                                            }
                                                                        ],
                                                                        "minimum_should_match": 1
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        else:
            query = {
                "query": {
                    "dis_max": {
                        "queries": [
                            {"match": {"fields.summary": key}}
                        ],
                        "tie_breaker": 0.3
                    }
                }
            }

        res = self.es.search(index="project", body=query,
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
