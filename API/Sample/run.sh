. set_env.sh
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/workspaces/${WORKSPACE}/runners/${SCENARIO}/start" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/yaml"
echo
echo Add EXPORT RUN=run-xxxxx in your set_env.sh
