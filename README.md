# bug-fixing-time-estimator
Bug fixing time estimator for public Jira projects.



docker run -d -P -p 5432:5432 --name masterPostgres -e POSTGRES_USER=postgres -e=POSTGRES_PASSWORD=postgres postgres:11.8

docker run -d -p 9200:9200 -p 9300:9300 --name masterElasticSearch --log-opt max-size=10m --log-opt max-file=2 -e "discovery.type=single-node" elasticsearch:7.9.3

docker run -d -p 5601:5601 --link masterElasticSearch:elasticsearch --name masterKibana kibana:7.9.3