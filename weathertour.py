#!/usr/bin/env python3
__author__  = 'Konstantin Weddige'
__version__ = '0.1'
from argparse import ArgumentParser
import gpxpy
import logging
import datetime

from dwd.client import DWDClient
from util import haversine

def follow_tour(points, time=None):
    last_station = None
    last_point = None
    distance = 0
    duration = datetime.timedelta()
    if not time:
        time = datetime.datetime.now()
    for point in points:
        if last_point:
            distance += haversine(last_point.latitude, last_point.longitude, point.latitude, point.longitude)
            duration = datetime.timedelta(seconds=int(distance / 60 * 60 * 60))
        last_point = point
        nearest_station = dwd.get_nearest_station(point.latitude, point.longitude)
        if not last_station == nearest_station:
            last_station = nearest_station
            time += duration
            print('{0:.0f}km\t{1}\t{2} ({3:.2f}km)'.format(distance, duration, last_station, last_station.distance(point.latitude, point.longitude)))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--log', default='ERROR')
    parser.add_argument('route', help='GPX file')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log))

    dwd = DWDClient()

    with open(args.route, 'r') as f:
        gpx = gpxpy.parse(f)

    if gpx.routes:
        for route in gpx.routes:
            logging.info('Start route')
            follow_tour(route.points)
    else:
        for track in gpx.tracks:
            for segment in track.segments:
                logging.info('Start segment')
                follow_tour(segment.points)
