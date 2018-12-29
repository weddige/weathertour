from util import haversine

class Station:
    def __init__(self, station_id, elevation, lat, lon, name, country):
        self.id = station_id
        self.elevation = elevation
        self.lon = lon
        self.lat = lat
        self.name = name
        self.country = country

    def __str__(self):
        return '{0}: {1}'.format(self.id, self.name)

    def distance(self, lat, lon):
        return haversine(lat, lon, self.lat, self.lon)
