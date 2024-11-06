import xarray as xr
from colorama import Fore, Style
from tests.utils import find_different_datasets, get_consensus_check_msg, get_filename
from tests.test_variable_name import check_vars_same_name


def check_units(ds1: xr.Dataset, ds2: xr.Dataset, verbose=False):
    if not check_vars_same_name(ds1, ds2, False):
        if verbose: 
            print(Fore.CYAN + f"Unit Check Err Output: ")
            print(f"Comparing {get_filename(ds1)} and {get_filename(ds2)}")
            print(f"The data variables NOT the same, so the units check fails by default."  + Style.RESET_ALL)
            print()
        return False


    for var in ds1.data_vars:
        if 'bnds' in var: 
            continue 
        if 'units' not in ds1[var].attrs or 'units' not in ds2[var].attrs:
            if 'units' not in ds1[var].attrs and 'units' not in ds2[var].attrs:
                continue
            print(Fore.CYAN + f"Unit Check Err Output: ")
            print(f"Comparing {get_filename(ds1)} and {get_filename(ds2)}")
            bad_ds = get_filename(ds1) if 'units' not in ds1[var].attrs else get_filename(ds2)
            print(f"No unit attribute for variable: {var} in {bad_ds}"  + Style.RESET_ALL)
            return False
        if ds1[var].attrs["units"] != ds2[var].attrs["units"]:
            print(Fore.CYAN + f"Unit Check Err Output: ")
            print(f"Comparing {get_filename(ds1)} and {get_filename(ds2)}")
            print(f"The units for the {var} variable are not the same. "  + Style.RESET_ALL)
            print(f"Units for {var} in the first dataset: {ds1[var].attrs['units']}")
            print(f"Units for {var} in the second dataset: {ds2[var].attrs['units']}")
            print()
            return False

    return True


def test_units(datasets: list, verbose = False, checks = None) -> str:
    different_datasets = find_different_datasets(datasets, check_units, verbose)
    msgs = ["Units are not equivalent across all datasets.", "Units are equivalent across all datasets."]
    return get_consensus_check_msg(different_datasets, "Units Check", msgs, checks, len(datasets))

