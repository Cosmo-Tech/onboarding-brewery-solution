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
  --from-literal CSM_POSTGRES_HOST=${AWS_ENDPOINT_URL} \
  --from-literal CSM_POSTGRES_HOST=${AWS_ACCESS_KEY_ID} \
  --from-literal CSM_POSTGRES_HOST=${AWS_SECRET_ACCESS_KEY} \
  --from-literal CSM_POSTGRES_HOST=${S3_BUCKET_NAME}
  echo
  echo Secret created with postgresql information
fi