"""
CONNECT module containing Connect class
"""
import os
import time
import json
import logger

from dotenv import load_dotenv
from mvdam.sdk_handler import sdk_handle


class Connect():
    """
    Connect Class exposing the following methods:
    __init__

    auth

    refresh

    """

    def __init__(self, verb: str, **kwargs: dict):
        """
        Initialise the Asset class

        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped
        """
        self.log = logger.get_logger(__name__)

        self.verb = verb

        load_dotenv()

        self.grant_type = kwargs.get('grant_type')
        self.username = kwargs.get('username') or os.getenv('MVUSERNAME')
        self.password = kwargs.get('password') or os.getenv('MVPASSWORD')
        self.client_id = kwargs.get('client_id') or os.getenv('MVCLIENTID')
        self.client_secret = kwargs.get('client_secret') or os.getenv('MVCLIENTSECRET')
        self.refresh_token = kwargs.get('refresh_token')

        self.sdk_handle = sdk_handle

    def auth(self) -> bool:
        """
        Authorize the user by call with the Connect object.
        """
        if self.grant_type == 'password' or 'refresh_token':

            data = {
                'grant_type': self.grant_type,
                'username': self.username,
                'password': self.password,
                'scope': 'openid api offline_access'
            }

            auth = {
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }

            self.log.debug(auth)

            response = self.sdk_handle.connect.auth(
                data=data,
                auth=auth
                )

            if response.status_code == 200:
                session_file = open('.session', 'w')
                response_json = response.json()

                session_file.write(json.dumps(response_json, default=str))
                self.log.info('Auth successful')
                return True
            else:
                self.log.warning('Auth API response: %s', response.status_code)
                return False

        elif self.grant_type == 'auth-code':
            self.log.warning("Auth-Code flow not yet implemented. Please use password flow.")

    def refresh(self) -> bool:
        """
        Execute the auth GET call with the Connect object.
        """
        data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        response = self.sdk_handle.connect.auth(
            data=data
            )

        if response.status_code == 200:
            session_file = open('.session', 'w')
            response_json = response.json()

            session_expiry = time.time() + response_json['expires_in']
            response_json['expires_at'] = session_expiry
            session_file.write(json.dumps(response_json, default=str))
            self.log.info('Auth API response: %s', {response.status_code})
            return True
        else:
            self.log.info('Auth API response: %s', {response.status_code})
            self.log.debug(response.text)
            return False

    def action(self) -> bool:
        """
        Passthrough function calling the verb required
        """
        self.verb = self.verb.replace("-", "_")
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            return func()
        else:
            self.log.warning('Action %s did not match any of the valid options.', self.verb)
