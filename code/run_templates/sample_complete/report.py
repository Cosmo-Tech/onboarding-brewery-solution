import os

if os.environ.get("CSM_ORC_IS_SUCCESS") == "True":
    print("Run is a success")
else:
    print("Run is a failure")
