#!/usr/bin/env python

'''Velogames classic riders schedule'''

import sys
import csv
import logging
import argparse
import os.path
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup


URL = 'https://www.velogames.com/spring-classics/2018/riders.php'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def download(url, filename):
    '''Downloads url to filename'''
    r = requests.get(url)
    r.raise_for_status()
    with open(filename, 'w', encoding=r.encoding) as output:
        output.write(r.text)


def main():

    filename = 'riders.php'

    parser = argparse.ArgumentParser(description='Parse rider data')
    parser.add_argument('source', help='download or local', nargs='?',
                        choices=('download', 'local'), default='local')

    args = parser.parse_args()
    source = args.source

    if source == 'download' or not os.path.isfile(filename):
        download(URL, filename)

    with open(filename) as handle:
        html_data = handle.read()

    soup = BeautifulSoup(html_data, 'html.parser')

    table = soup.find('table')
    data = []
    fieldnames = ['name', 'team', 'points', 'cost']
    for tr in table.find_all('tr')[1:]: #[1:] to skip the header
        cells = tr.find_all('td')
        name = cells[1].get_text()
        team = cells[2].get_text()
        points = int(cells[3].get_text() or '0')
        cost = int(cells[4].get_text() or '0')
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
