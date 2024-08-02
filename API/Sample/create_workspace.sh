. set_env.sh
envsubst < create_workspace.yaml > /tmp/create_workspace.yaml
curl -L -k -X POST "${BASE_URL}/organizations/${ORGANIZATION}/workspaces" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/yaml" --data-binary "@/tmp/create_workspace.yaml"
echo
echo Add EXPORT WORKSPACE=w-xxxxx in your set_env.sh