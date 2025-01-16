"""
Test the wcps.service module.
"""

from hashlib import sha256

import requests

from wcps.model import Datacube
from wcps.service import Service


def get_checksum(response: requests.Response):
    hash_func = sha256()
    hash_func.update(response.content)
    return hash_func.hexdigest()


def test_service():
    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    response = service.execute('for $c in (NIR) return encode($c, "PNG")')
    expected = 'a71c63b3d24ecc065609395358348e23ce3eb546dc3e3d5f98c714901beda27d'
    assert get_checksum(response) == expected

    query = Datacube("NIR").encode("PNG")
    response = service.execute(query)
    assert get_checksum(response) == expected
