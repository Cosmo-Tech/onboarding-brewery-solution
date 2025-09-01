import os

from get_logger import logger

prefixes = ["CSM", "AZURE", "IDP"]
max_key_length = 0
for env_key, env_value in sorted(os.environ.items()):
    for prefix in prefixes:
        if env_key.startswith(prefix) and "SECRET" not in env_key:
            max_key_length = max(max_key_length, len(env_key))

for env_key, env_value in sorted(os.environ.items()):
    for prefix in prefixes:
        if env_key.startswith(prefix) and "SECRET" not in env_key:
            logger.info(f"{env_key:<{max_key_length}} : {env_value}")
