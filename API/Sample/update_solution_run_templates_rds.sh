. set_env.sh
envsubst < update_solution_run_template_rds.json > /tmp/update_solution.json
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/solutions/${SOLUTION}/runTemplates" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/json" --data-binary "@/tmp/update_solution.json"