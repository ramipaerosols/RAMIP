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


def run(paths: list[str], check_monotonic: bool=True, check_calendar: bool=True, check_units: bool=True, check_variable_name: bool=True) -> None:

    
    
    if check_monotonic:
        pass
    if check_calendar:
        pass
    if check_units:
        pass
    if check_variable_name:
        pass


if __name__ == "__main__":
    pass