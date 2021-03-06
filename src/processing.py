import json

try:
    # When imported from FastApi
    from src.models import PowerPlant
except ImportError:
    # When __main__
    from models import PowerPlant

def calculate_cost_per_mwh(p: PowerPlant, type_to_cost: dict):
    p.cost_per_mwh = round(p.efficiency * type_to_cost[p.type], 2)


def loads_wind_pp(wind_pp: list, required_load: float, wind_percentage: int) -> float:
    """Process the windturbine powerplants

    @required wind_pp: list<PowerPlant>     : a list of the windturbine powerplants
    @required required_loads: float         : the load goal necessary to produce
    @required wind_percentage: int          : wind force in percentage

    Return the residual power load to produce
    """

    residual_load = required_load
    for p in wind_pp:
        max_produced = round(p.pmax * p.efficiency * wind_percentage/100, 1)
        if max_produced <= residual_load:
            p.p = max_produced
            residual_load -= max_produced

    return residual_load


def loads_other_pp(other_pp: list, required_load: float, co2_eur: int) -> None:
    """Process the non-windturbine powerplants

    @required other_pp: list<PowerPlant>    : a list of the non-windturbine powerplants
    @required required_load: float          : the load goal necessary to produce
    @required co2_eur: int                  : cost of co2 in euro/ton
    """

    residual_load = required_load
    for p in other_pp:
        if p.pmin > residual_load:
            continue

        max_produced = round(p.pmax * p.efficiency, 1)
        if max_produced <= residual_load:
            p.p = max_produced
            residual_load -= max_produced

        else:
            p.p = round(residual_load, 1)
            residual_load = 0

        p.co2_cost = round(p.p * 0.3 * co2_eur, 2)


def compute_loads(powerplants: list, load: int, fuels: dict):
    """Process all the powerplants given

    @required powerplants: list<PowerPlant> : a list of all the powerplants available
    @required load: int                     : the load goal necessary to produce
    @required fuels: dict<str, float>       : a dict containing the prices of gas, kerosine and co2 ton as well as wind in percentage
    """

    type_to_cost = {
        "gasfired": float(fuels['gas(euro/MWh)']),
        "turbojet": float(fuels['kerosine(euro/MWh)']),
    }

    wind_pp = []
    other_pp = []
    for p in powerplants:
        if p.type == "windturbine":
            wind_pp.append(p)
        else:
            calculate_cost_per_mwh(p, type_to_cost)
            other_pp.append(p)

    other_pp.sort(key=lambda x: x.cost_per_mwh, reverse=True)
    residual_load = loads_wind_pp(wind_pp, load, round(float(fuels['wind(%)']), 1))
    loads_other_pp(other_pp, residual_load, int(fuels['co2(euro/ton)']))


def compute_loads_from_request(data: dict):
    """This function act as a middlemare between the incoming request (in json) and the computation

    @rqeuired data: dict                    : the incoming dict (json) coming from the POST request

    Return the response Json. The Json is a list of all the powerplants indicating the name, what they have to produce and the co2 cost
    """

    load = int(data['load'])
    fuels = data['fuels']
    powerplants_dict = data['powerplants']

    powerplants = []
    for powerplant in powerplants_dict:
        p = powerplant
        powerplants.append(PowerPlant(p['type'], p['efficiency'], p['name'], p['pmin'], p['pmax']))

    compute_loads(powerplants, load, fuels)

    r = []
    for p in powerplants:
        r.append(dict(p))

    return json.dumps(r)


if __name__ == '__main__':
    """Use only in debug
    """

    with open('example_payloads/payload3.json') as f:
        import json
        data = ''.join(f.readlines())
        data = json.loads(data)

    load = int(data['load'])
    fuels = data['fuels']
    powerplants_dict = data['powerplants']

    powerplants = []
    for powerplant in powerplants_dict:
        p = powerplant
        powerplants.append(PowerPlant(p['type'], p['efficiency'], p['name'], p['pmin'], p['pmax']))

    compute_loads(powerplants, load, fuels)
    for p in powerplants:
        print(p)