#!/usr/bin/env python
"""
run_tests.py

Run multiple tests simultaneously on a single or multiple RAMIP datasets and
compile the results.

Developers: Willow Lin Stenglein, Cameron Cummins
Contact: cameron.cummins@utexas.edu
Last Header Update: 10/10/24
"""
from tests.test_monotonic import test_monotonic
from tests.test_calendar import test_calendar
from tests.test_units import test_units
from tests.test_variable_name import test_variable_name
from tests.test_spatial_coords import test_spatial_coords
from tests.utils import convert_paths, get_filename
from tests.show_single import show_single
from colorama import Fore, Style

def check_model(paths: list[str], verbose: bool=False) -> None:
    run(paths, check_variable_name=False, check_units=False, verbose=verbose)


def run(paths: str | list[str], verbose: bool=False, check_monotonic: bool=True, check_calendar: bool=True, 
        check_units: bool=True, check_variable_name: bool=True, check_spatial_coords: bool=True) -> None:

    datasets = convert_paths(paths)

    if(isinstance(paths, str)):
        show_single(datasets[0], verbose)
        return 
    
    if(len(datasets) == 0):
        print(Fore.RED + "No datasets passed in." + Style.RESET_ALL)
        return 

    checks = {} # Dictionary to store the results of each check
    summary_msg = "" 

    if verbose:
        print(f"Checking {len(datasets)} datasets: {[get_filename(ds) for ds in datasets]}")
        print("\n")

    datasets_with_time = [ds for ds in datasets if 'time' in ds.dims]
    if len(datasets) != len(datasets_with_time) and (check_monotonic or check_calendar):
        tmp = [get_filename(ds) for ds in datasets if 'time' not in ds.dims]
        summary_msg += f"WARNING: The following datasets do not have a time dimension and will not be checked for monotonicity or correct calendar encoding: {tmp}\n\n"

    if check_monotonic:
        summary_msg += test_monotonic(datasets_with_time, verbose, checks) + "\n"
    if check_calendar:
        summary_msg += test_calendar(datasets_with_time, verbose, checks) + "\n"
    if check_units:
        summary_msg += test_units(datasets, verbose, checks) + "\n"
    if check_variable_name:
        summary_msg += test_variable_name(datasets, verbose, checks) + "\n"
    if check_spatial_coords:
        summary_msg += test_spatial_coords(datasets, verbose, checks) + "\n"

    print(f"\n\nSUMMARY: {sum(checks.values())}/{len(checks)} checks passed.")
    print("=============================================================")
    print(summary_msg)

    # Check if we should offer some helpful advice 
    if int(sum(checks.values())) < len(checks) and not verbose:
        print("If you would like more information on why the checks failed, run the function with the verbose flag set to True. To avoid this output becoming too long, we would recommend running the function with just two files at a time.")


# if __name__ == "__main__":
#     pass