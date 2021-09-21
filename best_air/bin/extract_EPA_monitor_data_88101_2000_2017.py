import csv
import pandas as pd

CALIFORNIA = 6  # State Code to keep

data_dir = '/Volumes/T7/Box Sync/BEST-AIR/Data/AQ Monitoring/EPA Criteria Pollutants/PM Daily Data/'

pathname = data_dir + '2017/daily_88101_2017.csv'

# Create 'Monitor ID' = State Code + County Code + Site Num + Parameter Code
# Drop rows with 'Sample Duration' of '24-HR BLK AVG' (redundant)
# Calculate quarterly average of daily means.
# Calculate annual average of four quarterly averages.
# Parameter code is always 88101; name is always 'PM2.5 - Local Conditions'
cols_to_keep = [
    'State Code',
    'County Code',
    'Site Num',
    'Parameter Code',
    'POC',
    'Latitude',
    'Longitude',
    'Sample Duration',
    'Date Local',
    'Event Type',  # ['None', 'Included', 'Excluded']
    'Method Code',  # decide which to keep
    # 'Method Name',
    'Observation Count',
    'Observation Percent',
    'Arithmetic Mean',

    # 'Datum',            # all are in ['WGS84', 'NAD83']
    # 'Units of Measure', # all are 'Micrograms/cubic meter (LC)'
]

def verify_excludes_have_matching_includes(df):
    df = df.copy()
    df.columns = [name.replace(' ', '') for name in df.columns]
    excl = df.query("EventType == 'Excluded'")

    count = 0
    for idx, row in excl.iterrows():
        id = row.monitor_id
        date = row.DateLocal
        poc = row.POC
        found = df.query("EventType == 'Included' and SampleDuration == '1 HOUR' and monitor_id == @id and POC == @poc and DateLocal == @date")
        count += len(found)

        if len(found) > 1:
            print("Multiple matches: \n", found)

    if count != len(excl):
        raise Exception(f"Found {count} Included matches for {len(excl)} Excluded")

def extract(input_path, output_path):
    print(f"Reading '{input_path}'")
    df = pd.read_csv(input_path, index_col=None, usecols=cols_to_keep)

    mask = (df['State Code'] == CALIFORNIA) & (df['Sample Duration'] != '24-HR BLK AVG')
    df = df[mask].copy()

    # Create fixed width monitor ID from these four numeric columns
    df['monitor_id'] = (df['State Code'].astype(str).str.zfill(2) + '-' +
                        df['County Code'].astype(str).str.zfill(3) + '-' +
                        df['Site Num'].astype(str).str.zfill(4) + '-' +
                        df['Parameter Code'].astype(str).str.zfill(5))

    cols_to_drop = ['Parameter Code', 'State Code']
    df.drop(cols_to_drop, axis='columns', inplace=True)

    verify_excludes_have_matching_includes(df)

    rows_to_keep = (df['Event Type'] != 'Excluded')
    df = df[rows_to_keep]

    print(f"Saving extracted data {df.shape} to '{output_path}'")
    df.to_csv(output_path, index=None, quoting=csv.QUOTE_NONNUMERIC)

for year in (2000, 2017):
    input_path  = data_dir + f"{year}/daily_88101_{year}.csv.gz"
    output_path = data_dir + f"extracted_monitor_data_88101_{year}.csv"
    extract(input_path, output_path)
