import re
import zipfile
import datetime
import urllib.request
import os.path
import logging
import lxml.etree
import pyrfc3339

from dwd.station import Station


logger = logging.getLogger(__name__)


class DWDClient:
    def __init__(self, source_url='https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_S_LATEST_240.kmz'):
        self._stations = []
        self._source_url = source_url
        self._data_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self._data_path = os.path.join(self._data_dir, 'MOSMIX.kmz')

    def refresh(self):
        logger.info('Retrieve data...')
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)
        urllib.request.urlretrieve(self._source_url, self._data_path)

    @property
    def stations(self):
        if not self._stations:
            logger.info('Load stations...')
            if not os.path.exists(self._data_path):
                self.refresh()
            with zipfile.ZipFile(self._data_path, 'r') as kmz_file:
                filename = kmz_file.namelist()[0]
                with kmz_file.open(filename) as kml_file:
                    kml = lxml.etree.parse(kml_file)

            node = kml.getroot().find('{http://www.opengis.net/kml/2.2}Document')
            node = node.find('{http://www.opengis.net/kml/2.2}ExtendedData')
            node = node.find(
                '{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}ProductDefinition'
            )
            node = node.find(
                '{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}ForecastTimeSteps'
            )

            times = [pyrfc3339.parse(i.text) for i in node]

            document = kml.getroot().find('{http://www.opengis.net/kml/2.2}Document')
            nodes = document.findall('{http://www.opengis.net/kml/2.2}Placemark')

            self._stations = [Station(node, times) for node in nodes]
        else:
            logger.debug('Use cached stations...')
        return self._stations

    def get_nearest_station(self, lat, lon):
        return min(self.stations, key=lambda station: station.distance(lat, lon))
