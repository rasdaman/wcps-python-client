"""
Test the wcps.service module.
"""

from hashlib import sha256

import pytest
import requests

from wcps.model import Datacube, AxisIter, Condense, CondenseOp
from wcps.service import Service, WCPSResultType


def get_checksum(response: bytes):
    hash_func = sha256()
    hash_func.update(response)
    return hash_func.hexdigest()


def make_text_response(text: str, content_type: str = 'text/plain') -> requests.Response:
    """
    Build a canned :class:`requests.Response` with the given text body, without any
    network access, so that only the result parsing can be tested.
    """
    response = requests.Response()
    response.status_code = 200
    response.headers['Content-Type'] = content_type
    response._content = text.encode('utf-8')
    return response


def test_execute_raw():
    service = Service("https://ows.rasdaman.org/rasdaman/ows")

    response = service.execute_raw('for $c in (NIR) return encode($c, "PNG")')
    expected = '1b547e175f5fbca3742771ab5216fa2f043eb2c3a51f5eb6c7a3b4d22adbbe79'
    assert get_checksum(response.content) == expected

    query = Datacube("NIR").encode("PNG")
    response = service.execute_raw(query)
    assert get_checksum(response.content) == expected

    query = Datacube("NIR").sum()
    response = service.execute_raw(query)
    assert response.text == '{ 269047963, 205047787, 195546065 }'

    query = Datacube("NIR")["i":0:2, "j":0:2].red.encode("json")
    response = service.execute_raw(query)
    assert response.text == '[\n [104,101],\n [103,103]\n]'

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
               .where(cov["ansi": ansi_iter.ref()].Red.avg() > 20)
               .using(cov["ansi": ansi_iter.ref()]))
    query = max_map.encode("PNG")
    result = service.execute(query)
    assert result.type == WCPSResultType.IMAGE

    result = service.execute('for $c in (NIR) return encode($c, "PNG")')
    expected = '1b547e175f5fbca3742771ab5216fa2f043eb2c3a51f5eb6c7a3b4d22adbbe79'
    assert result.type == WCPSResultType.IMAGE
    assert get_checksum(result.value) == expected

    query = Datacube("NIR")["i":0:2, "j":0:2].red.encode("json")
    result = service.execute(query)
    assert result.type == WCPSResultType.JSON
    assert result.value == [[104, 101], [103, 103]]

    query = Datacube("NIR").encode("PNG")
    result = service.execute(query, convert_to_numpy=True)
    assert result.type == WCPSResultType.NUMPY
    assert result.value.shape == (1076, 1916, 3)

    query = Datacube("NIR").encode("application/netcdf")
    result = service.execute(query, convert_to_numpy=True)
    assert result.type == WCPSResultType.NUMPY
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
    expected = '1b547e175f5fbca3742771ab5216fa2f043eb2c3a51f5eb6c7a3b4d22adbbe79'
    assert get_checksum(temp_file_path.read_bytes()) == expected

    service.download('for $c in (NIR) return encode($c + 1, "PNG")', str(temp_file_path))
    expected = '9ba23169475814e4b8dfb444319062370a5fd11f7bfefbfab469daa2ef437a54'
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

def test_execute_null_multiband_scalar():
    """
    A query such as::

        for $c in (mean_summer_airtemp)
        return {
          extended_point: extend($c[Lat(-35:-25), Lon(120:140)], {Lat(-40:-20), Lon(115:145)})[Lat(-38), Lon(117)],
          original_point: extend($c[Lat(-35:-25), Lon(120:140)], {Lat(-40:-20), Lon(115:145)})[Lat(-30), Lon(130)]
        }

    returns the text ``{ NULL, 0 }`` when one of the bands evaluates to NULL.
    The parser must not raise and must convert NULL to None.
    """
    service = Service("https://ows.rasdaman.org/rasdaman/ows")
    response = make_text_response('{ NULL, 0 }')
    result = service.response_to_wcps_result(response)
    assert result.type == WCPSResultType.MULTIBAND_SCALAR
    assert result.value == [None, 0]


def test_execute_null_scalar():
    """A single-band result of NULL must parse to None."""
    service = Service("https://ows.rasdaman.org/rasdaman/ows")
    response = make_text_response('NULL')
    result = service.response_to_wcps_result(response)
    assert result.type == WCPSResultType.SCALAR
    assert result.value is None


def test_execute_domain_result():
    """
    A query such as::

        for $c in (mean_summer_airtemp)
        return domain($c)

    returns a spatial domain such as
    ``Lat(-44.524999999999987:-8.974999999999987),Lon(111.975:156.27500000000000886)``.
    The parser must not raise and must return the raw text as a TEXT result.
    """
    service = Service("https://ows.rasdaman.org/rasdaman/ows")
    domain_text = 'Lat(-44.524999999999987:-8.974999999999987),Lon(111.975:156.27500000000000886)'
    response = make_text_response(domain_text)
    result = service.response_to_wcps_result(response)
    assert result.type == WCPSResultType.TEXT
    assert result.value == domain_text


def test_execute_unparseable_multiband_result():
    """A multiband text result with non-scalar bands must fall back to raw TEXT."""
    service = Service("https://ows.rasdaman.org/rasdaman/ows")
    domain_text = 'Lat(-44.524999999999987:-8.974999999999987),Lon(111.975:156.27500000000000886)'
    response = make_text_response('{ ' + domain_text + ' }')
    result = service.response_to_wcps_result(response)
    assert result.type == WCPSResultType.TEXT
    assert result.value == '{ ' + domain_text + ' }'


def test_list_udfs():
    service = Service("https://ows.rasdaman.org/rasdaman/ows")
    result = service.list_udfs()
    assert result is not None
    ok = 'Stddev_pop' in result
    assert ok

# def test_list_udfs_none():
#     service = Service("http://localhost:8080/rasdaman/ows")
#     result = service.list_udfs()
#     assert result is None
