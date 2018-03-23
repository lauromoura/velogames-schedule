# coding: utf-8

#!/usr/bin/env python

import csv
import json

with open('races.csv') as csvfile:
    races = list(csv.DictReader(csvfile))
with open('riders.csv') as csvfile:
    riders = list(csv.DictReader(csvfile))

def is_in_race(rider, race):
    if any([schedule['name'] == rider['name'] and schedule['race'] == race for schedule in races]):
        return 1
    else:
        return 0

RACES = [
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

for rider in riders:
    for race in RACES:
        rider[race] = is_in_race(rider, race)

with open('table.json', 'w') as jsonfile:
    json.dump(riders, jsonfile)
