"""Class for making HTTP requests."""
from typing import Dict
import requests


class RequestService():
    """Class for making HTTP requests.

    Methods
    -------
    make_get_request(
            method: str,
            endpoint: str,
            params: Dict[str, str] = None) -> requests.Response:
        Makes HTTP request using the given parameters.
    """

    @staticmethod
    def make_get_request(
            endpoint: str, params: Dict[str, str] = None) -> requests.Response:
        """Makes HTTP request using given arguments and returns response.

        Returns
        -------
        requests.Response
            The request's response object.
        """
        if params:
            return requests.get(endpoint, params)
        return requests.get(endpoint)
