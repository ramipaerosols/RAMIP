import xarray as xr
from utils import find_different_datasets, get_check_msg, get_filename


def check_vars_same_name(ds1: xarray.Dataset, ds2: xarray.Dataset, verbose: bool) -> bool:
    # Check that the variables in the datasets have the same name
    
    vars_1 = list(ds1.data_vars.keys())
    vars_2 = list(ds2.data_vars.keys())

    if vars_1 != vars_2:
        if verbose: 
            print(Fore.CYAN + f"Check 2 Err Output: ")
            print(f"Comparing {get_filename(ds1)} and {get_filename(ds2)}")
            print(f"The data variable names are NOT the same. Here are the names: "  + Style.RESET_ALL)
            print(vars_1)
            print(vars_2)
            print()

        return False

    return True


def test_units(datasets: list, verbose = False):
    different_datasets = find_different_datasets(datasets, check_vars_same_name, verbose)
    msgs = ["Variables do not have the same name across all datasets.", "Variables have the same name across all datasets."]
    print(get_check_msg(different_datasets, "Var Name Check", msgs)) 
