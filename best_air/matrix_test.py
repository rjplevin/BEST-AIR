# Notes
# apply a function on all data variables in a Dataset
# Dataset.map()

# Tips on vectorization here:
# http://xarray.pydata.org/en/stable/examples/apply_ufunc_vectorize_1d.html
#
# Note use of numba to compile some functions.
# https://numba.pydata.org/numba-doc/latest/user/5minguide.html
# https://tedboy.github.io/pandas/enhancingperf/enhancingperf2.html
#
# Also, dask
# https://towardsdatascience.com/how-i-learned-to-love-parallelized-applies-with-python-pandas-dask-and-numba-f06b0b367138
#
import numpy as np
import xarray as xr
from numba import njit
import timeit

num_pollutants = 25
num_grid_cells = 2000
num_src_sectors = 30

pollutants  = [f"Pol{n}" for n in range(num_pollutants)]
src_sectors = [f"X{n}" for n in range(num_src_sectors)]
grid_cells  = list(range(num_grid_cells))

SRC_SECTOR = 'src_sector'
POLLUTANT = 'pollutant'
GRID_CELL = 'grid_cell'

SRC_GRID_CELL = 'src_grid_cell'
DST_GRID_CELL = 'dst_grid_cell'

# Size is 12MB for data1.values
data1 = xr.DataArray(np.random.randn(num_pollutants, num_src_sectors, num_grid_cells),
                     dims=(POLLUTANT, SRC_SECTOR, GRID_CELL),
                     coords={POLLUTANT: pollutants,
                             SRC_SECTOR: src_sectors,
                             GRID_CELL: grid_cells})

data1.attrs["long_name"] = "some meaningful name"
data1.attrs["units"] = "kg"
data1.attrs["description"] = "Mass rate of pollutant incident on grid cell"

# any other attributes we want to store
data1.attrs["data_source"] = 'CARB whatever'

# Size is 32MB for the fraction.values
fraction = xr.DataArray(np.random.randn(num_grid_cells, num_grid_cells),
                        dims=(SRC_GRID_CELL, DST_GRID_CELL),
                        coords={SRC_GRID_CELL: grid_cells,
                                DST_GRID_CELL: grid_cells})

distance = xr.DataArray(np.random.randn(num_grid_cells, num_grid_cells),
                        dims=(SRC_GRID_CELL, DST_GRID_CELL),
                        coords={SRC_GRID_CELL: grid_cells,
                                DST_GRID_CELL: grid_cells}) * 1000
distance = abs(distance)

# 25.6 sec with @njit, sec without
@njit
def compute(distance, fraction, output):
    for sector in range(num_src_sectors):
        for pollutant in range(num_pollutants):
            for src in range(num_grid_cells):
                for dst in range(num_grid_cells):
                    output[pollutant, sector, dst] = distance[src, dst] * fraction[src, dst]

# def tester():
#     data2 = data1 + 100
#     data3 = data2 * 2
#
# result = timeit.timeit(tester, number=1000)

output = xr.DataArray(np.zeros((num_pollutants, num_src_sectors, num_grid_cells), dtype=float),
                      dims=(POLLUTANT, SRC_SECTOR, GRID_CELL),
                      coords={POLLUTANT: pollutants,
                              SRC_SECTOR: src_sectors,
                              GRID_CELL: grid_cells})

def tester():
    compute(distance.data, fraction.data, output.data)

# first, trigger the compilation
#tester()

# Without numba, time: 1309.42 = 22 min; with numba, 2.63 seconds.
result = timeit.timeit(tester, number=1)

print(f"Time: {result:.2f}")

def total1(df):
    total = df.sum(axis='columns').sum()
    return total

def total2(df):
    total = df.values.sum()
    return total


def other_test():
    import pandas as pd

    df = pd.DataFrame(data=1.234, columns=[f"col{n}" for n in range(20)], index=[f"row{n}" for n in range(100)])
    matrix = df.values

    secs = timeit.timeit(lambda: total1(df), number=1000)
    print(f"Total1 takes {secs} sec")

    secs = timeit.timeit(lambda: total2(df), number=1000)
    print(f"Total2 takes {secs} sec")

other_test()
