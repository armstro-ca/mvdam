"""
ASSET module containing Asset class
"""
import json
import logging

from mvsdk.rest import Client
from _bulk.bulk_object import BulkObject


class Asset():
    """
    Asset Class exposing the following methods:
    __init__

    -- Asset --
    get

    delete

    put

    rename

    -- Asset Keyword --
    add-keywords

    delete-keywords

    set-keywords

    get-keywords

    """

    def __init__(self, session: dict, verb: str, asset_id: str, verbosity: str, keywords: str):
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
        self.verbosity = verbosity
        self.keywords = keywords

        logging.debug('Verbosity level set to %s', self.verbosity)
        if self.verbosity == "bulk":
            self.bulk = True
            self.bulk_object = BulkObject()
        else:
            self.bulk = False

        self.sdk_handle = Client()

        self.verbs =[
            'get', 
            'post', 
            'delete',
            'delete_keywords',
            'create_keywords',
            'get_keywords',
            'set_keywords'
            ]

    # --------------
    # ASSET
    # --------------
    def get(self):
        """
        Execute the GET asset call with the Asset object.
        """
        self.sdk_handle.asset.get(
            object_id = self.asset_id
            )

    def delete(self):
        """
        Execute the DELETE asset call with the Asset object.
        """

    def put(self):
        """
        Execute the PUT asset call with the Asset object.
        """

    def rename(self):
        """
        Composite method to RENAME asset with the Asset object.
        """

    # --------------
    # ASSET KEYWORDS
    # --------------

    def add_keywords(self):
        """
        Execute the CREATE asset keywords call with the Asset object.
        """
        response = self.sdk_handle.asset.create_keywords(
            data=json.dumps(self.keywords.split(',')),
            object_id=self.asset_id,
            auth=self.session["json"]["access_token"],
            bulk=self.bulk
            )

        if self.bulk:
            self.bulk_object.add_request(response)
            return self.bulk_object

        if 200 <= response['status'] < 300:
            print(f'Keywords {" and".join(self.keywords.replace(",",", ").rsplit(",", 1))}'
                  f' added to {self.asset_id}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')

    def delete_keywords(self):
        """
        Execute the DELETE asset keywords call with the Asset object.
        """

        # TODO: Consider caching this for bulk performance
        response = self.sdk_handle.keyword.get(
            auth=self.session["json"]["access_token"]
            )

        existing_keywords = {}
        for existing_keyword in response['json']['payload']:
            existing_keywords[existing_keyword['keywordName']] = existing_keyword['id']

        for keyword in self.keywords.split(','):
            try:
                logging.debug('Existing keyword to be deleted:\n[%s] - [%s]',
                              keyword, existing_keywords[keyword])
                response = self.sdk_handle.asset.delete_keyword(
                    object_id=self.asset_id,
                    object_action=f'keywords/{existing_keywords[keyword]}',
                    auth=self.session["json"]["access_token"],
                    bulk=self.bulk
                    )

                if self.bulk:
                    self.bulk_object.add_request(response)
                else:
                    if 200 <= response['status'] < 300:
                        print(f'Keyword {keyword} removed from {self.asset_id}')
                    elif response['status'] == 404:
                        print(f'Asset with ID {self.asset_id} did not have '
                              'keyword {keyword} associated with it.')
                    else:
                        print(f'Error: {response}')
            except Exception as error:
                print(f'Exception when deleting keywords: {error}')

        return self.bulk_object if self.bulk else True

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the Asset object.
        """
        if self.asset_id is None:
            logging.info('AssetID required to get asset keywords. '
                         'Please retry with --asset-id assetID as a parameter.')
            print('AssetID required to get asset keywords. '
                  'Please retry with --asset-id assetID as a parameter.')
            return

        response = self.sdk_handle.asset.get_keywords(
            object_id=self.asset_id,
            auth=self.session["json"]["access_token"],
            bulk=self.bulk
            )

        if self.bulk:
            self.bulk_object.add_request(response)
            return self.bulk_object

        if response['status'] == 200:
            if self.verbosity == "verbose":
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
        Execute the SET asset keywords call with the Asset object.
        """
        if self.asset_id is None:
            logging.info('AssetID required to get asset keywords. '
                         'Please retry with --asset-id assetID as a parameter.')
            print('AssetID required to get asset keywords. '
                  'Please retry with --asset-id assetID as a parameter.')
            return

        response = self.sdk_handle.asset.get_keywords(
            object_id=self.asset_id,
            auth=self.session["json"]["access_token"],
            bulk=False
            )

        current_keywords = []
        for keyword in response['json']['payload']:
            current_keywords.append(keyword['keywordName'])

        current_keywords = set(current_keywords)
        new_keywords = set(self.keywords.split(','))

        keywords_to_remove = current_keywords.difference(new_keywords)
        keywords_to_add = new_keywords.difference(current_keywords)

        if not (keywords_to_remove or keywords_to_add):
            print('No difference between '
                  f'{" and".join(self.keywords.replace(",",", ").rsplit(",", 1))} '
                  f'and existing keywords set for Asset ({self.asset_id})')

        if keywords_to_remove:
            self.keywords = ','.join(str(s) for s in keywords_to_remove)
            logging.debug('Keywords to remove: [%s]', self.keywords)
            response = self.delete_keywords()

        if keywords_to_add:
            self.keywords = ','.join(str(s) for s in keywords_to_add)
            logging.debug('Keywords to add: [%s]', self.keywords)
            response = self.add_keywords()

        return self.bulk_object if self.bulk else True


    # --------------
    # GENERIC ACTION
    # --------------

    def action(self):
        """
        Passthrough function calling the verb required
        """
        self.verb = self.verb.replace("-", "_")
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            return func()
        else:
            print(f'Action {self.verb} did not match any of the valid options.')
            print(f'Did you mean {" or".join(", ".join(self.verbs).rsplit(",", 1))}?')

