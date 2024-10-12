import xarray as xr
from utils import find_different_datasets, get_check_msg


def check_monotonic(ds1: xr.Dataset, ds2: xr.Dataset):
    return ds1.time.to_index().is_monotonic_increasing and ds2.time.to_index().is_monotonic_increasing


def test_monotonic(datasets: list, verbose = False, checks = None):
    different_datasets = find_different_datasets(datasets, check_monotonic, verbose)
    msgs = ["Time coordinates are not monotonic.", 
            "Time coordinates are monotonic."]
    print(get_check_msg(different_datasets, "Monotonic Check", msgs, checks)) 

