"""
ASSET module containing Asset class
"""
import json
import logger
import pandas as pd
import pathlib

from _bulk import Bulk
from mvsdk.rest import Client
from mvsdk.rest.bulk import BulkRequest, BulkResponse


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
                 csv: str, keywords: str, bulk: bool = None):
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
        self.csv = csv
        self.keywords = keywords
        self.bulk = bulk

        if self.bulk:
            self.bulk_request = BulkRequest()

        self.sdk_handle = Client()

        self.existing_keywords = {}

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

    def add_keywords(self, asset_id: str = None, keywords: list = None, bulk: BulkRequest = None):
        """
        Execute the CREATE asset keywords call with the Asset object.
        """
        keywords = keywords or self.keywords
        bulk = bulk or self.bulk
        asset_id = asset_id or self.asset_id

        if keywords is str:
            keywords = keywords.split(',')

        response = self.sdk_handle.asset.create_keywords(
            data=json.dumps(keywords.split(',')),
            object_id=asset_id,
            auth=self.session["access_token"],
            bulk=bulk
            )

        if bulk:
            bulk.add_request(response)
            return bulk

        if 200 <= response.status_code < 300:
            keyword_list = keywords.replace(",", ", ").rsplit(",", 1)
            self.log.info('Keywords %s added to %s',
                          " and".join(keyword_list), asset_id)

        elif response.status_code == 404:
            self.log.warning('Asset with ID %s was not found.', asset_id)

        else:
            self.log.error('Error %s: %s', response.status_code, response.text)

    def delete_keywords(self, asset_id: str = None, keywords: list = None, bulk: BulkRequest = None):
        """
        Execute the DELETE asset keywords call with the Asset object.
        """
        keywords = keywords or self.keywords
        bulk = bulk or self.bulk
        asset_id = asset_id or self.asset_id

        if len(self.existing_keywords) == 0:
            response = self.get_asset_keywords(asset_id=asset_id)

            for existing_keyword in response.json()['payload']:
                self.existing_keywords[existing_keyword['keywordName']] = existing_keyword['id']

        for keyword in keywords.split(','):
            try:
                self.log.debug('Existing keyword to be deleted:\n[%s] - [%s]',
                            keyword, self.existing_keywords[keyword])

                response = self.sdk_handle.asset.delete_keyword(
                    object_id=asset_id,
                    object_action=f'keywords/{self.existing_keywords[keyword]}',
                    auth=self.session["access_token"],
                    bulk=True if bulk else False
                    )

                if bulk:
                    bulk.add_request(response)
                    continue

                elif 200 <= response.status_code < 300:
                    self.log.info('Keyword %s removed from %s', keyword, asset_id)

                elif response.status_code == 404:
                    self.log.warning('Asset with ID %s did not have keyword %s \
                                    associated with it.', asset_id, keyword)

                else:
                    self.log.error('Error %s: %s', response.status_code, response.text)
            except KeyError:
                self.log.error('Deletion requested for non-existant keyword:\n[%s]', keyword)

        if self.bulk:
            return self.bulk
        else:
            True

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the Asset object.
        """
        if self.asset_id is None:
            self.log.info('AssetID required to get asset keywords. '
                          'Please retry with --asset-id assetID as a parameter.')
            return
        
        response = self.get_asset_keywords(asset_id=self.asset_id)

        if self.bulk:
            self.bulk_request.add_request(response)
            return self.bulk_request

        if response.status_code == 200:
            self.log.debug(json.dumps(response.json(), indent=4))

            keywords = []

            for keyword in response.json()['payload']:
                keywords.append(keyword['keywordName'])

            self.log.info('Keywords for asset %s: %s', self.asset_id, keywords)

        elif response.status_code == 404:
            self.log.warning('Asset with ID %s was not found.', self.asset_id)

        else:
            self.log.error('Error %s: %s', response.status_code, response.text)

    def set_keywords(self, asset_id: str = None, keywords: str = None):
        """
        Execute the SET asset keywords call with the Asset object.
        """

        asset_id = asset_id or self.asset_id
        keywords = keywords or self.keywords

        if asset_id is None:
            self.log.info('AssetID required to get asset keywords. '
                          'Please retry with --asset-id assetID as a parameter.')
            return asset_id

        response = self.get_asset_keywords(asset_id=asset_id)

        current_keywords = []
        for keyword in response.json()['payload']:
            current_keywords.append(keyword['keywordName'])

        self.log.debug('Current keywords for [%s]:[%s]', asset_id, current_keywords)

        current_keywords = set(current_keywords)
        new_keywords = set(keywords.split(','))

        keywords_to_remove = current_keywords.difference(new_keywords)
        keywords_to_add = new_keywords.difference(current_keywords)

        if not (keywords_to_remove or keywords_to_add):
            self.log.debug('No difference between %s and existing keywords set for Asset %s',
                           " and".join(self.keywords.replace(",", ", ").rsplit(",", 1)), asset_id)

        if keywords_to_remove:
            self.keywords = ','.join(str(s) for s in keywords_to_remove)
            self.log.debug('Keywords to remove: [%s]', self.keywords)
            self.delete_keywords()

        if keywords_to_add:
            self.keywords = ','.join(str(s) for s in keywords_to_add)
            self.log.debug('Keywords to add: [%s]', self.keywords)
            self.add_keywords()

        return self.bulk_request if self.bulk else True

    def set_keywords_with_csv(self):
        """
        Execute the SET asset keywords call with the Asset object.

        This is a purpose built, bulk only, method.
        """
        # set the size of the bulk batches to post at any one time
        batch_size: int = 100
        error_count: int = 0

        # initiate instance of bulk endpoint
        bulk = Bulk(self.session)

        # open the csv file within context 
        with open(self.csv, 'r') as f:
            df = pd.read_csv(f)

            # create batches of get keyword requests to calculate deltas
            for i in range(0, len(df), batch_size):
                df_batch = df.iloc[i:i + batch_size]

                bulk_request = BulkRequest()
                self.existing_keywords = {}

                # Build a BulkRequest object to get the existing keywords for each asset_id
                for index, row in df_batch.iterrows():
                    asset_id = row["System.Id"]
                    new_keywords = ''.join(row["Keywords"]).replace(', ', ',')
                    self.log.info('Processing #%s [%s] with keywords [%s]', index, asset_id, new_keywords)
                    bulk_request.add_request(self.get_asset_keywords(asset_id=asset_id, bulk=True))

                # Send the BulkRequest object to the bulk handle
                request = bulk_request.get_payload()
                self.log.debug(request)

                response = bulk.post(request)
                
                bulk_response = BulkResponse(response)

                self.log.info('Get Keywords Response status = [%s], returned in [%s]', response.status_code, response.elapsed)
                self.log.debug(bulk_response.get_response)

                missing_keywords = []
                surplus_keywords = []

                # Process the response and add the deltas to the dataframe
                for index, row in df_batch.iterrows():
                    try:
                        response = bulk_response.get_response[index % batch_size]
                    
                        if int(response['status_code']) >= 300:
                            error_count += 1
                            self.dump_current_row(response)
                            missing_keywords.append('')
                            surplus_keywords.append('')
                        else:
                            self.existing_keywords.update(self.get_existing_keywords(response))
                            current_keywords = self.get_current_keywords(response)
                            new_keywords = row["Keywords"].split(', ')
                            missing_keywords.append(self.get_keywords_missing(set(current_keywords), set(new_keywords)))
                            surplus_keywords.append(self.get_keywords_surplus(set(current_keywords), set(new_keywords)))
                    except IndexError:
                        missing_keywords.append('')
                        surplus_keywords.append('')

                self.log.info('missing_keywords: %s', missing_keywords)
                self.log.info('surplus_keywords: %s', surplus_keywords)

                #df_batch['missing_keywords'] = missing_keywords
                #df_batch['surplus_keywords'] = surplus_keywords

                df_batch = df_batch.assign(missing_keywords=missing_keywords)
                df_batch = df_batch.assign(surplus_keywords=surplus_keywords)

                # Build the BulkRequest to post the updates
                #   Additions first
                bulk_request = BulkRequest()

                for index, row in df_batch.iterrows():
                    asset_id = row["System.Id"]
                    missing_keywords = row["missing_keywords"]

                    if missing_keywords != '':
                        self.log.info('Processing addition for #%s [%s] with keywords [%s]',
                                      index, asset_id, missing_keywords)
                        self.add_keywords(asset_id=asset_id, keywords=missing_keywords, bulk=bulk_request)
                    else:
                        self.log.info('Skipping addition for #%s [%s]', index, asset_id)

                # Send the BulkRequest object to the bulk handle
                #    First check there's anything to actually send
                if bulk_request.get_request_count():
                    request = bulk_request.get_payload()
                    self.log.debug(request)
                else:
                    self.log.debug(f'No requests to post. Skipping.')

                response = bulk.post(request)

                bulk_response = BulkResponse(response)
                
                self.log.info('Add Keywords Response status = [%s], returned in [%s]', response.status_code, response.elapsed)

                self.log.debug(response)

                for response in bulk_response.post_response:
                    if int(response['status_code']) >= 300:
                        error_count += 1
                        self.dump_current_row(response)

                #   Deletions second
                bulk_request = BulkRequest()
                
                for index, row in df_batch.iterrows():
                    asset_id: str = row["System.Id"]
                    surplus_keywords = row["surplus_keywords"]

                    if surplus_keywords != '':
                        self.log.info('Processing deletion for #%s [%s] with keywords [%s]',
                                      index, asset_id, surplus_keywords)
                        try:
                            self.delete_keywords(asset_id=asset_id, keywords=surplus_keywords, bulk=bulk_request)
                        except KeyError as error:
                            self.log.error('KeyError building delete bulk: %s\n%s', error, row)
                            self.log.error('Existing Keywords; %s', self.existing_keywords)
                            self.dump_current_row(row)
                    else:
                        self.log.info('Skipping deletion for #%s [%s]', index, asset_id)

                # Send the BulkRequest object to the bulk handle
                #    First check there's anything to actually send
                if bulk_request.get_request_count():
                    request = bulk_request.get_payload()
                    self.log.debug(request)
                else:
                    self.log.debug(f'No requests to post. Skipping.')

                response = bulk.post(request)

                bulk_response = BulkResponse(response)

                self.log.info('Delete Keywords Response status = [%s], returned in [%s]', response.status_code, response.elapsed)

                self.log.debug(response)

                for response in bulk_response.post_response:
                    if int(response['status_code']) >= 300:
                        error_count += 1
                        self.dump_current_row(response)

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

            if isinstance(response, BulkRequest):
                # initiate instance of bulk endpoint
                _bulk = Bulk(self.session)

                # get contents of bulk object and post to sdk
                _bulk.post(response.get_payload())
            else:
                return response
        else:
            self.log.warning('Action %s did not match any of the valid options.', self.verb)
            self.log.warning('Did you mean %s?', " or".join(", ".join(self.verbs).rsplit(",", 1)))

    # --------------
    # Abstractions
    # --------------

    def get_asset_keywords(self, asset_id: str, bulk: bool = False):
        response = self.sdk_handle.asset.get_keywords(
            object_id=asset_id,
            auth=self.session["access_token"],
            bulk=bulk
            )

        return response

    def get_keywords_surplus(self, current_keywords: set, new_keywords: set):
        self.log.debug('current_keywords: [%s]', current_keywords)
        self.log.debug('new_keywords: [%s]', new_keywords)

        keywords_to_remove = current_keywords.difference(new_keywords)
        self.log.debug('Keywords to delete: [%s]', list(keywords_to_remove))

        keywords_string = ','.join(str(s) for s in keywords_to_remove)

        return keywords_string

    def get_keywords_missing(self, current_keywords: set, new_keywords: set):
        self.log.debug('current_keywords: [%s]', current_keywords)
        self.log.debug('new_keywords: [%s]', new_keywords)

        keywords_to_add = new_keywords.difference(current_keywords)
        self.log.debug('Keywords to add: [%s]', keywords_to_add)

        keywords_string = ','.join(str(s) for s in keywords_to_add)

        return keywords_string

    def get_existing_keywords(self, response: dict):
        keywords = {}

        #self.log.debug('Existing keywords found: %s', response)

        for keyword in json.loads(response['payload']):
            keywords[keyword['keywordName']] = keyword['id']

        return keywords
        
    def get_current_keywords(self, response: dict):
        keywords = []

        #self.log.debug('Current keywords found: %s', response)

        for keyword in json.loads(response['payload']):
            keywords.append(keyword['keywordName'])

        return keywords
    
    def dump_current_row(self, response):
        file = pathlib.Path("execptions.txt")

        try:
            with file.open(mode='a') as f:
                f.write(str(response))
        except OSError as error:
            self.log.error("Writing to file %s failed due to: %s", file, error)
