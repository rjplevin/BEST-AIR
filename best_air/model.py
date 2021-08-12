from .config import getParam, getParamAsFloat, getParamAsInt
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

        # TBD: create a CSV table
        self.emission_sectors = [f"Sector-{n+1}" for n in range(50)]

        self.first_year = getParamAsInt('BEST_AIR.StartYear')
        self.last_year  = getParamAsInt('BEST_AIR.EndYear')
        self.default_discount_rate = getParamAsFloat('BEST_AIR.UserDiscountRate')

