"""
Test the wcps.service module.
"""

from hashlib import sha256

import pytest

from wcps.model import Datacube, AxisIter, Condense, CondenseOp
from wcps.service import Service, WCPSResultType


def get_checksum(response: bytes):
    hash_func = sha256()
    hash_func.update(response)
    return hash_func.hexdigest()


def test_execute_raw():
    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    response = service.execute_raw('for $c in (NIR) return encode($c, "PNG")')
    expected = 'a71c63b3d24ecc065609395358348e23ce3eb546dc3e3d5f98c714901beda27d'
    assert get_checksum(response.content) == expected

    query = Datacube("NIR").encode("PNG")
    response = service.execute_raw(query)
    assert get_checksum(response.content) == expected

    query = Datacube("NIR").sum()
    response = service.execute_raw(query)
    assert response.text == '{ 269047963, 205047787, 195546065 }'

    query = Datacube("NIR")["i":0:2, "j":0:2].red.encode("json")
    response = service.execute_raw(query)
    assert response.text == '[[104,101],[103,103]]'

    query = (Datacube("NIR").red > 5).all()
    response = service.execute_raw(query)
    assert response.text == 'f'

    query = (Datacube("NIR").red > 5).some()
    response = service.execute_raw(query)
    assert response.text == 't'


def test_execute():
    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    cov = Datacube("AvgTemperatureColorScaled")
    ansi_iter = (AxisIter("ansi_iter", "ansi")
                 .of_geo_axis(cov["ansi" : "2015-01-01" : "2015-07-01"]))
    max_map = (Condense(CondenseOp.MAX)
               .over(ansi_iter)
               .where(cov["ansi": ansi_iter.ref()].avg() > 20)
               .using(cov["ansi": ansi_iter.ref()]))
    query = max_map.encode("PNG")
    result = service.execute(query)
    assert result.type == WCPSResultType.ARRAY

    result = service.execute('for $c in (NIR) return encode($c, "PNG")')
    expected = 'a71c63b3d24ecc065609395358348e23ce3eb546dc3e3d5f98c714901beda27d'
    assert result.type == WCPSResultType.ARRAY
    assert get_checksum(result.value) == expected

    query = Datacube("NIR")["i":0:2, "j":0:2].red.encode("json")
    result = service.execute(query)
    assert result.type == WCPSResultType.JSON
    assert result.value == [[104, 101], [103, 103]]

    query = Datacube("NIR").encode("PNG")
    result = service.execute(query, convert_to_numpy=True)
    assert result.type == WCPSResultType.ARRAY
    assert result.value.shape == (1076, 1916, 3)

    query = Datacube("NIR").encode("application/netcdf")
    result = service.execute(query, convert_to_numpy=True)
    assert result.type == WCPSResultType.ARRAY
    assert result.value.shape == (1916, 1076, 3)

    query = Datacube("NIR").sum()
    result = service.execute(query)
    assert result.type == WCPSResultType.MULTIBAND_SCALAR
    assert result.value == [269047963, 205047787, 195546065]

    query = Datacube("NIR").red.sum()
    result = service.execute(query)
    assert result.type == WCPSResultType.SCALAR
    assert result.value == 269047963

    query = (Datacube("NIR").red > 5).all()
    result = service.execute(query)
    assert result.type == WCPSResultType.SCALAR
    assert result.value is False

    query = (Datacube("NIR").red > 5).some()
    result = service.execute(query)
    assert result.type == WCPSResultType.SCALAR
    assert result.value is True


def test_download(tmp_path):
    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    temp_file_path = tmp_path / "temp_file.png"
    service.download('for $c in (NIR) return encode($c, "PNG")', str(temp_file_path))
    expected = 'a71c63b3d24ecc065609395358348e23ce3eb546dc3e3d5f98c714901beda27d'
    assert get_checksum(temp_file_path.read_bytes()) == expected


def test_execute_error():
    cov = Datacube("S2_L2A")["time", "2025-01-15"]
    # NDVI formula
    ndvi = (cov.nir - cov.red) / (cov.nir + cov.red)
    # threshold NDVI values to highlight areas with high vegetation
    vegetation = ndvi > 0.5
    # encode final result to PNG
    query = vegetation.encode("PNG")

    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    # execute the query on the server and get back the response
    with pytest.raises(Exception) as e_info:
        service.execute(query)
        assert e_info.value == "NoSuchCoverage: Coverage 'S2_L2A' does not exist."
