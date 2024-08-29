if [ ! -d "${CSM_DATASET_ABSOLUTE_PATH}" ]; then
echo creating folder "${CSM_DATASET_ABSOLUTE_PATH}"
mkdir -p "${CSM_DATASET_ABSOLUTE_PATH}"
fi
echo copying data from code/run_templates/sample/scenariorun-data/ to "${CSM_DATASET_ABSOLUTE_PATH}"
cp -r code/run_templates/sample/scenariorun-data/* "${CSM_DATASET_ABSOLUTE_PATH}"
echo copy done