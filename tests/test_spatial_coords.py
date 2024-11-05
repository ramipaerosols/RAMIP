import xarray as xr
import numpy as np
from colorama import Fore, Style
from utils import find_different_datasets, get_consensus_check_msg, get_filename


def check_spatial_coords(ds1: xr.Dataset, ds2: xr.Dataset, verbose=False):
    possible_spatial_dims = ["lat", "lon", "lev", "latitude", "longitude", "level"]
    spatial_dims_1 = [dim for dim in possible_spatial_dims if dim in ds1.dims]
    spatial_dims_2 = [dim for dim in possible_spatial_dims if dim in ds2.dims]

    if spatial_dims_1 != spatial_dims_2:
        if verbose: 
            print("Spatial dims are not the same")
        return False
    
    # Check that the spatial dims have the same shape
    for dim in spatial_dims_1:
        if ds1[dim].shape != ds2[dim].shape:
            if verbose: 
                print("Spatial dims do not have the same shape")
            return False
        
    # Check that the spatial dims have the same values
    for dim in spatial_dims_1:
        if not np.array_equal(ds1[dim].values, ds2[dim].values):
            if verbose: 
                print(Fore.CYAN + f"Spatial Coordinates Err Output: ")
                print(f"Comparing {get_filename(ds1)} and {get_filename(ds2)}")
                print(f"The {dim} dimension does not have the same values. (It's possible that more dimensions also do not have the same values.) Here are the first 10 values that are different: "  + Style.RESET_ALL)
                for index in np.where(ds1[dim].values != ds2[dim].values)[0][:10]:
                    print(f"{ds1[dim].values[index]} != {ds2[dim].values[index]} (index {index})")
                print()
            return False
        
    return True


def test_spatial_coords(datasets: list, verbose = False, checks = None) -> str:
    different_datasets = find_different_datasets(datasets, check_spatial_coords, verbose)
    msgs = ["Spatial coordinates are not equivalent across all datasets.", 
            "Spatial coordinates are equivalent across all datasets."]
    return get_consensus_check_msg(different_datasets, "Spatial Coord Check", msgs, checks, len(datasets))

