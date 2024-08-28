. set_env.sh
envsubst < update_scenario.json > /tmp/update_scenario.json
curl -L -k -X PATCH "${BASE_URL}/organizations/${ORGANIZATION}/workspaces/${WORKSPACE}/runners/${SCENARIO}" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/json" --data-binary "@/tmp/update_scenario.json"