import os
import shutil
import pytest
from math import isclose
from pathlib import Path
import pandas as pd
from ..main import (
    get_dataset_file_from_env_vars,
    get_parameter_file_from_env_vars,
    get_parameter_value,
    get_all_scenario_parameters,
    get_bar_parameters,
    update_bar_file_with_scenario_parameters,
    run_parameter_handler,
)

# Location of test data
test_data_path = Path(__file__).parent / "test-data"
parameter_path = test_data_path / "scenariorun-parameters"
dataset_path = test_data_path / "scenariorun-data"

# Some test scenario parameters
parameters = [
    {"parameterId": "int_parameter", "value": "3", "varType": "int"},
    {"parameterId": "number_parameter", "value": "3.5", "varType": "number"},
    {"parameterId": "string_parameter", "value": "banana", "varType": "string"},
    {"parameterId": "bool_parameter", "value": "true", "varType": "bool"},
]

compared_scenario_parameters = [
    {"parameterId": "stock", "value": "42", "varType": "int", "isInherited": False},
    {
        "parameterId": "restock_quantity",
        "value": "15",
        "varType": "int",
        "isInherited": False,
    },
    {
        "parameterId": "num_waiters",
        "value": "3",
        "varType": "int",
        "isInherited": False,
    },
]


def test_get_dataset_file_from_env_vars(monkeypatch):
    """Test getting the bar file from a env var (monkeypatched)"""

    monkeypatch.setenv("CSM_DATASET_ABSOLUTE_PATH", str(dataset_path))

    bar_file = get_dataset_file_from_env_vars("Bar.csv")
    # Assert the file exists
    assert bar_file.exists()

    # # TODO: Not sure I need to test this, because it only tests if I' ve set my env vars ok.
    # # Also: it's butt ugly & asking for trouble with the rel paths...
    # # assert it's the right file (form environment vars)
    # assert bar_file.resolve() == Path("../../scenariorun-data/Bar.csv")


def test_get_parameter_file_from_env_vars(monkeypatch):
    """Test getting the bar file from a env var (monkeypatched)"""

    # Temporarily set the environment variable
    monkeypatch.setenv("CSM_PARAMETERS_ABSOLUTE_PATH", str(parameter_path))
    # Get the parameter file from the temporary env var
    parameter_file = get_parameter_file_from_env_vars()

    # Assert the file exists
    assert parameter_file.exists()

    # # TODO: Not sure I need to test this, because it only tests if I' ve set my env vars ok.
    # # Also: it's butt ugly & asking for trouble with the rel paths...
    # # assert it's the right file (form environment vars)
    # assert bar_file.resolve() == Path("../../scenariorun-data/Bar.csv")


def test_get_all_scenario_parameters():
    """Test that get_all_scenario_parameters gets the correct parameters"""

    parameter_file = parameter_path / "parameters.json"
    scenario_parameters = get_all_scenario_parameters(parameter_file)

    assert scenario_parameters == compared_scenario_parameters


def test_get_bar_parameters(monkeypatch):
    """Test that get_bar_parameters reads the correct values from the parameters.json file"""

    monkeypatch.setenv("CSM_PARAMETERS_ABSOLUTE_PATH", str(parameter_path))

    # read file & get variables
    stock, restock_quantity, num_waiters = get_bar_parameters()

    # assert value for each parameter
    assert stock == 42
    assert restock_quantity == 15
    assert num_waiters == 3


@pytest.mark.parametrize(
    "current_parameter, expected_type, expected_value",
    [
        ("int_parameter", int, 3),
        ("number_parameter", float, 3.5),
        ("string_parameter", str, "banana"),
        ("bool_parameter", str, "true"),
    ],
)
def test_get_parameter_value(current_parameter, expected_type, expected_value):
    """Test that get_parameter_value returns the correct value in the correct format"""
    parameter_value = get_parameter_value(parameters, current_parameter)
    assert type(parameter_value) == expected_type
    if expected_type == float:
        assert isclose(parameter_value, expected_value)
    else:
        assert parameter_value == expected_value


def test_update_bar_file(tmp_path):
    """Test that the parameter handler applies the correct values to the Bar.csv"""

    orig_bar_file = dataset_path / "Bar.csv"
    expected_output_bar_file = test_data_path / "expected-update-dataset" / "Bar.csv"

    tmp_bar_file = shutil.copy(orig_bar_file, tmp_path)
    update_bar_file_with_scenario_parameters(
        tmp_bar_file, stock=84, restock_quantity=30, num_waiters=6
    )

    assert_csv_equal(tmp_bar_file, expected_output_bar_file)


def test_run_parameter_handler(tmp_path, monkeypatch):
    # Copy test data to temp path
    shutil.copytree(test_data_path, tmp_path, dirs_exist_ok=True)
    # set environment variables to temp paths
    monkeypatch.setenv(
        "CSM_PARAMETERS_ABSOLUTE_PATH", str(tmp_path / "scenariorun-parameters")
    )
    monkeypatch.setenv("CSM_DATASET_ABSOLUTE_PATH", str(tmp_path / "scenariorun-data"))

    # set paths
    path_dataset = Path(os.environ.get("CSM_DATASET_ABSOLUTE_PATH"))
    path_exp_outcome = tmp_path / "expected-main"

    # assert that starting values are as expected
    df_bar_orig = pd.read_csv(path_dataset / "Bar.csv")
    assert df_bar_orig["NbWaiters"][0] == 30
    assert df_bar_orig["RestockQty"][0] == 20
    assert df_bar_orig["Stock"][0] == 10
    df_bar_check = pd.read_csv(path_exp_outcome / "Bar.csv")
    assert df_bar_check["NbWaiters"][0] == 3
    assert df_bar_check["RestockQty"][0] == 15
    assert df_bar_check["Stock"][0] == 42

    # run main
    run_parameter_handler()

    # assert resulting values are as expected
    assert_csv_equal(path_dataset / "Bar.csv", path_exp_outcome / "Bar.csv")


def assert_csv_equal(file1, file2, **kwargs):
    """Compare the contents of two csv files using pandas"""
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    pd.testing.assert_frame_equal(df1, df2, **kwargs)
