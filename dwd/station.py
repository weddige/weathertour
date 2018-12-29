from util import haversine

class Station:
    def __init__(self, node, times):
        self.id = node.findtext('{http://www.opengis.net/kml/2.2}name')
        self.name = node.findtext('{http://www.opengis.net/kml/2.2}description')
        
        self._forecast = node.findall('{http://www.opengis.net/kml/2.2}ExtendedData/{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}Forecast')
        self._times = times
            
        coordinates = node.findtext('{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates')
        lon, lat, alt = coordinates.split(',')
        
        self.elevation = float(alt)
        self.lon = float(lon)
        self.lat = float(lat)

        #self.country = country
        
    def __str__(self):
        return '{0}: {1}'.format(self.id, self.name)

    def distance(self, lat, lon):
        return haversine(lat, lon, self.lat, self.lon)
    
    @property
    def forecast(self):
        fc = {}
        for i in self._forecast:
            key = i.get('{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}elementName')
            values = i.findtext('{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}value').split()
            fc[key] = values
        
        return dict(zip(self._times, map(lambda i: dict(zip(fc.keys(), i)), zip(*fc.values()))))