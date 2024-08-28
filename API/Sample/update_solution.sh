. set_env.sh
envsubst < update_solution.json > /tmp/update_solution.json
curl -L -k -X PATCH "${BASE_URL}/organizations/${ORGANIZATION}/solutions/${SOLUTION}" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/json" --data-binary "@/tmp/update_solution.json"