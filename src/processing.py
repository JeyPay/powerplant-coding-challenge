import json

from src.models import PowerPlant

def calculate_cost_per_mw(p: PowerPlant, type_to_cost: dict):
    p.cost_per_mw = round(p.efficiency * type_to_cost[p.type], 2)


def loads_wind_pp(wind_pp: list, required_load: float, wind_percentage: int) -> float:
    residual_load = required_load
    for p in wind_pp:
        max_produced = int(p.pmax * p.efficiency * wind_percentage/100)
        if max_produced <= residual_load:
            p.p = max_produced
            residual_load -= max_produced

    return residual_load


def loads_other_pp(other_pp: list, required_load: float) -> None:
    residual_load = required_load
    for p in other_pp:
        if p.pmin > residual_load:
            continue

        max_produced = int(p.pmax * p.efficiency)
        if max_produced <= residual_load:
            p.p = max_produced
            residual_load -= max_produced

        else:
            p.p = residual_load
            residual_load = 0


def compute_loads(powerplants: list, load: int, fuels: dict):
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
            calculate_cost_per_mw(p, type_to_cost)
            other_pp.append(p)

    other_pp.sort(key=lambda x: x.cost_per_mw, reverse=True)

    residual_load = loads_wind_pp(wind_pp, load, int(fuels['wind(%)']))

    loads_other_pp(other_pp, residual_load)


def compute_loads_from_request(data: dict):
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
    with open('example_payloads/payload1.json') as f:
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