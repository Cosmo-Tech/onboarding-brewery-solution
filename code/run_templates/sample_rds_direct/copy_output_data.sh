export RESULT_DATASET_PATH="${CSM_DATASET_ABSOLUTE_PATH}/results"
if [ ! -d "${RESULT_DATASET_PATH}" ]; then
echo creating folder "${RESULT_DATASET_PATH}"
mkdir -p "${RESULT_DATASET_PATH}"
fi
echo copying data from ${CSM_OUTPUT_ABSOLUTE_PATH} to "${RESULT_DATASET_PATH}"
cp -r ${CSM_OUTPUT_ABSOLUTE_PATH}/* "${RESULT_DATASET_PATH}"
echo copy done