"""
KEYWORD module containing Keyword class
"""
import json
import logging

from mvsdk.rest import Client

class Keyword():

    def __init__(self, session: dict, verb: str, verbosity: str, keywords: str):
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
        self.verbosity = verbosity
        self.keywords = keywords

        logging.debug('Verbosity level set to %s', self.verbosity)
        self.bulk = True if self.verbosity == "bulk" else False

        self.sdk_handle = Client()

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
        Execute the asset GET call with the Asset object.
        """
        for keyword in self.keywords.split(','):
            self.sdk_handle.keyword.create(
                auth=self.session["json"]["access_token"],
                data = keyword)

    def get(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.sdk_handle.keyword.get(
            auth=self.session["json"]["access_token"]
            )

        if 200 <= response['status'] < 300:
            if self.verbosity == 'verbose':
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

    # --------------
    # GENERIC ACTION
    # --------------

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