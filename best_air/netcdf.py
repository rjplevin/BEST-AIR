import netCDF4 as nc
import urllib.parse
import urllib.request

# From https://unidata.github.io/netcdf4-python/
# Reading data from a multi-file netCDF dataset
# If you want to read data from a variable that spans multiple netCDF files, you can use the MFDataset class to read the
# data as if it were contained in a single file. Instead of using a single filename to create a Dataset instance, create
# a MFDataset instance with either a list of filenames, or a string with a wildcard (which is then converted to a sorted
# list of files using the python glob module). Variables in the list of files that share the same unlimited dimension are
# aggregated together, and can be sliced across multiple files.
#
# from netCDF4 import MFDataset
# >>> f = MFDataset("mftest*nc")

# https://opensourceoptions.com/blog/netcdf-with-python-netcdf4-metadata-dimensions-and-variables/ useful for introspection

# Potentially useful for downscaling, though we might not need sparse matrix:
# https://stackoverflow.com/questions/36318145/shapefile-to-2d-grid-as-sparse-matrix

# Create mask netcdf data using a shapefile
# https://mygeoblog.com/2019/06/25/mask-netcdf-using-shp-file/

# https://github.com/GeospatialPython/pyshp

# https://www.packtpub.com/product/learning-geospatial-analysis-with-python-third-edition/9781789959277

via_ftp = False


if via_ftp:
    # data_dir = '/Volumes/Plevin1TB/BEST-AIR/data/'
    # filename = data_dir + 'st_4k.ar.v0018..2020.2020001.rf3043_snp20200508.SMOKE4_official.saprc07_14jun2019.nc7'

    filename = 'st_4k.ar.v0018..2020.2020001.rf3043_snp20200508.SMOKE4_official.saprc07_14jun2019.nc7'
    # 'sftp://sftp.arb.ca.gov:11011//ftp/files/aqpsd/outside/LT/2020_modeling/area_point/area/netcdf/st_4k.ar.v0018..2020.2020001.rf3043_snp20200508.SMOKE4_official.saprc07_14jun2019.nc7'
    # 'sftp://aqduser:Cle@nAir@sftp.arb.ca.gov:11011/ftp/files/aqpsd/outside/LT/2020_modeling/area_point/area/netcdfst_4k.ar.v0018..2020.2020001.rf3043_snp20200508.SMOKE4_official.saprc07_14jun2019.nc7'
    username = 'aqquser'
    password = urllib.parse.quote('Cle@nAir') # '@' messes up URL syntax

    # Format is 'ftp://user:password@host:port/path'
    url = f"ftp://{username}:{password}@sftp.arb.ca.gov:11011/ftp/files/aqpsd/outside/LT/2020_modeling/area_point/area/netcdf/" + filename
    # url = f"sftp://{username}:{password}@sftp.arb.ca.gov:11011/outside/LT/2020_modeling/area_point/area/netcdf/" + filename

    print(url)
    # req = urllib.request.Request(url)
    f = urllib.request.urlopen(url)
else:
    f = '/Volumes/T7/BEST-AIR/data/CARB-FTP/st_4k.ar.v0018..2020.2020001.rf3043_snp20200508.SMOKE4_official.saprc07_14jun2019.nc7'

ds = nc.Dataset(f, mode='r')
print(ds)

# print(ds[''])
