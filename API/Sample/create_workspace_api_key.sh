. set_env.sh
envsubst < create_workspace_api_key.yaml > /tmp/create_workspace_api_key.yaml
echo WARNING: this script will create a secret in kubernetes in the current configured context
if [ -z $K8S_CONTEXT ]; then
  echo "K8S_CONTEXT is not set, please set it in set_env.sh"
else
  kubectl config use-context $K8S_CONTEXT
  kubectl -n bahamut create secret generic ${ORGANIZATION}-${WORKSPACE} --from-literal CSM_API_KEY=${API_KEY}
  echo
  echo Secret created
fi