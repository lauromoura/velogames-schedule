#!/usr/bin/env python

'''Velogames classic riders schedule'''

import sys
import csv
import logging
import argparse
import os.path
from unicodedata import normalize
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

CLASSIC = (5, 3, 1)
MINOR_TOUR = (10, 5, 3, 2, 1)

RaceInfo = namedtuple('RaceInfo', ['name', 'points', 'url'])
Result = namedtuple('Result', ['position', 'code', 'name', 'velo_points', 'ranking_points'])

RACES_INFO = [
        RaceInfo('Paris-Nice', MINOR_TOUR, 'https://www.velogames.com/paris-nice/2018/leaguescores.php?league=684737518'),
        RaceInfo('Tirreno-Adriatico', MINOR_TOUR, 'https://www.velogames.com/tirreno-adriatico/2018/leaguescores.php?league=684737518'),
        RaceInfo('MSR', CLASSIC, 'https://www.velogames.com/spring-classics/2018/leaguescores.php?league=684737518&ga=13&st=1'),
        RaceInfo('Volta-A-Catalunya', MINOR_TOUR, 'https://www.velogames.com/volta-a-catalunya/2018/leaguescores.php?league=684737518'),
        RaceInfo('RVV', CLASSIC, 'https://www.velogames.com/spring-classics/2018/leaguescores.php?league=684737518&ga=13&st=5'),
        RaceInfo('Pais-Vasco', MINOR_TOUR, 'https://www.velogames.com/pais-vasco/2018/leaguescores.php?league=684737518'),
        RaceInfo('PR', CLASSIC, 'https://www.velogames.com/spring-classics/2018/leaguescores.php?league=684737518&ga=13&st=7'),
]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def download(url, filename):
    '''Downloads url to filename'''
    r = requests.get(url)
    r.raise_for_status()
    with open(filename, 'w', encoding=r.encoding) as output:
        output.write(r.text)


def main():

    parser = argparse.ArgumentParser(description='Parse rider data')
    parser.add_argument('source', help='download or local', nargs='?',
                        choices=('download', 'local'), default='local')

    args = parser.parse_args()
    source = args.source
    user_data = {}

    for race_i, race in enumerate(RACES_INFO):
        filename = race.name + '.html'
        if source == 'download' or not os.path.isfile(filename):
            download(race.url, filename)

        with open(filename) as handle:
            html_data = handle.read()

        soup = BeautifulSoup(html_data, 'html.parser')

        users_li = soup.select('#users li')
        race_data = []
        for i, user_li in enumerate(users_li):
            pos = i + 1
            points = int(user_li.select('p.born')[0].text.replace(' points', ''))
            code = user_li.select('h3 a')[0]['href'].replace('teamroster.php?tid=', '')
            name = user_li.select('h3 + p.born')[0].text
            ranking_points = race.points[i] if len(race.points) > i else 0
            race_data.append(Result(pos, code, name, points, ranking_points))

            if code not in user_data:
               user_data[code] = (name, [0]*race_i)
            user_data[code][1].append(ranking_points)



        print(race.name, len(race_data))

        with open(race.name + '.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=race_data[0]._fields)
            writer.writeheader()
            for result in race_data:
                writer.writerow(result._asdict())

    for name, value in sorted(user_data.values(), key=lambda x: sum(x[1]), reverse=True):
        print(name, value, sum(value))


if __name__ == '__main__':
    main()

