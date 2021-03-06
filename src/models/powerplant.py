
class PowerPlant:
    """This class represent a powerplant"""

    # The type of powerplant (windturbine, gasfired, turbojet)
    type: str
    # The efficiency represented with a number between 0 and 1
    efficiency: float
    # The cost in euro to produce 1 MWh
    cost_per_mwh: float = 0.0
    # The name of the powerplant
    name: str
    # The minimum amount of MWh that the powerplant can produce (before efficiency calculus)
    pmin: int
    # The maximum amount of MWh that the powerplant can produce (before efficiency calculus)
    pmax: int
    # The power the powerplant has to produce to reach the load goal
    p: float = 0.0
    # The cost of the co2 emission based on 'p', co2 ton/MWh and price per ton
    co2_cost: float = 0.0

    def __init__(self, type_pp, efficiency, name, pmin, pmax):
        self.type = type_pp
        self.efficiency = efficiency
        self.name = name
        self.pmin = pmin
        self.pmax = pmax

    def __str__(self):
        return (f'{self.name}: \n\ttype: {self.type} \n\tefficiency: {self.efficiency} \n\tpmin: {self.pmin} \n\tpmax: {self.pmax} \n\tp: {self.p} \n\tco2_cost: {self.co2_cost}')

    def __iter__(self):
        for key in ['name', 'p', 'co2_cost']:
            yield (key, '{}'.format(getattr(self, key)))