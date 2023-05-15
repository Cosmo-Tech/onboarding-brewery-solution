from pathlib import Path
import json
import pandas as pd
import os


def run_parameter_handler():
    """Run the parameter handler"""

    # Get path to bar file (based on environment variables)
    bar_file = get_dataset_file_from_env_vars("Bar.csv")

    # Read the desired scenario parameters from the parameter file
    # (the parameter file location is determined from an environment variable)
    stock, restock_quantity, num_waiters = get_bar_parameters()

    # Update the bar file using the scenario parameters
    update_bar_file_with_scenario_parameters(
        bar_file, stock, restock_quantity, num_waiters
    )


def get_dataset_file_from_env_vars(dataset_file_path):
    """Obtain the path to the specified dataset file based on environment variables"""

    # Datasets (loaded from a data source)
    dataset_path = os.environ.get("CSM_DATASET_ABSOLUTE_PATH")
    dataset_file = Path(dataset_path) / dataset_file_path

    return dataset_file


def get_bar_parameters():
    """Obtain the bar parameters from the scenario
    parameter file."""

    # Obtain scenario parameters from the parameter file
    parameter_file = get_parameter_file_from_env_vars()
    parameters = get_all_scenario_parameters(parameter_file)

    # Retrieve the desired parameters and store them in variables
    stock = get_parameter_value(parameters, "stock")
    restock_quantity = get_parameter_value(parameters, "restock_quantity")
    num_waiters = get_parameter_value(parameters, "num_waiters")

    return stock, restock_quantity, num_waiters


def get_parameter_file_from_env_vars():
    """Get the scenario parameter file based on an env variable"""

    # Path to scenario parameters (set by the user)
    parameter_path = os.environ.get("CSM_PARAMETERS_ABSOLUTE_PATH")
    parameter_file = Path(parameter_path) / "parameters.json"

    return parameter_file


def get_all_scenario_parameters(parameter_file):
    """
    Obtain the scenario parameters from the parameter file,
    whose location is based on environment variables
    """

    # get the parameters
    with open(parameter_file) as fh:
        parameters = json.load(fh)
    return parameters


def update_bar_file_with_scenario_parameters(
    bar_file, stock, restock_quantity, num_waiters
):
    """Update the bar file with new values for stock, restock_quantity and num_waiters"""

    # Load the Bar.csv dataset file
    df_bar = pd.read_csv(bar_file)
    # Apply scenario parameters. Note: if there are multiple bars, these
    # values are applied to every bar.
    df_bar["Stock"] = stock
    df_bar["NbWaiters"] = num_waiters
    df_bar["RestockQty"] = restock_quantity
    # Write to csv (i.e. overwrite previous bar file)
    df_bar.to_csv(bar_file, index=False)


def get_parameter_value(parameters, parameter_id):
    """Obtain the value of a parameter from the `parameters` variable.
    `parameters` is assumed to be of the following shape:
    [
        {'parameterId': '...', 'value': '...', 'varType': '...', 'isInherited': '...'},
        ...
    ]
    i.e. a list of dictionary objects, where each dictionary at least
    contains the 'parameterId' and 'value' keys.
    If the parameter contains a property "varType", an attempt is made to
    assign the correct variable type (if int or float).
    """

    for par in parameters:
        if parameter_id == par["parameterId"]:
            val = par["value"]
            # try setting the right var type
            try:
                vartype = par["varType"]
                if vartype == "int":
                    val = int(val)
                elif vartype == "number":
                    val = float(val)
                return val
            except KeyError:
                return val
    raise KeyError(f"Parameter {parameter_id} not found in {parameters}")


# Run the code in main()
if __name__ == "__main__":
    run_parameter_handler()
