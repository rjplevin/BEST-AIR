from glob import glob
import pandas as pd
from os import path

datadir = '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/'

parts = [path for path in glob(datadir + 'part*')]
csvs = [path for path in glob(datadir + 'part*/*.csv')]

datadict = {}
for pathname in csvs:
    print(f"Reading '{pathname}'")
    df = pd.read_csv(pathname, index_col=None)
    basename = path.basename(pathname)
    part = pathname.split('/')[-2]
    fileroot = path.splitext(basename)[0]
    key = (fileroot, part)
    datadict[key] = df

basenames = {pair[0] for pair in datadict.keys()}
parts = sorted({pair[1] for pair in datadict.keys()})

print("Combining parts...")
data = {}
for basename in basenames:
    df_parts = [datadict[(basename, part)] for part in parts]
    data[basename] = pd.concat(df_parts, axis='rows')

for name, df in data.items():
    path = f"{datadir}combined/{name}.csv.gz"
    print(f"Writing {path}, shape: {df.shape}")
    df.to_csv(path, index=None)

# Example run:
#
# /Volumes/Plevin1TB/Software/anaconda3/envs/bestair/bin/python /Users/rjp/repos/BEST-AIR/best_air/bin/example_read_NATA.py
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part2/Ambient Concentration.csv'
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part2/Cancer Risk.csv'
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part2/Exposure Concentration.csv'
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part1/Ambient Concentration.csv'
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part1/Cancer Risk.csv'
# Reading '/Volumes/T7/BEST-AIR/data/ConcExpRisk_tract_poll_CA/part1/Exposure Concentration.csv'
# Combining parts...
# Exposure Concentration:
#   cols: Index(['State', 'EPA Region', 'County', 'FIPS', 'Tract', 'Population',
#        'Pollutant Name', 'Total Exposure Conc',
#        'PT-StationaryPoint Exposure Conc',
#        'OR-LightDuty-OffNetwork-Gas Exposure Conc',
#        'OR-LightDuty-OffNetwork-Diesel Exposure Conc',
#        'OR-HeavyDuty-OffNetwork-Gas Exposure Conc',
#        'OR-HeavyDuty-OffNetwork-Diesel Exposure Conc',
#        'OR-LightDuty-OnNetwork-Gas Exposure Conc',
#        'OR-LightDuty-OnNetwork-Diesel Exposure Conc',
#        'OR-HeavyDuty-OnNetwork-Gas Exposure Conc',
#        'OR-HeavyDuty-OnNetwork-Diesel Exposure Conc',
#        'OR-Refueling Exposure Conc', 'OR-HeavyDuty-Hoteling Exposure Conc',
#        'NR-Recreational-inc-PleasureCraft Exposure Conc',
#        'NR-Construction Exposure Conc',
#        'NR-CommercialLawnGarden Exposure Conc',
#        'NR-ResidentialLawnGarden Exposure Conc',
#        'NR-Agriculture Exposure Conc', 'NR-CommercialEquipment Exposure Conc',
#        'NR-AllOther Exposure Conc', 'NR-CMV_C1C2 Exposure Conc',
#        'NR-CMV_C3 Exposure Conc', 'NR-CMV_C1C2C3_underway Exposure Conc',
#        'NR-Locomotives Exposure Conc', 'NR-Point-Airports Exposure Conc',
#        'NR- Point-Railyards Exposure Conc', 'NP-industrial Exposure Conc',
#        'NP-CommercialCooking Exposure Conc', 'NP-OilGas Exposure Conc',
#        'NP-SolventsCoatings Exposure Conc',
#        'NP-StorageTransfer_BulkTerminals_GasStage1 Exposure Conc',
#        'NP-MiscellaneousNonindustrial Exposure Conc',
#        'NP-FuelCombustion_not_RWC Exposure Conc',
#        'NP-ResidentialWoodCombustionRWC Exposure Conc',
#        'NP-WasteDisposal Exposure Conc', 'NP-AgricultureLivestock Conc',
#        'FIRE Exposure Conc', 'BIOGENICS Exposure Conc',
#        'SECONDARY Exposure Conc', 'BACKGROUND Exposure Conc'],
#       dtype='object')
#   shape: (1414350, 46)
# Ambient Concentration:
#   cols: Index(['State', 'EPA Region', 'County', 'FIPS', 'Tract', 'Population',
#        'Pollutant Name', 'Total Conc', 'PT-StationaryPoint Conc',
#        'OR-LightDuty-OffNetwork-Gas Conc',
#        'OR-LightDuty-OffNetwork-Diesel Conc',
#        'OR-HeavyDuty-OffNetwork-Gas Conc',
#        'OR-HeavyDuty-OffNetwork-Diesel Conc',
#        'OR-LightDuty-OnNetwork-Gas Conc', 'OR-LightDuty-OnNetwork-Diesel Conc',
#        'OR-HeavyDuty-OnNetwork-Gas Conc', 'OR-HeavyDuty-OnNetwork-Diesel Conc',
#        'OR-Refueling Conc', 'OR-HeavyDuty-Hoteling Conc',
#        'NR-Recreational-inc-PleasureCraft Conc', 'NR-Construction Conc',
#        'NR-CommercialLawnGarden Conc', 'NR-ResidentialLawnGarden Conc',
#        'NR-Agriculture Conc', 'NR-CommercialEquipment Conc',
#        'NR-AllOther Conc', 'NR-CMV_C1C2 Conc', 'NR-CMV_C3 Conc',
#        'NR-CMV_C1C2C3_underway Conc', 'NR-Locomotives Conc',
#        'NR-Point-Airports Conc', 'NR- Point-Railyards Conc',
#        'NP-industrial Conc', 'NP-CommercialCooking Conc', 'NP-OilGas Conc',
#        'NP-SolventsCoatings Conc',
#        'NP-StorageTransfer_BulkTerminals_GasStage1 Conc',
#        'NP-MiscellaneousNonindustrial Conc', 'NP-FuelCombustion_not_RWC Conc',
#        'NP-ResidentialWoodCombustionRWC Conc', 'NP-WasteDisposal Conc',
#        'NP-AgricultureLivestock Conc', 'FIRE Conc', 'BIOGENICS Conc',
#        'SECONDARY Conc', 'BACKGROUND Conc'],
#       dtype='object')
#   shape: (1414350, 46)
# Cancer Risk:
#   cols: Index(['State', 'EPA Region', 'County', 'FIPS', 'Tract', 'Population',
#        'Pollutant Name', 'Total Cancer Risk (per million)',
#        'PT-StationaryPoint Cancer Risk (per million)',
#        'OR-LightDuty-OffNetwork-Gas Cancer Risk (per million)',
#        'OR-LightDuty-OffNetwork-Diesel Cancer Risk (per million)',
#        'OR-HeavyDuty-OffNetwork-Gas Cancer Risk (per million)',
#        'OR-HeavyDuty-OffNetwork-Diesel Cancer Risk (per million)',
#        'OR-LightDuty-OnNetwork-Gas Cancer Risk (per million)',
#        'OR-LightDuty-OnNetwork-Diesel Cancer Risk (per million)',
#        'OR-HeavyDuty-OnNetwork-Gas Cancer Risk (per million)',
#        'OR-HeavyDuty-OnNetwork-Diesel Cancer Risk (per million)',
#        'OR-Refueling Cancer Risk (per million)',
#        'OR-HeavyDuty-Hoteling Cancer Risk (per million)',
#        'NR-Recreational-inc-PleasureCraft Cancer Risk (per million)',
#        'NR-Construction Cancer Risk (per million)',
#        'NR-CommercialLawnGarden Cancer Risk (per million)',
#        'NR-ResidentialLawnGarden Cancer Risk (per million)',
#        'NR-Agriculture Cancer Risk (per million)',
#        'NR-CommercialEquipment Cancer Risk (per million)',
#        'NR-AllOther Cancer Risk (per million)',
#        'NR-CMV_C1C2 Cancer Risk (per million)',
#        'NR-CMV_C3 Cancer Risk (per million)',
#        'NR-CMV_C1C2C3_underway Cancer Risk (per million)',
#        'NR-Locomotives Cancer Risk (per million)',
#        'NR-Point-Airports Cancer Risk (per million)',
#        'NR- Point-Railyards Cancer Risk (per million)',
#        'NP-industrial Cancer Risk (per million)',
#        'NP-CommercialCooking Cancer Risk (per million)',
#        'NP-OilGas Cancer Risk (per million)',
#        'NP-SolventsCoatings Cancer Risk (per million)',
#        'NP-StorageTransfer_BulkTerminals_GasStage1 Cancer Risk',
#        'NP-MiscellaneousNonindustrial Cancer Risk (per million)',
#        'NP-FuelCombustion_not_RWC Cancer Risk (per million)',
#        'NP-ResidentialWoodCombustionRWC Cancer Risk (per million)',
#        'NP-WasteDisposal Cancer Risk (per million)',
#        'NP-AgricultureLivestock Cancer Risk (per million)',
#        'FIRE Cancer Risk (per million)', 'BIOGENICS Cancer Risk (per million)',
#        'SECONDARY Cancer Risk (per million)',
#        'BACKGROUND Cancer Risk (per million)', 'Total Respiratory HI',
#        'Total Neurological HI', 'Total Liver HI', 'Total Developmental HI',
#        'Total Reproductive HI', 'Total Kidney HI', 'Total Ocular HI',
#        'Total Endocrine HI', 'Total Hematological HI',
#        'Total Immunological HI', 'Total Skeletal HI', 'Total Spleen HI',
#        'Total Thyroid HI', 'Total Wholebody HI'],
#       dtype='object')
#   shape: (1414350, 60)
#
# Process finished with exit code 0
