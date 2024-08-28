. set_env.sh
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/workspaces/${WORKSPACE}/runners/$SCENARIO/runs/$RUN/data/query" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/json" --data '{ "query": "SELECT * FROM CD_BarProbe" }'
