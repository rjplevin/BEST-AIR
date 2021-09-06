import csv
import pyodbc

# Note: had to install Access ODBC driver from https://www.microsoft.com/en-US/download/details.aspx?id=13255
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
PWD = ''

for part in ('part1', 'part2'):
    print(f"Processing {part}")
    MDB = f't:/tmp/ConcExpRisk_tract_poll_CA_{part}.mdb'

    connect_str = f'DRIVER={DRV};DBQ={MDB};'
    con = pyodbc.connect(connect_str)
    cur = con.cursor()

    tables = [name for (path, _, name, ttype, _) in cur.tables() if ttype == 'TABLE']

    for table in tables:
        print(f"Reading table '{table}'")
        query = f'SELECT * FROM "{table}";'
        rows = cur.execute(query).fetchall()
        colnames = [x[0] for x in cur.description]
        # cur.close()

        prefix = table.split('(')[0].strip()  # use the part before the first parenthesis only
        pathname = f't:/tmp/{part}/{prefix}.csv'
        print(f"Writing '{pathname}'")
        with open(pathname, 'w') as f:
            writer = csv.writer(f)      # default field-delimiter is ","
            writer.writerow(colnames)
            writer.writerows(rows)

    cur.close()
    con.close()

print("Done")
