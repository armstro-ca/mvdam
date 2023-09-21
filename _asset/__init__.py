"""
ASSET module containing Asset class
"""
import json
import logger

from _bulk import Bulk
from mvsdk.rest import Client
from mvsdk.rest.bulk import BulkContainer


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

    def __init__(self, session: dict, verb: str, asset_id: str,
                 keywords: str, bulk: bool = False):
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

        self.session = session
        self.verb = verb
        self.asset_id = asset_id
        self.keywords = keywords
        self.bulk = bulk

        if self.bulk:
            self.bulk_container = BulkContainer()

        self.sdk_handle = Client()

        self.verbs = [
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
            object_id=self.asset_id
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
            self.bulk_container.add_request(response)
            return self.bulk_container
        
        if 200 <= response['status'] < 300:
            keyword_list = self.keywords.replace(",", ", ").rsplit(",", 1)
            self.log.info('Keywords %s added to %s',
                          " and".join(keyword_list), self.asset_id)
            
        elif response['status'] == 404:
            self.log.warning('Asset with ID %s was not found.', self.asset_id)

        else:
            self.log.error('Error: %s', response)

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
            self.log.debug('Existing keyword to be deleted:\n[%s] - [%s]',
                           keyword, existing_keywords[keyword])
            
            response = self.sdk_handle.asset.delete_keyword(
                object_id=self.asset_id,
                object_action=f'keywords/{existing_keywords[keyword]}',
                auth=self.session["json"]["access_token"],
                bulk=self.bulk
                )

            if self.bulk:
                self.bulk_container.add_request(response)

            elif 200 <= response['status'] < 300:
                self.log.info('Keyword %s removed from %s', keyword, self.asset_id)

            elif response['status'] == 404:
                self.log.warning('Asset with ID %s did not have keyword %s \
                                 associated with it.', self.asset_id, keyword)
                
            else:
                self.log.error('Error: %s', response)

        return self.bulk_container if self.bulk else True

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the Asset object.
        """
        if self.asset_id is None:
            self.log.info('AssetID required to get asset keywords. '
                          'Please retry with --asset-id assetID as a parameter.')
            return

        response = self.sdk_handle.asset.get_keywords(
            object_id=self.asset_id,
            auth=self.session["json"]["access_token"],
            bulk=self.bulk
            )

        if self.bulk:
            self.bulk_container.add_request(response)
            return self.bulk_container
        
        if response['status'] == 200:
            self.log.debug(json.dumps(response, indent=4))

            keywords = []
            for keyword in response['json']['payload']:
                keywords.append(keyword['keywordName'])

            self.log.info('Keywords for asset %s: %s', self.asset_id, keywords)

        elif response['status'] == 404:
            self.log.warning('Asset with ID %s was not found.', self.asset_id)

        else:
            self.log.error('Error: %s', response)

    def set_keywords(self):
        """
        Execute the SET asset keywords call with the Asset object.
        """
        if self.asset_id is None:
            self.log.info('AssetID required to get asset keywords. '
                          'Please retry with --asset-id assetID as a parameter.')
            return self.asset_id

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
            self.log.debug('Keywords to remove: [%s]', self.keywords)
            response = self.delete_keywords()

        if keywords_to_add:
            self.keywords = ','.join(str(s) for s in keywords_to_add)
            self.log.debug('Keywords to add: [%s]', self.keywords)
            response = self.add_keywords()

        return self.bulk_container if self.bulk else True

    # --------------
    # GENERIC ACTION
    # --------------

    def action(self):
        """
        Passthrough function calling the verb required
        """
        self.verb = self.verb.replace("-", "_")
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            response = func()

            if isinstance(response, BulkContainer):
                bulk_requests = response.get_bulk_body()

                self.log.debug('Bulk Request: %s', bulk_requests)

                payload_length = str(len(bulk_requests['payload']))
                bulk_requests['headers']['Content-Length'] = payload_length

                _bulk = Bulk(self.session)

                print(f'{_bulk.post(bulk_requests)}')
            else:
                return response
        else:
            self.log.warning('Action %s did not match any of the valid options.', self.verb)
            self.log.warning('Did you mean %s?', " or".join(", ".join(self.verbs).rsplit(",", 1)))
