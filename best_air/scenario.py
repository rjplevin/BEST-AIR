from .core import BestAirObject

class ScenarioTarget(BestAirObject):
    def __init__(self, policy, pollutant, pct_reduction, source, region):
        self.policy = policy                # the policy calling for this reduction
        self.pollutant = pollutant          # the pollutant to reduce
        self.pct_reduction = pct_reduction  # the required percent reduction
        self.source = source                # TBD: the source (sector?)
        self.region = region                # TBD: the region (air basin? county? CT? any of these?)


class Scenario(BestAirObject):
    def __init__(self):
        self.targets = []   # list of ScenarioTargets

