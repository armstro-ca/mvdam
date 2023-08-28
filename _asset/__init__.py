import json
import logging

from mvsdk.rest import Client

class Asset():

    def __init__(self, session: dict, verb: str, asset_id: str, verbose: bool):
        """
        Initialise the Asset class
        
        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.session = session
        self.verb = verb
        self.asset_id = asset_id
        self.verbose = verbose
        
        self.sdk_handle = Client()

        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {self.session["json"]["access_token"]}',
                'User-Agent': 'MVDAM_CLI/0.1.0'
            }
        
        self.verbs =[
            'get', 
            'post', 
            'delete',
            'get-keywords'
            ]

    # --------------
    # ASSET
    # --------------

    def put(self):
        """
        
        """

    def get(self):
        """
        Execute the GET asset call with the initialised Asset object.
        """
        self.sdk_handle.asset.get(
            headers = self.headers,
            object_id = self.asset_id
            )

    def delete(self):
        """
        Execute the DELETE asset call with the initialised Asset object.
        """

    def rename_asset(self):
        """
        Composite method to RENAME asset with the initialised Asset object.
        """

    # --------------
    # ASSET KEYWORDS
    # --------------

    def delete_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
        response = self.sdk_handle.asset.delete_keywords(
            headers = self.headers,
            object_id = self.asset_id
            )
        
        if response['status'] == 200:
            print(f'{response}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
        self.headers['Accept'] = 'application/json'

        response = self.sdk_handle.asset.get_keywords(
            headers=self.headers,
            object_id=self.asset_id
            )
        
        if response['status'] == 200:
            if self.verbose:
                print(json.dumps(response, indent=4))
            else:
                keywords = []
                for keyword in response['json']['payload']:
                    keywords.append(keyword['keywordName'])
                print(f'Keywords for asset {self.asset_id}: {keywords}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')

    # --------------
    # GENERIC ACTION
    # --------------

    def action(self):
        """
        Passthrough function calling the verb required
        """
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print('Action passed did not match valid options')