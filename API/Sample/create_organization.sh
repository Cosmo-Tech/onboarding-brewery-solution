. set_env.sh
envsubst < create_organization.yaml > /tmp/create_organization.yaml
curl -L -k -X POST "${BASE_URL}/organizations" --header "X-CSM-API-KEY: ${API_KEY}" --header "Content-Type: application/yaml" --data-binary "@/tmp/create_organization.yaml"
echo
echo Add EXPORT ORGANIZATION=o-xxxxx in your set_env.sh