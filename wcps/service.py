"""
Execute a WCPS query on a WCPS server, and save/return the result.
"""
from __future__ import annotations

import requests
from requests.auth import HTTPBasicAuth

from wcps.model import WCPSExpr

DEFAULT_CONN_TIMEOUT = 10
"""Default timeout to establish a connection to the WCPS service: 10 seconds."""
DEFAULT_READ_TIMEOUT = 10 * 60
"""Default timeout to wait for a query to execute: 10 minutes."""


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
                conn_timeout: int = DEFAULT_CONN_TIMEOUT,
                read_timeout: int = DEFAULT_READ_TIMEOUT,
                output_file: str = None) -> requests.Response:
        """
        Sends a WCPS query to the service.

        :param wcps_query: the WCPS query to be executed on the server.
        :param conn_timeout: how long (seconds) to wait for the connection to be established
        :param read_timeout: how long (seconds) to wait for the query to execute
        :param output_file: an optional path where the response will be written to.
        :return: the response object from evaluating the query.
        """
        if isinstance(wcps_query, WCPSExpr):
            wcps_query = str(wcps_query)

        url = self.endpoint_wcps + wcps_query
        stream = bool(output_file)

        response = requests.get(url,
                                auth=self.auth,
                                timeout=(conn_timeout, read_timeout),
                                stream=stream)
        response.raise_for_status()

        if output_file is not None:
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        return response
