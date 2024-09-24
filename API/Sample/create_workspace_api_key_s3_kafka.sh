. set_env.sh
echo WARNING: this script will create a secret in kubernetes in the current configured context
if [ -z $K8S_CONTEXT ]; then
  echo "K8S_CONTEXT is not set, please set it in set_env.sh"
else
  kubectl config use-context $K8S_CONTEXT
  kubectl -n bahamut delete secret ${ORGANIZATION}-${WORKSPACE}
  kubectl -n bahamut create secret generic ${ORGANIZATION}-${WORKSPACE} \
  --from-literal CSM_API_KEY=${API_KEY} \
  --from-literal AWS_ENDPOINT_URL=${AWS_ENDPOINT_URL} \
  --from-literal AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  --from-literal AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  --from-literal S3_BUCKET_NAME=${S3_BUCKET_NAME} \
  --from-literal S3_USE_SSL=${S3_USE_SSL} \
  --from-literal S3_CA_PEM=${S3_CA_PEM} \
  --from-literal CSM_NOTIFY_KAFKA=${CSM_NOTIFY_KAFKA} \
  --from-literal CSM_KAFKA_BROKER=${CSM_KAFKA_BROKER} \
  --from-literal CSM_KAFKA_TOPIC=${CSM_KAFKA_TOPIC} \
  --from-literal CSM_KAFKA_USERNAME=${CSM_KAFKA_USERNAME} \
  --from-literal CSM_KAFKA_PASSWORD=${CSM_KAFKA_PASSWORD} \
  --from-literal CSM_KAFKA_SSL=${CSM_KAFKA_SSL} \
  --from-literal CSM_KAFKA_CA_PEM=${CSM_KAFKA_CA_PEM}
  echo
  echo Secret created with postgresql information
fi