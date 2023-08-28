import json
import logging

from mvsdk.rest import Client

class Keyword():

    def __init__(self, session: dict, verb: str, verbose: bool, keywords: str):
        """
        Initialise the Keyword class
        
        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.session = session
        self.verb = verb
        self.verbose = verbose
        self.keywords = keywords.split(',')

        self.sdk_handle = Client()

        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {self.session["json"]["access_token"]}',
                'User-Agent': 'MVDAM_CLI/0.1.0'
            }

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]

    # --------------
    # KEYWORD
    # --------------

    def create(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        for keyword in self.keywords:
            self.sdk_handle.keyword.create(headers = self.headers, data = keyword)

    def get(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        logging.debug('Client instace is: %s', type(self.sdk_handle))
        response = self.sdk_handle.keyword.get(headers = self.headers)

        if response['status'] == 200:
            if self.verbose:
                print(json.dumps(response, indent=4))
            else:
                keywords = {}
                for keyword in response['json']['payload']:
                    keywords[keyword['id']] = keyword['keywordName']
                print(f'Keywords available: {keywords}')
        elif response['status'] == 404:
            print('404 returned.')
        else:
            print(f'Error: {response}')

    def update(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        self.sdk_handle.keyword.update(params={'operator':'other_thing'})

    # --------------
    # GENERIC ACTION
    # --------------

    def action(self):
        """
        Passthrough function calling the verb required
        """
        #try:
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        #except Exception as error:
        #logging.error('need to throw exception here')# %s', error)