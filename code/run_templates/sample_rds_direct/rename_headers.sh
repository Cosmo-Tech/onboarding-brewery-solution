if [ -z $CSM_OUTPUT_ABSOLUTE_PATH ]; then
    echo "CSM_OUTPUT_ABSOLUTE_PATH is not set"
    exit 1
else
    echo "CSM_OUTPUT_ABSOLUTE_PATH is set to $CSM_OUTPUT_ABSOLUTE_PATH"
    find $CSM_OUTPUT_ABSOLUTE_PATH -type f -exec sed -i -e 's/ //g' {} \;
fi