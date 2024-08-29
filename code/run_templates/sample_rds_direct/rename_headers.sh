export RESULT_DATASET_PATH="${CSM_DATASET_ABSOLUTE_PATH}/results"
if [ -z $RESULT_DATASET_PATH ]; then
    echo "RESULT_DATASET_PATH is not set"
    exit 1
else
    echo "RESULT_DATASET_PATH is set to $RESULT_DATASET_PATH"
    find $RESULT_DATASET_PATH -type f -exec sed -i -e 's/ //g' {} \;
fi