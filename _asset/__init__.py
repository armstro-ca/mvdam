import json
import logging

from mvsdk.rest import Client

class Asset():

    def __init__(self, session: dict, verb: str, asset_id: str, verbose: bool, keywords: str):
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
        self.keywords = keywords
        
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
            'get-keywords',
            'delete-keywords',
            'create-keywords'
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

    def add_keywords(self):
        """
        Execute the CREATE asset keywords call with the initialised Asset object.
        """
        response = self.sdk_handle.asset.create_keywords(
            data = json.dumps(self.keywords.split(',')),
            headers = self.headers,
            object_id = self.asset_id
            )
        
        if 200 <= response['status'] < 300:
            print(f'{response["json"]}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')


    def delete_keywords(self):
        """
        Execute the DELETE asset keywords call with the initialised Asset object.
        """

        response = self.sdk_handle.keyword.get(headers = self.headers)

        existing_keywords = {}
        for existing_keyword in response['json']['payload']:
                    existing_keywords[existing_keyword['keywordName']] = existing_keyword['id']

        print(existing_keywords)
        print(self.keywords)

        for keyword in self.keywords.split(','):
            try:
                response = self.sdk_handle.asset.delete_keyword(
                    headers = self.headers,
                    object_id = self.asset_id,
                    object_action = f'keywords/{existing_keywords[keyword]}'
                    )
                
                if 200 <= response['status'] < 300:
                    print(f'{response}')
                elif response['status'] == 404:
                    print(f'Asset with ID {self.asset_id} did not have keyword {keyword} associated with it.')
                else:
                    print(f'Error: {response}')
            except Exception as error:
                print(f'{error}')
        
        

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
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

    def set_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
        response = self.sdk_handle.asset.get_keywords(
            headers=self.headers,
            object_id=self.asset_id
            )
        
        current_keywords = []
        for keyword in response['json']['payload']:
            current_keywords.append(keyword['keywordName'])

        current_keywords = set(current_keywords)
        new_keywords = set(self.keywords.split(','))

        keywords_to_remove = current_keywords.difference(new_keywords)
        keywords_to_add = new_keywords.difference(current_keywords)

        self.keywords = ','.join(str(s) for s in keywords_to_remove)
        logging.debug(f'Keywords to remove: {self.keywords}')
        self.delete_keywords()

        self.keywords = ','.join(str(s) for s in keywords_to_add)
        logging.debug(f'Keywords to add: {self.keywords}')
        self.add_keywords()

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