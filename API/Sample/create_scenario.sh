. set_env.sh
envsubst < create_scenario.yaml > /tmp/create_scenario.yaml
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/workspaces/${WORKSPACE}/runners" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/yaml" --data-binary "@/tmp/create_scenario.yaml"
echo
echo Add EXPORT SCENARIO=r-xxxxx in your set_env.sh