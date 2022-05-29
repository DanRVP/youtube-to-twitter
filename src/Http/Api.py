from src.Http.ResponseObject import Response
import requests

class Api:
    _base_url = ''

    def __init__(self, url) -> None:
        pass

    def get(self, endpoint: str, headers: dict) -> Response:
        """ 
        Sends a get request to the specified endpoint of the Shiptheory API
        :param `endpoint`: Endpoint to hit
        :return `Response`: object
        """
        url = self._base_url + endpoint        
        response = Response()
        res = requests.get(url, headers = headers)
        response.url = res.url
        response.code = res.status_code

        if (response.code != 200):
            response.error = res.json()
            return response
        
        response.body = res.json()
        return response

    def post(self, endpoint: str, data: dict, headers: dict) -> Response:
        """ 
        Sends a post request to the specified endpoint of the Shiptheory API
        :param `endpoint`: Endpoint to hit
        :param `data`: JSON string of data
        :return `Response`: object
        """
        url = self._base_url + endpoint        
        response = Response()
        res = requests.post(url, headers=headers, json=data)
        response.url = res.url
        response.code = res.status_code

        if (response.code != 200):
            response.error = res.json()
            return response
        
        response.body = res.json()
        return response

    def put(self, endpoint: str, data: dict, headers: dict) -> Response:
        """ 
        Sends a put request to the specified endpoint of the Shiptheory API
        :param `endpoint`: Endpoint to hit
        :param `data`: JSON string of data
        :return `Response`: object
        """
        url = self._base_url + endpoint        
        response = Response()
        res = requests.put(url, headers=headers, json=data)
        response.url = res.url
        response.code = res.status_code

        if (response.code != 200):
            response.error = res.json()
            return response
        
        response.body = res.json()
        return response
