#!/usr/bin/env python3
__author__  = 'Konstantin Weddige'
__version__ = '0.2'
from argparse import ArgumentParser
import gpxpy
import logging
import datetime

from dwd.client import DWDClient
from util import haversine


logger = logging.getLogger(__name__)


def follow_tour(points, start_time=None):
    last_station = None
    last_point = None
    distance = 0
    duration = datetime.timedelta()
    if not start_time:
        start_time = datetime.datetime.now()
    for point in points:
        if last_point:
            distance += haversine(last_point.latitude, last_point.longitude, point.latitude, point.longitude)
            duration = datetime.timedelta(seconds=int(distance / 60 * 60 * 60))
        last_point = point
        nearest_station = dwd.get_nearest_station(point.latitude, point.longitude)
        if not last_station == nearest_station:
            last_station = nearest_station
            
            time = start_time + duration
            fc_time = min((abs((t-time).total_seconds()), t) for t in nearest_station.forecast)[1]
            fc = nearest_station.forecast[fc_time]
            
            print('{0:.0f}km\t{1}\t{2} ({3:.2f}km)'.format(distance, duration, last_station, last_station.distance(point.latitude, point.longitude)))
            
            #print(fc)
            
            print('\t{0}'.format(fc_time))
            print('\tWind\t\t{0}m/s ({1}°)'.format(fc['FF'], fc['DD']))
            print('\tTemperature\t{0:.1f}°C'.format(float(fc['TTT']) - 272.15))
            print('\tCloud cover\t{0}%'.format(fc['N']))
            print('\tPrecipitation\t{0}l/m²'.format(fc['RR1c']))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--log', default='ERROR')
    parser.add_argument('route', help='GPX file')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log))

    dwd = DWDClient()
    
    if args.refresh:
        dwd.refresh()

    with open(args.route, 'r') as f:
        gpx = gpxpy.parse(f)

    if gpx.routes:
        for route in gpx.routes:
            logger.info('Start route')
            follow_tour(route.points)
    else:
        for track in gpx.tracks:
            for segment in track.segments:
                logger.info('Start segment')
                follow_tour(segment.points)
