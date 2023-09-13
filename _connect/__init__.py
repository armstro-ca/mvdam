"""
CONNECT module containing Connect class
"""
import os
import time
import json
import logging

from dotenv import load_dotenv
from mvsdk.rest import Client


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
        self.verb = verb

        load_dotenv()

        try:
            self.grant_type = kwargs['grant_type']
        except KeyError:
            self.grant_type = None
        if self.grant_type == 'password':
            self.username = kwargs['username'] or os.getenv('MVUSERNAME')
            self.password = kwargs['password'] or os.getenv('MVPASSWORD')

        self.kwargs = kwargs

        self.client_id = kwargs['client_id'] or os.getenv('MVCLIENTID')
        self.client_secret = kwargs['client_secret'] or os.getenv('MVCLIENTSECRET')

        try:
            self.refresh_token = kwargs['refresh_token']
        except KeyError:
            self.refresh_token = None

        self.sdk_handle = Client()

        self.verbs = [
            'get',
            'post',
            'delete'
            ]

    def auth(self):
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

            logging.debug(auth)

            response = self.sdk_handle.connect.auth(
                data=data,
                auth=auth
                )

            if response['status'] == 200:
                session_file = open('.session', 'w')

                # TODO: Don't need to do this if check_session() is checking against JWT value
                response['json']['expires_at'] = time.time() + response['json']['expires_in']
                session_file.write(json.dumps(response))
                print('Auth successful')
            else:
                print(f'Auth API response: {response["status"]}')

        elif self.grant_type == 'auth-code':
            print("Auth-Code flow not yet implemented. Please use password flow.")

    def refresh(self):
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

        if response['status'] == 200:
            session_file = open('.session', 'w')
            response['json']['expires_at'] = time.time() + response['json']['expires_in']
            session_file.write(json.dumps(response))
        else:
            logging.info('Auth API response: %s', {response["status"]})

    def action(self):
        """
        Passthrough function calling the verb required
        """
        self.verb = self.verb.replace("-", "_")
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print(f'Action {self.verb} did not match any of the valid options.')
            print(f'Did you mean {" or".join(", ".join(self.verbs).rsplit(",", 1))}?')
