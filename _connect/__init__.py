"""
CONNECT module containing Connect class
"""
import os
import base64
import time
import json
import logging
from mvsdk.rest import Client


class Connect():
    """
    Connect Class exposing the following methods:
    __init__

    auth

    refresh

    """

    def __init__(self, verb: str, **kwargs: dict):
                 #username: str, password: str, grant_type: str):
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

        self._auth_string = base64.b64encode(
            bytes(f'{self.client_id}:{self.client_secret}',
            'utf-8"')
            )
        self._auth_string = self._auth_string.decode("utf-8")

        self.sdk_handle = Client()

        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self._auth_string}',
                'User-Agent': 'PostmanRuntime/7.32.3',
                'Accept': '*/*',
                'Host': 'iam-qa.mediavalet.com'
            }

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]


    def auth(self):
        """
        Authorize the user by call with the initialised Connect object.
        """
        if self.grant_type == 'password' or 'refresh_token':

            data = {
                'grant_type': self.grant_type,
                'username': self.username,
                'password': self.password,
                'scope': 'openid api offline_access'
            }
            domain_action = 'token'
            #try:
            response = self.sdk_handle.connect.auth(
                params="",
                headers=self.headers,
                data=data,
                domain_action=domain_action
                )

            if response['status'] == 200:
                session_file = open('.session', 'w')

                ## TODO: Don't need to do this if check_session() is checking against JWT value
                response['json']['expires_at'] = time.time() + response['json']['expires_in']
                session_file.write(json.dumps(response))
            else:
                print(f'Auth API response: {response["status"]}')

            #except Exception as error:
            #    print(f'Failure to authenticate; {error}')

        elif self.grant_type == 'auth-code':
            print("Auth-Code flow not yet implemented. Please use password flow.")

    def refresh(self):
        """
        Execute the auth GET call with the initialised Connect object.
        """
        data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        domain_action = 'token'

        response = self.sdk_handle.connect.auth(
            params="",
            headers=self.headers,
            data=data,
            domain_action=domain_action
            )

        if response['status'] == 200:
            session_file = open('.session', 'w')
            response['json']['expires_at'] = time.time() + response['json']['expires_in']
            session_file.write(json.dumps(response))
        else:
            print(f'Auth API response: {response["status"]}')

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