#!/usr/bin/env python

'''Velogames classic riders schedule'''

import sys
import csv

from bs4 import BeautifulSoup
from unicodedata import normalize


def main():
    with open(sys.argv[1]) as handle:
        html_data = handle.read()

    soup = BeautifulSoup(html_data, 'html.parser')


    table = soup.find('table')
    data = []
    fieldnames = ['name', 'team', 'points', 'cost']
    for tr in table.find_all('tr')[1:]: #[1:] to skip the header
        cells = tr.find_all('td')
        name = cells[1].get_text()
        team = cells[2].get_text()
        points = int(cells[4].get_text() or '0')
        cost = int(cells[5].get_text() or '0')
        data.append({
            'name': normalize('NFC', name),
            'team': normalize('NFC', team),
            'points': points,
            'cost': cost
            })

    with open('riders.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rider in data:
            writer.writerow(rider)



if __name__ == '__main__':
    main()
