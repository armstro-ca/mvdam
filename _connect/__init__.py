import os
from mvsdk.rest import Client
import base64
import time
import json

class Connect():

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
        self.grant_type = kwargs['grant_type']
        if self.grant_type == 'password':
            self.username = kwargs['username'] or os.getenv('MVUSERNAME')
            self.password = kwargs['password'] or os.getenv('MVPASSWORD')

        print(self.username)
        print(os.getenv('MVUSERNAME'))
        self.kwargs = kwargs

        client_id = os.getenv('MVCLIENTID')
        client_secret = os.getenv('MVCLIENTSECRET')

        self._auth_string = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8"'))
        self._auth_string = self._auth_string.decode("utf-8")

        self.sdk_handle = Client()

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]


    def auth(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        if self.grant_type == 'password':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self._auth_string}',
                'User-Agent': 'PostmanRuntime/7.32.3',
                'Accept': '*/*',
                'Host': 'iam-qa.mediavalet.com'
            }
            data = {
                'grant_type': self.grant_type,
                'username': self.username,
                'password': self.password,
                'scope': 'openid api'
            }
            domain_action = 'token'
            #try:
            response = self.sdk_handle.connect.auth(
            params="",
            headers=headers,
            data=data,
            domain_action=domain_action)

            if response['status'] is 200:
                session_file = open('.session', 'w')
                response['json']['expires_at'] = time.time() + response['json']['expires_in']
                session_file.write(json.dumps(response))
            else:
                print(f'Auth API response: {response["status"]}')

            #except Exception as error:
            #    print(f'Failure to authenticate; {error}')

        elif self.grant_type == 'auth-code':
            print("Auth-Code flow not yet implemented. Please use password flow.")
            

    def action(self):
        """
        Passthrough function calling the verb required
        """
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print('need to throw exception here')