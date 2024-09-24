. set_env.sh
echo WARNING: this script will create a secret in kubernetes in the current configured context
if [ -z $K8S_CONTEXT ]; then
  echo "K8S_CONTEXT is not set, please set it in set_env.sh"
else
  kubectl config use-context ${K8S_CONTEXT}
  kubectl -n ${K8S_NAMESPACE} delete secret ${SECRET_S3_CA_NAME}
  kubectl -n ${K8S_NAMESPACE} create secret generic ${SECRET_S3_CA_NAME} \
  --from-file=${SECRET_S3_CA_FILE}
  echo
  echo Secret created with s3 ca pem information
fi
