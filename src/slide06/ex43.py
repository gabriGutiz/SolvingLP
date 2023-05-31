
from pulp import *
import pandas as pd
import numpy as np
from collections import defaultdict

def main() -> None:
    prob = LpProblem("FordProblem", LpMinimize)

    df = pd.read_csv("./ex43.csv", delimiter=',')

    df = df.set_index("Plant")

    plants_aux = list(df.index)

    dics = defaultdict(str)
    for col in list(df.columns):
        dics[col] = dict(zip(plants_aux, df[col]))

    plants = []

    for var in list(df.index):
        plants.append(f'Taurus_{var}')
        plants.append(f'Lincoln_{var}')
        plants.append(f'Escort_{var}')

    vars = LpVariable.dicts("Plant", plants, cat=LpInteger)
    vars_aux = LpVariable.dicts("Plant", plants_aux, cat=LpBinary)

    prob += lpSum([
        vars[i]*(
            dics['CostTaurus'][i] +
            dics['CostLincoln'][i] +
            dics['CostEscort'][i]
            ) for i in vars_aux
        ].extend([
            
        ]))

    print(plants)
    print(dics)

if __name__ == '__main__':
    main()
