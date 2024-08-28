. set_env.sh
curl -L -k -X GET "${BASE_URL}/organizations/${ORGANIZATION}/workspaces/${WORKSPACE}/runners/${SCENARIO}" --header "X-CSM-API-KEY: ${API_KEY}"