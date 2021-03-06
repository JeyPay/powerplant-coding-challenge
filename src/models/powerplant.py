
class PowerPlant:
    type: str
    efficiency: float
    cost_per_mw: float = 0.0
    name: str
    pmin: int
    pmax: int
    # Will be calculated during the processing
    p: int = 0

    def __init__(self, type_pp, efficiency, name, pmin, pmax):
        self.type = type_pp
        self.efficiency = efficiency
        self.name = name
        self.pmin = pmin
        self.pmax = pmax

    def __str__(self):
        return (f'{self.name}: \n\ttype: {self.type} \n\tefficiency: {self.efficiency} \n\tpmin: {self.pmin} \n\tpmax: {self.pmax} \n\tp: {self.p} \n\tcost_per_mw: {self.cost_per_mw}')

    def __iter__(self):
        for key in ['name', 'p']:
            yield (key, '{}'.format(getattr(self, key)))