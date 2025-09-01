import os
import pathlib
import shutil

from get_logger import logger

target_run_folder = os.environ.get("CSM_DATASET_ABSOLUTE_PATH", "Simulation/Resource/scenariorun-data")
default_dataset_path = pathlib.Path("Simulation/Resource/default_dataset")

target_path = pathlib.Path(target_run_folder)
target_path.mkdir(parents=True, exist_ok=True)

for csv_path in default_dataset_path.glob("*.csv"):
    logger.info(f"Processing {csv_path.name}")
    shutil.copy(csv_path, target_path)
