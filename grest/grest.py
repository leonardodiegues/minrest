"""Main module."""
import re
import inspect
import requests
from urllib.parse import urljoin

from grest import parser

def _make_method_name(name):
    return name.replace('-', '_').title().replace('_', '')


class GenericClient(object):

    auth = None
    method_index = {}

    def __init__(self, api_url, endpoints):
        assert any([isinstance(endpoints, str), isinstance(endpoints, list)])
        self.api_url = api_url
        self._endpoints = endpoints
        self.__make_endpoint_methods()

    def __raw_endpoint(self, method_name):
        if isinstance(self._endpoints, list):
            return self._endpoints[self.method_index[method_name]]
        return self._endpoints

    def __request(self, **kwargs):
        [code_context] = inspect.stack()[1][4]
        regexp = re.compile(r"\.(.*?)\(")
        method_name = regexp.search(code_context).group(1)
        endpoint = self.__raw_endpoint(method_name)
        url = urljoin(self.api_url, endpoint)
        return requests.Request(**kwargs)

    def __make_endpoint_methods(self):
        if isinstance(self._endpoints, list):
            for index, endpoint in enumerate(self._endpoints):
                method_name = _make_method_name(endpoint) + "Method"
                self.method_index.update({method_name: index})
                setattr(self.__class__, method_name, self.__request)
        else:
            method_name = _make_method_name(self._endpoints) + "Method"
            self.method_index.update({method_name: 1})
            setattr(self.__class__, method_name, self.__request)

    @property
    def endpoints(self):
        return self.endpoints

    @property
    def methods(self):
        return [x for x in dir(self.__class__) if x.endswith('Method')]