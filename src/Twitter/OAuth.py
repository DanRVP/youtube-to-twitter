from hashlib import sha1
import hmac
import random
import string
import time
from dotenv import load_dotenv
import os
import urllib.parse

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

    def __init__(self, method, url) -> None:
        load_dotenv
        self._oauth_consumer_key = os.getenv('OAUTH_CONSUMER_KEY')
        self._oauth_consumer_secret = os.getenv('OAUTH_CONSUMER_SECRET')
        self._oauth_token = os.getenv('OAUTH_TOKEN')
        self._oauth_token_secret = os.getenv('OAUTH_TOKEN_SECRET')
        self._http_method = method
        self._url = url

    def createAuthorizationString(self) -> str:
        """Create an OAUTH 1.0 Authorization string"""
        params = {
            'oauth_consumer_key': self._oauth_consumer_key,
            'oauth_nonce': self._generateNonce(),
            'oauth_signature': '',
            'oauth_signature_method': self._OAUTH_SIGANTURE_METHOD,
            'oauth_timestamp': self._generateTimeStamp(),
            'oauth_token': self._oauth_token,
            'oauth_version': self._OAUTH_VERSION,
        }

        params_string = self._generateParamsString(params)
        unencoded_signature = self._generateSignature(params_string)
        signing_key = self._generateSigningKey()
        hashed_signature = hmac.new(bytes(signing_key), bytes(unencoded_signature), sha1)
        params['oauth_signature'] = hashed_signature.digest().encode("base64").rstrip('\n')
        
        auth_string = 'OAuth '
        for i in params:
            auth_string += urllib.parse.quote(i) + '="' + urllib.parse.quote(params[i]) + '",'

        return auth_string.rstrip(',')


    def _generateParamsString(params: dict) -> str:
        """
        Generate a params string which used in the process of genrating the OAuth signature
        @param dict `params`
        """
        if 'oauth_signature' in params:
            del params['oauth_signature']

        full_params = {{'include_entities':'true'} | params}

        encoded_params = {}
        for i in full_params:
            encoded_params[urllib.parse.quote(i)] = urllib.parse.quote(full_params[i])

        sorted_params =  {}
        for j in sorted(encoded_params):
            sorted_params[j] = encoded_params[j]

        params_string = ''
        for k in sorted_params:
            params_string += k + '=' + sorted_params[k] + '&'

        return params_string.rstrip('&')

    def _generateNonce():
        """
        Generates a random 36 character string to be used as an OAuth nonce
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(36))

    def _generateSignature(self, params_string):
        """
        Generates a signature string to be SHA-1 hashed
        @param string `params_string`
        """
        signature = self._http_method.upper() + '&'
        signature += urllib.parse.quote(self._url) + '&'
        signature += urllib.parse.quote(params_string)
        return signature

    def _generateTimeStamp():
        """
        Generates a unix timestamp
        """
        return int(time.time())

    def _generateSigningKey(self):
        """
        Generate a key used to sign the params string when SHA-1 encrypting
        """
        encoded_consumer_secret = urllib.parse.quote(self._oauth_consumer_secret)
        encoded_token_secret = urllib.parse.quote(self._oauth_token_secret)
        return encoded_consumer_secret + encoded_token_secret
