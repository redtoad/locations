
from pygeocoder import Geocoder
from pygeolib import GeocoderError


def address_lookup(addr):
    """
    Fetches geo coordinates for address.

    :param addr: address string
    :returns: latitude and longitude for address
    :rtype: (float, float)
    """
    try:
        result = Geocoder.geocode(addr)
        # Note: coordinates are returned in lon/lat!
        return tuple(reversed(result[0].coordinates))
    except GeocoderError, e:
        return None
