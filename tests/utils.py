import xarray
import numpy as np
from colorama import Fore, Style
from typing import Callable
from datetime import datetime


class Logger:
    def __init__(self):
        self.__logs = []

    def log(self, msg):
        self.__logs.append(msg)

    def getLogs(self):
        return self.__logs

def find_majority_ds(datasets: list[xarray.Dataset], check_equiv: Callable, verbose: bool) -> int: 
    r"""
    Determines the majority result from 'check_equiv' for a list of xarray
    Datasets using the Boyer–Moore majority vote algorithm.

    Parameters
    ----------
    datasets : list[xarray.Dataset]
        List of xarray Datasets to run 'check_equiv' on and compare results for
    check_equiv : Callable
        Function to run using datasets in 'datasets' as input.
    verbose : bool
        Whether or not to print full output.

    Returns
    -------
    majority_ds : xarray.Dataset
        Dataset that produces majority result from 'check_equiv'. Returns None 
        if no majority is found.
    """
    majority_ds = None
    counter = 0

    for ds in datasets:
        if counter == 0:
            majority_ds = ds
            counter += 1
            continue

        if check_equiv(majority_ds, ds, False):
            counter += 1
        else:
            counter -= 1

    # count if majority_ds is actually the majority 
    counter = 0
    for ds in datasets:
        if check_equiv(majority_ds, ds, verbose):
            counter += 1
            
    if counter <= len(datasets) / 2:
        return None

    return majority_ds


def find_different_datasets(datasets: list[xarray.Dataset], check_equiv: Callable, verbose: bool) -> list:
    r"""
    Finds datasets that return a value from 'check_equiv' that is different
    from the majority.

    Parameters
    ----------
    datasets : list[xarray.Dataset]
        List of xarray Datasets to run 'check_equiv' on and compare results for
    check_equiv : Callable
        Function to run using datasets in 'datasets' as input.
    verbose : bool
        Whether or not to print full output.

    Returns
    -------
    different_datasets : list[xarray.Dataset]
        List of datasets that are different from the majority result from 'check_equiv'
    """
    # Find the datasets that are different from the majority dataset
    # It will return [-1] if no majority dataset is found
    majority_ds = find_majority_ds(datasets, check_equiv, verbose)
    if majority_ds is None:
        return [None]

    different_datasets = []
    for ds in datasets:
        if not check_equiv(majority_ds, ds, False):
            different_datasets.append(ds)

    return different_datasets


def get_filename(ds: xarray.Dataset) -> str:
    """
    Gets file name associated with the given xarray Dataset.

    Parameters
    ----------
    dataset : xarray.Dataset
        Dataset to obtain source path from

    Returns
    -------
    filename : str
        File name of netCDF dataset
    """
    return ds.encoding["source"].split("/")[-1]


def get_check_msg(different_datasets: list, check_name: str, msgs: list, checks) -> str: 
    """
    Returns a standardized message for a passed check or a failed check. 

    Parameters
    ----------
    different_datasets: list[xarray.Dataset]
        List of xarray Datasets which failed the check because they were different from the majority. 
        Will be [None] if there was no majority and most Datasets were different from each other. 
    check_name: str
        The name of this check 
    msgs: list[str]
        msgs[0] is what should be said if the check failed. msgs[1] is what should be said if the check passed. 
    checks: Dict[str, bool] [optional, default=None]
        An optional Dictionary that maps the check name to whether or not it passed 
    """ 

    if different_datasets == [None]:
        if checks is not None:
            checks[check_name] = False 
        check_msg = Fore.RED + f"{check_name} failed: {msgs[0]} A majority of them are different from each other.\n" + Style.RESET_ALL
    elif len(different_datasets) == 0:
        if checks is not None:
            checks[check_name] = True 
        check_msg = Fore.GREEN + f"{check_name} passed: {msgs[1]}\n" + Style.RESET_ALL
    else: 
        dataset_names = [get_filename(ds) for ds in different_datasets]
        if checks is not None:
            checks[check_name] = False 
        check_msg = Fore.RED + f"{check_name}: {msgs[0]} The following datasets ({len(different_datasets)}/{different_datasets[0].count}) are different from the majority opinion: " + str(dataset_names) + "\n" + Style.RESET_ALL

    return check_msg

def convert_paths(paths: list[str]) -> list[xarray.Dataset]:
    """
    Converts a list of file paths to a list of xarray Datasets. These paths 
    can be either netCDF files or zarr stores.

    Parameters
    ----------
    paths : list[str]
        List of file paths to convert to xarray Datasets

    Returns
    -------
    datasets : list[xarray.Dataset]
        List of xarray Datasets
    """
    datasets = []
    for path in paths:
        if path.endswith(".nc"):
            datasets.append(xarray.open_dataset(path))
        elif path.endswith(".zarr"):
            datasets.append(xarray.open_zarr(path))
        else:
            raise ValueError(f"File type not supported: {path}")
    return datasets