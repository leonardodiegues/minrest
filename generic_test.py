from grest.grest import GenericClient

API_URL = 'http://google.com/api/v2/'
ENDPOINTS = [
    'search',
    'pipiroom-local',
    'threads',
    'videos',
    'findWithExample',
    'find'
]

gc = GenericClient(API_URL, ENDPOINTS)
print(gc.endpoint_methods)