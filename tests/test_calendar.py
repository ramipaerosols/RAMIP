import xarray as xr
from utils import find_different_datasets, get_check_msg, Logger


def check_calendar(ds1: xr.Dataset, ds2: xr.Dataset):
    return ds1.time.encoding['calendar'] == ds2.time.encoding['calendar']


def test_calendar(datasets: list, verbose = False, log: Logger = None):
    if Logger is not None:
        print = Logger.log
    
    different_datasets = find_different_datasets(datasets, check_calendar, verbose)
    msgs = ["Time coordinates do not use the same calendar across all datasets.", 
            "Time coordinates use the same calendar across all datasets."]
    print(get_check_msg(different_datasets, "Calendar Check", msgs)) 

