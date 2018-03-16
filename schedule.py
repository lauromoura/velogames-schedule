#!/usr/bin/env python

'''Script to fetch the startlist for each race'''

import sys
import csv
import logging
import argparse
import os.path
import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
BASE_URL = 'https://procyclingstats.com/race/{0}/2018/startlist'


def get_filename(race):
    return '{0}.html'.format(race)

def get_url(race):
    return BASE_URL.format(race)


def download(race):
    filename = get_filename(race)
    url = get_url(race)

    r = requests.get(url)
    r.raise_for_status()
    with open(filename, 'w', encoding=r.encoding) as output:
        output.write(r.text)

    with open('update-time.txt', 'w') as datefile:
        timezone = pytz.timezone('America/Recife')
        dt = datetime.datetime.now(timezone)
        datefile.write(dt.strftime("%d %B %Y - %H:%M %Z"))


def process_files(races, source):
    return sum([process_file(race, source) for race in races], []) # Flatten


def process_file(race, source):
    '''Returns a list of dictionaries with the startlist for the given race.'''
    logging.debug('Processing race %s. Target source: %s', race, source)
    filename = get_filename(race)

    if (source == 'download') or not os.path.isfile(filename):
        logging.warning('File %s not found. Trying to download it.', filename)
        download(race)

    data = []

    with open(filename) as handle:
        html_data = handle.read()

    soup = BeautifulSoup(html_data, 'html.parser')

    table = soup.find_all('div', class_='div760l')[0]
    teams = table.find_all('div')
    for team in teams:
        if team['style'] == 'clear: both; ':
            continue

        team, *riders = team.find_all('a')
        team = normalize('NFC', team.get_text())
        for rider in riders:
            surname, name = rider.strings
            surname = [x.strip().capitalize() for x in surname.split()]
            name = [x for x in name.split()]
            name = normalize('NFC', ' '.join(name + surname))

            data.append({'race': race, 'name': name, 'team': team})


    return data

def main():
    fieldnames = ['race', 'name', 'team']

    parser = argparse.ArgumentParser(description='Parse schedule data')
    parser.add_argument('source', help='download or local', nargs='?',
            choices=('download', 'local'), default='local')

    args = parser.parse_args()
    data = process_files(RACES, args.source)

    with open('races.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)



if __name__ == '__main__':
    main()
