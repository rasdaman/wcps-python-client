"""
Execute a WCPS query on a WCPS server, and save/return the result.
"""
from __future__ import annotations

import io
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Union

import numpy as np
import requests
from PIL import Image
import netCDF4 as nc
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from wcps.model import WCPSExpr, WCPSClientException

DEFAULT_CONN_TIMEOUT = 10
"""Default timeout to establish a connection to the WCPS service: 10 seconds."""
DEFAULT_READ_TIMEOUT = 10 * 60
"""Default timeout to wait for a query to execute: 10 minutes."""


class WCPSResultType(StrEnum):
    """A list of possible WCPS result types."""
    SCALAR = 'scalar'
    """A scalar value such as 1, 1.55, etc."""
    MULTIBAND_SCALAR = 'multiband_scalar'
    """A multiband scalar value is a list of multiple numbers, e.g. [1, 2, 3]"""
    JSON = 'json'
    """A JSON list"""
    ARRAY = 'array'
    """An array, either encoded to a data format such as TIFF, PNG, netCDF, or as a numpy object."""


@dataclass
class WCPSResult:
    """
    Encapsulates a result from executing a WCPS query.
    """
    value: any
    """The result value: a scalar or list of scalars, a JSON list, or an array (encoded or numpy)."""
    type: WCPSResultType
    """The result type."""


class Service:
    """
    Establish a connection to a WCPS service, send queries and retrieve results.

    :param endpoint: the WCPS server endpoint URL, e.g. https://ows.rasdaman.org/rasdaman/ows
    :param username: optional username for basic authentication to the WCPS server
    :param password: optional password for basic authentication to the WCPS server

    Example usage: ::

        service = Service("https://ows.rasdaman.org/rasdaman/ows")
        query = Datacube("NIR").encode("PNG")

        # save the response to a file output.png
        service.query(query, output_file='output.png')
        # or get the response object back
        response = service.query(query)
    """

    def __init__(self, endpoint, username=None, password=None):
        self.endpoint = endpoint
        self.endpoint_wcps = endpoint + '?service=WCS&version=2.0.1&request=ProcessCoverages&query='
        self.auth = HTTPBasicAuth(username, password) if username and password else None

    def execute(self,
                wcps_query: str | WCPSExpr,
                convert_to_numpy: bool = False,
                conn_timeout: int = DEFAULT_CONN_TIMEOUT,
                read_timeout: int = DEFAULT_READ_TIMEOUT) -> WCPSResult:
        """
        Sends a WCPS query to the service. Depending on the result, it returns:

        - A single number (int or float) if the result was a single scalar value
        - A list of numbers (int or float) if the result was a multiband scalar value
        - A JSON array object if the result was a JSON array (the query did encode to "JSON")
        - A string if the result was a CSV array (the query did encode to "CSV")
        - A bytes object if the result was a binary data format, such as TIFF, netCDF, PNG.

        :param wcps_query: the WCPS query to be executed on the server.
        :param convert_to_numpy: if True an *array* result encoded to a data format
            will be automatically converted to a numpy array.
        :param conn_timeout: how long (seconds) to wait for the connection to be established
        :param read_timeout: how long (seconds) to wait for the query to execute
        :return: the response object from evaluating the query.

        :raise: :exc:`wcps.model.WCPSClientException` if the server returns an error status code.
        """
        response = self.execute_raw(wcps_query, conn_timeout, read_timeout)
        return self.response_to_wcps_result(response, convert_to_numpy=convert_to_numpy)

    def download(self,
                 wcps_query: str | WCPSExpr,
                 output_file: str,
                 conn_timeout: int = DEFAULT_CONN_TIMEOUT,
                 read_timeout: int = DEFAULT_READ_TIMEOUT):
        """
        Sends a WCPS query to the service and save the response into an ``output_file``.

        :param wcps_query: the WCPS query to be executed on the server.
        :param output_file: a path where the response will be written to.
        :param conn_timeout: how long (seconds) to wait for the connection to be established
        :param read_timeout: how long (seconds) to wait for the query to execute
        :return: the response object from evaluating the query.

        :raise: :exc:`wcps.model.WCPSClientException` if the server returns an error status code.
        """
        with open(output_file, 'wb') as file:
            response = self.execute_raw(wcps_query, conn_timeout, read_timeout, stream=True)
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def execute_raw(self,
                    wcps_query: str | WCPSExpr,
                    conn_timeout: int = DEFAULT_CONN_TIMEOUT,
                    read_timeout: int = DEFAULT_READ_TIMEOUT,
                    stream: bool = False) -> requests.Response:
        """
        Sends a WCPS query to the service and return the raw :class:`requests.Response` object.

        The :meth:`execute` and :meth:`download` are more user-friendly methods that return
        the response properly interpreted or download to a file.

        :param wcps_query: the WCPS query to be executed on the server.
        :param conn_timeout: how long (seconds) to wait for the connection to be established
        :param read_timeout: how long (seconds) to wait for the query to execute
        :param stream: allow streaming the query result so it can be downloaded in chunks

        :return: the response object from evaluating the query.

        :raise: :exc:`wcps.model.WCPSClientException` if the server returns an error status code.
        """
        # prepare request parameters
        if isinstance(wcps_query, WCPSExpr):
            wcps_query = str(wcps_query)
        url = self.endpoint_wcps + wcps_query

        # make request
        response = requests.get(url,
                                auth=self.auth,
                                timeout=(conn_timeout, read_timeout),
                                stream=stream)

        # check for errors from the server
        try:
            response.raise_for_status()
        except HTTPError as ex:
            err = self._parse_error_xml(response.text)
            if err is not None:
                raise WCPSClientException(err) from ex
            raise ex

        return response

    def response_to_wcps_result(self,
                                response: requests.Response,
                                convert_to_numpy: bool = False) -> WCPSResult:
        """
        Converts a :class:`requests.Response` into a :class:`WCPSResult`.

        :param response: the response to be converted.
        :param convert_to_numpy: if True an *array* result encoded to a data format
            will be automatically converted to a numpy array.
        :return: a :class:`WCPSResult` with the :attr:`WCPSResult.type` set to the
            response type, and the :attr:`WCPSResult.value` set to the response value.
        """
        content_type = response.headers.get('Content-Type', '')

        # json array
        if 'application/json' in content_type:
            return WCPSResult(value=response.json(), type=WCPSResultType.JSON)

        # single or multiband scalar
        if content_type == '' or 'text/plain' in content_type:
            content = response.text

            # single band
            if '{' not in content:
                return WCPSResult(value=self._parse_scalar(content), type=WCPSResultType.SCALAR)

            # multiband
            content = content.replace('{', '').replace('}', '')
            scalars = [self._parse_scalar(band) for band in content.split(',')]
            if len(scalars) > 1:
                return WCPSResult(value=scalars, type=WCPSResultType.MULTIBAND_SCALAR)

            return WCPSResult(value=scalars[0], type=WCPSResultType.SCALAR)

        # array
        if convert_to_numpy:

            # 2D image formats
            if 'image/' in content_type:
                image = Image.open(io.BytesIO(response.content))
                return WCPSResult(value=np.array(image), type=WCPSResultType.ARRAY)

            # netcdf
            if 'application/netcdf' in content_type:
                with nc.Dataset("memory", mode="r", memory=response.content) as dataset:

                    data_arrays = []
                    for var_name, variable in dataset.variables.items():
                        if var_name in dataset.dimensions:
                            continue
                        ndim = variable.ndim
                        data_arrays.append(variable[:])

                    # Stack all arrays along a new dimension
                    return WCPSResult(value=np.stack(data_arrays, axis=ndim),
                                      type=WCPSResultType.ARRAY)

            # unsupported format
            raise WCPSClientException(f"Cannot convert content-type {content_type} "
                                      f"to a numpy array object.")

        # no conversion to numpy
        return WCPSResult(value=response.content, type=WCPSResultType.ARRAY)

    @staticmethod
    def _parse_scalar(value: str) -> Union[int | float | bool]:
        """
        Parse a string into a correctly typed number / bool value.
        :param value: a number in string format
        :return: a number or boolean value.
        :meta private:
        """
        value = value.strip()
        # Attempt to parse as a boolean
        if value in ('t', 'f'):
            return value == 't'

        # Attempt to parse as an integer
        try:
            return int(value)
        except ValueError:
            pass

        # Attempt to parse as a float
        try:
            return float(value)
        except ValueError:
            pass

        raise WCPSClientException(f"Failed parsing text response to a scalar number/bool value: '{value}'")

    @staticmethod
    def _parse_error_xml(xml_str: Optional[str | bytes]) -> Optional[str]:
        """
        Parse an ows:ExceptionReport returned by the WCPS server to extract the
        ows:ExceptionText elements for a human-readable error.
        :param xml_str: the error as a string/bytes; may be None.
        :return: the extracted error message, or None if xml_str is None
        :meta private:
        """
        if xml_str is None:
            return None
        try:
            namespaces = {'ows': 'http://www.opengis.net/ows/2.0'}
            root = ET.fromstring(xml_str)
            exceptions = root.findall('.//ows:Exception', namespaces)
            ret = []
            for ex in exceptions:
                err = ''
                ex_code = ex.get('exceptionCode')
                if ex_code is not None:
                    err = ex_code + ': '
                exception_texts = ex.findall('.//ows:ExceptionText', namespaces)
                for ex_text in exception_texts:
                    err += ex_text.text
                ret.append(err)
            return '\n'.join(ret)
        except ET.ParseError:
            return xml_str
