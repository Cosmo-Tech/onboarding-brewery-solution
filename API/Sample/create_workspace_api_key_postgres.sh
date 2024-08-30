. set_env.sh
envsubst < create_workspace_api_key.yaml > /tmp/create_workspace_api_key.yaml
echo WARNING: this script will create a secret in kubernetes in the current configured context
if [ -z $K8S_CONTEXT ]; then
  echo "K8S_CONTEXT is not set, please set it in set_env.sh"
else
  kubectl config use-context $K8S_CONTEXT
  kubectl -n bahamut delete secret ${ORGANIZATION}-${WORKSPACE}
  kubectl -n bahamut create secret generic ${ORGANIZATION}-${WORKSPACE} \
  --from-literal CSM_API_KEY=${API_KEY} \
  --from-literal CSM_POSTGRES_HOST=${CSM_POSTGRES_HOST_K8S} \
  --from-literal CSM_POSTGRES_DB=${CSM_POSTGRES_DB} \
  --from-literal CSM_POSTGRES_SCHEMA=${CSM_POSTGRES_SCHEMA} \
  --from-literal CSM_POSTGRES_USER=${CSM_POSTGRES_USER} \
  --from-literal CSM_POSTGRES_PASSWORD=${CSM_POSTGRES_PASSWORD} \
  --from-literal CSM_POSTGRES_PORT=${CSM_POSTGRES_PORT}
  echo
  echo Secret created with postgresql information
fi