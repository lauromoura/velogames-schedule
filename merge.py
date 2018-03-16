# coding: utf-8

#!/usr/bin/env python

import pandas as pd

races = pd.read_csv('races.csv')
riders = pd.read_csv('riders.csv')

def is_in_race(race):
    def func(x):
        # FIXME +700 calls, getting 2 full bool index on the larger races table...
        return not races[(races['name'] == x['name']) & (races['race'] == race)].empty
    return func

RACES = [
    'milano-sanremo',
    'e3-harelbeke',
    'gent-wevelgem',
    'dwars-door-vlaanderen',
    'ronde-van-vlaanderen',
    'scheldeprijs',
    'paris-roubaix',
    'de-brabantse-pijl',
    'amstel-gold-race',
    'la-fleche-wallone',
    'liege-bastogne-liege',
]

for race in RACES:
    riders[race] = riders.apply(is_in_race(race), axis=1)

(riders*1).to_csv('table.csv', index_label='name')

