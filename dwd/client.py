import re

from dwd.station import Station


class DWDClient:
    def __init__(self, base_url='https://opendata.dwd.de/'):
        self._stations = []

    @property
    def stations(self):
        if not self._stations:
            with open('data/RR_Monatswerte_Beschreibung_Stationen.txt', 'r', encoding='latin-1') as f:
                for line in f.readlines()[2:]:
                    parts = re.split('\s+', line, 6)
                    name, bundesland = parts[6].rsplit(maxsplit=1)
                    name = name.strip()
                    self._stations.append(Station(parts[0], float(parts[3]), float(parts[4]), float(parts[5]), name, bundesland))
        return self._stations

    def get_nearest_station(self, lat, lon):
        return min(self.stations, key=lambda station: station.distance(lat, lon))
