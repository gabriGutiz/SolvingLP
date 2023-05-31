"""
Problem:
One investor wants to decide on how to invest his money
based on 8 investiments as shown on the follow table.

Investiment          |  01  |  02  |  03  |  04  |  05  |  06  |  07  |  08  |
------------------------------------------------------------------------------
Payment ($ thousand) |  14  |  26  |  35  |  25  |  20  |  15  |  40  |  30  |
Return ($ thousand)  |  20  |  35  |  50  |  40  |  30  |  25  |  70  |  50  |
Risk                 |  01  |  02  |  03  |  04  |  02  |  04  |  05  |  05  |
Time (year)          |  10  |  05  |  06  |  03  |  05  |  01  |  02  |  02  |

Risk: 1=low, 5=high
Total investiment: $100,000

Constraints:
1. At least 2 investiments must have time of at least 4 years;
2. At most 2 investiments can have high risk (at least 4); 
3. If the investiment 5 is choosen, then the investiment 6 must be choosen;
"""

from pulp import *
import pandas as pd
import numpy as np
from collections import defaultdict


def main() -> None:
    prob = LpProblem("InvestimentProblem", LpMaximize)

    df = pd.read_csv("./ex01.csv", delimiter=',')

    new = df['Investiment'].str.split(' ', expand=True)
    df['Investiment'] = new[0]
    df = df.set_index('Investiment').transpose()

    investiments = list(df.index)

    dics = defaultdict(str)
    for col in list(df.columns):
        dics[col] = dict(zip(investiments, df[col]))

    vars = LpVariable.dicts("Investiment", investiments, cat=LpBinary)

    # Objective Function
    prob += lpSum([dics['Return'][i]*vars[i] for i in investiments])

    # Budget constraint
    prob += lpSum([vars[i]*dics['Payment'][i] for i in investiments]) <= 100, 'Budget'

    # Constraint 1
    prob += lpSum([vars[i] if dics['Time'][i] >= 4 else 0 for i in investiments]) >= 2, 'HighTime'

    # Constraint 2
    prob += lpSum([vars[i] if dics['Risk'][i] >= 4 else 0 for i in investiments]) >= 2, 'LowRisk'

    # Constraint 3
    prob += vars['5'] <= vars['6'], '5and6Investiment'

    print(prob)

    prob.solve()

    for var in prob.variables():
        print(f'VAR {var.name} - VAL={var.value()}')

if __name__ == '__main__':
    main()
