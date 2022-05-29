from base64 import b64encode
from hmac import digest
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from time import time
from dotenv import load_dotenv
from os import getenv
from urllib.parse import quote

class OAuth:
    """
    Used to implement the 1.0 OAuth flow specifically for Twitter
    """
    _OAUTH_VERSION = '1.0'
    _OAUTH_SIGANTURE_METHOD = 'HMAC-SHA1'
    _oauth_token = ''
    _oauth_token_secret = ''
    _oauth_consumer_key = ''
    _oauth_consumer_secret = ''
    _http_method = ''
    _url = ''
    _data = {}

    def __init__(self, method, url, data) -> None:
        load_dotenv
        self._oauth_consumer_key = getenv('OAUTH_CONSUMER_KEY')
        self._oauth_consumer_secret = getenv('OAUTH_CONSUMER_SECRET')
        self._oauth_token = getenv('OAUTH_TOKEN')
        self._oauth_token_secret = getenv('OAUTH_TOKEN_SECRET')
        self._http_method = method
        self._url = url
        self._data = data

    def createAuthorizationString(self) -> str:
        """Create an OAUTH 1.0 Authorization string"""
        params = {
            'oauth_consumer_key': self._oauth_consumer_key,
            'oauth_nonce': self._generateNonce(),
            'oauth_signature_method': self._OAUTH_SIGANTURE_METHOD,
            'oauth_timestamp': self._generateTimeStamp(),
            'oauth_token': self._oauth_token,
            'oauth_version': self._OAUTH_VERSION,
        }

        params_string = self._generateParamsString(params)
        signature = self._generateSignature(params_string)
        signing_key = self._generateSigningKey()

        byte_signature = signature.encode('utf-8')
        byte_key = signing_key.encode('utf-8')

        hashed_signature = digest(byte_key, byte_signature, 'sha1')
        params['oauth_signature'] = b64encode(hashed_signature).decode('utf-8')
        
        auth_string = 'OAuth '
        for i in sorted(params):
            auth_string += quote(i) + '="' + quote(params[i]) + '", '

        return auth_string.rstrip(', ')

    def _generateParamsString(self, params: dict) -> str:
        """
        Generate a params string which used in the process of genrating the OAuth signature
        @param dict `params`
        """
        if 'oauth_signature' in params:
            del params['oauth_signature']

        full_params = {**self._data, **params}

        encoded_params = {}
        for i in full_params:
            encoded_params[quote(i)] = quote(full_params[i])

        sorted_params =  {}
        for j in sorted(encoded_params):
            sorted_params[j] = encoded_params[j]

        params_string = ''
        for k in sorted_params:
            params_string += k + '=' + sorted_params[k] + '&'

        return params_string.rstrip('&')

    def _generateNonce(self) -> str:
        """
        Generates a random 36 character string to be used as an OAuth nonce
        """
        return ''.join(choice(ascii_uppercase + digits + ascii_lowercase) for _ in range(36))

    def _generateSignature(self, params_string) -> str:
        """
        Generates a signature string
        @param string `params_string`
        """
        signature = self._http_method.upper() + '&'
        signature += quote(self._url) + '&'
        signature += quote(params_string)
        return signature

    def _generateTimeStamp(self) -> str:
        """
        Generates a unix timestamp
        """
        # Convert to int first to remove floating point 
        # Then convert to string as will be concatenated with other strings
        return str(int(time()))

    def _generateSigningKey(self) -> str:
        """
        Generate a key used to sign the params string when encrypting
        """
        encoded_consumer_secret = quote(self._oauth_consumer_secret)
        encoded_token_secret = quote(self._oauth_token_secret)
        return encoded_consumer_secret + '&' + encoded_token_secret
