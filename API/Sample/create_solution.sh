. set_env.sh
envsubst < create_solution.yaml > /tmp/create_solution.yaml
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/solutions" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/yaml" --data-binary "@/tmp/create_solution.yaml"
echo
echo Add EXPORT SOLUTION=sol-xxxxx in your set_env.sh