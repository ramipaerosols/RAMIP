import xarray as xr
from utils import find_wrong_datasets, get_indiv_check_msg
from datetime import timedelta
import numpy as np
from colorama import Fore, Style
from utils import get_filename
import collections

def check_monotonic(ds1: xr.Dataset, verbose = False):
    if verbose and (not ds1.time.to_index().is_monotonic_increasing or not ds1.time.to_index().is_unique): 
        print(Fore.CYAN + f"Monotonic Check Err Output: " + Style.RESET_ALL)

        if not ds1.time.to_index().is_monotonic_increasing:
            # Find list of non-increasing indices 
            times = ds1.time.to_index()
            differences = np.diff(times)
            violations = list(np.where(differences < timedelta(0)))[0]
            
            if(len(violations) > 10):
                print(Fore.CYAN + f"The time values for {get_filename(ds1)} dataset are not fully increasing. Here are the first 10 time steps that violate the monotonic increasing condition: "  + Style.RESET_ALL)
                violations = violations[:10]
            else:
                print(Fore.CYAN + f"The time values for {get_filename(ds1)} dataset are not fully increasing. Here are the time steps that violate the monotonic increasing condition: "  + Style.RESET_ALL)
            for index in violations:
                print(f"{times[index]} -> {times[index+1]} (index {index} -> {index+1})")
            print()
        if not ds1.time.to_index().is_unique:
            duplicates = collections.defaultdict(list)
            for i, time in enumerate(ds1.time.to_index()):
                duplicates[time].append(i)
            # for k, v in sorted(duplicates.iteritems()):
            #     if len(v) >= 2:
            # get all duplicates where len(v) >= 2
            duplicates = [(k, v) for k, v in duplicates.items() if len(v) >= 2]
            if(len(duplicates) > 10):
                print(Fore.CYAN + f"The time values for {get_filename(ds1)} dataset are not unique. Here are the first 10 time steps that are not unique: "  + Style.RESET_ALL)
                duplicates = duplicates[:10]
            else:
                print(Fore.CYAN + f"The time values for {get_filename(ds1)} dataset are not unique. Here are the time steps that are not unique: "  + Style.RESET_ALL)
            for k, v in duplicates:
                print(f"{k} (indices {v})")
            print()

    return ds1.time.to_index().is_monotonic_increasing and ds1.time.to_index().is_unique


def test_monotonic(datasets: list, verbose = False, checks = None) -> str:
    wrong_datasets = find_wrong_datasets(datasets, check_monotonic, verbose)
    msgs = ["Time coordinates are not strictly increasing.", 
            "Time coordinates are strictly increasing."]
    return get_indiv_check_msg(wrong_datasets, "Monotonic Check", msgs, checks, len(datasets))

