from collections import defaultdict
from .config import getParamAsFloat, getParamAsInt
from .core import BestAirObject
from .table_manager import TableManager

# _cache = {}
#
# def cached(func):
#     """
#     Simple decorator to cache results keyed on method args.
#     """
#     def wrapper(*args, **kwargs):
#         # convert kwargs dict, which is unhashable, to tuple of pairs
#         key = (func.__name__, args, tuple(kwargs.items()))
#
#         try:
#             return _cache[key]
#         except KeyError:
#             _cache[key] = result = func(*args, **kwargs)
#             return result
#
#     return wrapper

class Model(BestAirObject):
    def __init__(self):
        self.table_mgr = tbl_mgr = TableManager()

        self.TACs = tbl_mgr.get_table('TAC')
        self.TACs.fillna('', inplace=True)

        self.CAPs = tbl_mgr.get_table('CAP')

        self.tac_names = sorted(self.TACs.index)
        self.cap_names = sorted(self.CAPs.index)

        df = tbl_mgr.get_table('counties')
        self.counties = sorted(df['name'])

        df = tbl_mgr.get_table('air-basins')
        self.air_basins = sorted(df['name'])

        df = tbl_mgr.get_table('air-districts')
        self.air_districts = sorted(df['name'])

        df = tbl_mgr.get_table('source-sectors')
        self.source_sectors = [f"{row.category}-{row.subcategory}" for idx, row in df.iterrows()]
        self.source_sector_types = sorted(df.source_type.unique())

        self.source_sectors_dict = d = defaultdict(lambda: defaultdict(list))
        for idx, row in df.iterrows():
            d[row.source_type][row.category].append(row.subcategory)

        self.first_year = getParamAsInt('BEST_AIR.StartYear')
        self.last_year  = getParamAsInt('BEST_AIR.EndYear')
        self.default_discount_rate = getParamAsFloat('BEST_AIR.UserDiscountRate')

