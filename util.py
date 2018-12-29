import math

RADIUS = 6371

def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2) - math.radians(lat1)
    dlon = math.radians(lon2) - math.radians(lon1)
    d = math.sin(dlat * 0.5)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon * 0.5)**2
    return 2 * RADIUS * math.asin(math.sqrt(d))
