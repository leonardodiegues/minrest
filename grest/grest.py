"""Main module."""
import requests
from urllib.parse import urljoin

from grest import parser

def _make_method_name(name):
    return name.replace('-', '_').title().replace('_', '')


class GenericClient(object):

    auth = None
    last_endpoint = None

    def __init__(self, api_url, endpoints):
        assert any([isinstance(endpoints, str), isinstance(endpoints, list)])
        self.api_url = api_url
        self._endpoints = endpoints
        self.__make_endpoint_methods()

    def __request(self, **kwargs):
        url = urljoin(self.api_url, self.last_endpoint)
        return requests.Request(**kwargs)

    def __make_endpoint_methods(self):
        if isinstance(self._endpoints, list):
            for endpoint in self._endpoints:
                setattr(
                    self.__class__,
                    _make_method_name(endpoint) + "Method",
                    classmethod(self.__request)
                )
        else:
            setattr(
                self.__class__,
                _make_method_name(self._endpoints) + "Method",
                classmethod(self.__request)
            )

    @property
    def endpoints(self):
        return self.endpoints

    @property
    def methods(self):
        return [x for x in dir(self.__class__) if x.endswith('Method')]