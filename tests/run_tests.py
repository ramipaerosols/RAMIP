#!/usr/bin/env python
"""
run_tests.py

Run multiple tests simultaneously on a single or multiple RAMIP datasets and
compile the results.

Developers: Willow Lin Stenglein, Cameron Cummins
Contact: cameron.cummins@utexas.edu
Last Header Update: 10/10/24
"""
from test_monotonic import test_monotonic
from test_calendar import test_calendar
from test_units import test_units
from test_variable_name import test_variable_name
from test_spatial_coords import test_spatial_coords
from utils import convert_paths

def run(paths: list[str], check_monotonic: bool=True, check_calendar: bool=True, check_units: bool=True, 
        check_variable_name: bool=True, check_spatial_coords: bool=True, verbose: bool=False) -> None:

    datasets = convert_paths(paths)
    checks = {} # Dictionary to store the results of each check
    summary_msg = "" 

    if check_monotonic:
        summary_msg += test_monotonic(datasets, verbose, checks)
    if check_calendar:
        summary_msg += test_calendar(datasets, verbose, checks)
    if check_units:
        summary_msg += test_units(datasets, verbose, checks)
    if check_variable_name:
        summary_msg += test_variable_name(datasets, verbose, checks)
    if check_spatial_coords:
        summary_msg += test_spatial_coords(datasets, verbose, checks)

    print(f"\n\nSUMMARY: {sum(checks.values())}/{len(checks)} checks passed.")
    print("=============================================================")
    print(summary_msg)

    # Check if we should offer some helpful advice 
    if int(sum(checks.values())) < len(checks) and not verbose:
        print("If you would like more information on why the checks failed, run the function with the verbose flag set to True. To avoid this output becoming too long, we would recommend running the function with just two files at a time.")


# if __name__ == "__main__":
#     pass