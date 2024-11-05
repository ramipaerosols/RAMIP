import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import itertools
from utils import get_filename

def show_single(ds: xr.Dataset, verbose: bool=False):
    """
    Given a single dataset, this function prints out several plots that show different aspects of the dataset. 

    Plot 1: A line plot of timeseries data averaged over all spatial dimensions. Other dimensions, such as 
        "member" are plotted as separate lines. If there are multiple other dimensions, then their combinations are plotted.
    Plot 2: Instead of a line plot, a heat map is generated using the same specifications as #1. 
    Plot 3: A map of the mean of all dimensions other than latitude and longitude for the entire time period.
    Plot 3.5 (Optional): If lev or level is a spatial dimension, then a map of the mean over all dimensions other
        than lev/level. 
    Plot 4: A map of the mean of all dimensions other than latitude and longitude for the first timestep.
    Plot 5: A map of the mean of all dimensions other than latitude and longitude for the last timestep.
    """

    path = get_filename(ds)

    if verbose:
        print("Checking single zarr store: ", path)
        print(ds) 
        print("\n\n")
        print(ds.info())
        print("\n\n")

    data_vars = []
    for var in ds.data_vars:
        # we want to ignore all data variables that are actually bounds
        if 'bnds' not in ds[var].dims:
            data_vars.append(ds[var])

    if len(data_vars) > 1: 
        print("More than one valid data variable in zarr store")
        return 
    
    data = data_vars[0]

    # TASK 1
    if verbose: 
        print(data)
        print()

    possible_spatial_dims = ["lat", "lon", "lev", "latitude", "longitude", "level"]
    spatial_dims = [dim for dim in possible_spatial_dims if dim in data.dims]
    other_dimensions = [dim for dim in data.dims if dim not in spatial_dims and dim != 'time']

    # latitudinal weighting for task 1 and task 2 
    if 'lat' in spatial_dims:
        weights = np.cos(np.deg2rad(data.lat))
    if 'latitude' in spatial_dims:
        weights = np.cos(np.deg2rad(data.latitude))
    weights.name = "weights"
    data_weighted = data.weighted(weights)


    # Take the mean over the spatial dimensions and plot each combination of the other_dimensions as a line with the x-axis being "time"
    if len(other_dimensions) > 1:
        # We need to group our dataarray so it has one singular new dimension that has all combinations of the other_dimensions
        data_ = data.stack(new_dim=other_dimensions)
        data_ = data_.rename({'new_dim': str(tuple(other_dimensions))})
        data_ = data_.weighted(weights)
        data_.mean(dim=spatial_dims).plot.line(x='time')
    elif len(other_dimensions) == 1:
        data_weighted.mean(dim=spatial_dims).plot.line(x='time', hue=other_dimensions[0])
    else:
        data_weighted.mean(dim=spatial_dims).plot()

    plt.suptitle(f"Mean over spatial dimensions")
    plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
    plt.show()

    # TASK 2
    if len(other_dimensions) > 1:
        new_dim_name = str(tuple(other_dimensions))
        data_ = data.stack(new_dim=other_dimensions, create_index=False)
        data_ = data_.rename({'new_dim': new_dim_name})
        all_coord_names = [data[dim].values for dim in other_dimensions]
        combination_coord_labels = [tuple(str(x) for x in combo) for combo in itertools.product(*all_coord_names)]
        data_ = data_.weighted(weights)
        data_.mean(dim=spatial_dims).plot.pcolormesh(x='time', y=new_dim_name)
        plt.yticks(ticks=range(len(combination_coord_labels)), labels=combination_coord_labels)
    elif len(other_dimensions) == 1:
        data_weighted.mean(dim=spatial_dims).plot.pcolormesh(x='time', y=other_dimensions[0])
    else:
        print("Not enough dimensions for a color mesh plot.")
        # data.mean(dim=spatial_dims).plot.pcolormesh()

    if len(other_dimensions) >= 1:
        plt.suptitle(f"Mean over spatial dimensions")
        plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
        plt.show()

    # TASK 3
    other_dimensions = other_dimensions + ['time']
    if 'lev' in spatial_dims:
        other_dimensions += ['lev']
    elif 'level' in spatial_dims:
        other_dimensions += ['level']
    data.mean(dim=other_dimensions).plot()
    plt.suptitle(f"Mean over entire time period and all other dimensions")
    plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
    plt.show()

    # TASK 3.5
    if 'lev' in spatial_dims or 'level' in spatial_dims:
        other_dims = [dim for dim in data.dims if dim != 'lev' and dim != 'level']
        data.mean(dim=other_dims).plot.line(y='lev')
        plt.suptitle(f"Mean over every dimension except lev")
        plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
        plt.show()

    # TASK 4
    other_dimensions.remove('time')
    data.isel(time=0).mean(dim=other_dimensions).plot()
    plt.suptitle(f"First timestep, mean over all other dimensions ")
    plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
    plt.show() 

    # TASK 5
    data.isel(time=-1).mean(dim=other_dimensions).plot()
    plt.suptitle(f"Last timestep, mean over all other dimensions")
    plt.figtext(0.5, 0, f"Plot generated for {path}", horizontalalignment='center', fontsize=7) 
    plt.show() 
