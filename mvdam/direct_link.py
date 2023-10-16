"""
KEYWORD module containing Keyword class
"""
import json
import pathlib
import logger
import pandas as pd
from tqdm import tqdm

from mvdam.bulk import Bulk
from mvdam.session_manager import current_session
from mvdam.sdk_handler import sdk_handle

from mvsdk.rest.bulk import BulkRequest, BulkResponse


class DirectLink():

    def __init__(self, verb: str, **kwargs):
        """
        Initialise the DirectLink class

        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.log = logger.get_logger(__name__)

        self.session = current_session
        self.verb = verb
        self.asset_id = kwargs.get('asset_id')
        self.input_csv = kwargs.get('input_csv')
        self.output_csv = kwargs.get('output_csv')
        self.offset = kwargs.get('offset') or 0

        self.isDevModeEnabled = False
        self.isEmbedCode = False
        self.isUniqueLink = False
        self.linkName = 'Default'
        self.turnSubtitlesOn = False
        self.chosenLanguages = ''
        self.file_format = 'JPEG'
        self.file_height = '316'
        self.file_width = '259'
        self.file_type = 'Original'

        self.sdk_handle = sdk_handle

        self.verbs = [
            'get',
            'post',
            'delete'
            ]

    # --------------
    # KEYWORD
    # --------------

    def get(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.sdk_handle.direct_link.get(
            auth=self.session.access_token,
            object_id=self.asset_id
            )

        response_json = response.json()

        if 200 <= response.status_code < 300: 
            if response_json['recordCount']['totalRecordsFound'] == 0:
                self.log.info('Asset %s has no Direct Link. Use "create" to create one.', self.asset_id)
            else:
                links = {}

                for link in response_json['payload']:
                    links[link['cdnLink']] = link['linkName']

                self.log.info('Direct Link(s) for %s: \n%s', self.asset_id, json.dumps(links, indent=4))

            return response_json

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

    def create(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.create_direct_link()

        response_json = response.json()

        if 200 <= response.status_code < 300:
            self.log.info('Direct Link for %s: %s', self.asset_id, response_json['payload']['cdnLink'])

            return response_json

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s:\n%s', response, response.text)

    def create_with_csv(self):
        """
        Execute the POST (create) direct_link call across a CSV of Asset IDs.

        This is a purpose built, bulk only, method.
        """
        # set the size of the bulk batches to post at any one time
        batch_size: int = 100
        offset: int = self.offset
        error_count: int = 0
        error_limit: int = 5
        loc: int = 0

        # initiate instance of bulk endpoint
        bulk = Bulk(self.session)

        # open the csv file within context
        with open(self.input_csv, 'r') as f:
            df = pd.read_csv(f)

            df_export = pd.DataFrame()

            # create batches of get keyword requests to calculate deltas
            for i in range(offset, len(df), batch_size):
                self.log.info('Processing %s records in batches of %s. Batch: %s to %s',
                              len(df),
                              batch_size,
                              offset+(loc*batch_size),
                              offset+((loc+1)*batch_size)
                              )
                loc += 1

                if error_count > 0:
                    self.log.info('Error encountered: %s of %s allowable', error_count, error_limit)

                df_batch = df.iloc[i:i + batch_size]

                bulk_request = BulkRequest()

                # Build a BulkRequest object to get the existing keywords for each asset_id
                for index, row in tqdm(df_batch.iterrows(), total=df_batch.shape[0], desc='Building bulk request...'):
                    asset_id = row['System.Id']
                    self.log.debug('Processing #%s [%s]',
                                   index, asset_id)
                    bulk_request.add_request(self.create_direct_link(asset_id=asset_id, bulk=True))

                # Send the BulkRequest object to the bulk handle
                response = bulk.post(bulk_request.get_payload())

                bulk_response = BulkResponse(response)

                self.log.info('Get Keywords Response status = [%s], returned in [%s]',
                              response.status_code, response.elapsed)
                self.log.debug(bulk_response.get_response)

                links = []

                # Process the response and add the links to the dataframe
                for index, row in tqdm(df_batch.iterrows(), total=df_batch.shape[0], desc='Processing response...'):
                    try:
                        response = bulk_response.post_response[index % batch_size]

                        payload = response['payload']
                        link = json.loads(payload)['cdnLink']

                        if int(response['status_code']) >= 300:
                            error_count += 1
                            self.dump_current_row(f'{row["System.Id"]} : {response}')
                            links.append('')
                        else:
                            links.append(link)                            
                    except IndexError:
                        links.append('')

                df_batch = df_batch.assign(Links=links)
                df_export = pd.concat((df_export, df_batch), axis=0)

                self.log.info("Writing to %s", self.output_csv)

                df_export.to_csv(self.output_csv, index=False)

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
            self.log.warning('Action %s did not match any of the valid options.', self.verb)
            self.log.warning('Did you mean %s?', " or".join(", ".join(self.verbs).rsplit(",", 1)))

    # --------------
    # Abstractions
    # --------------
    
    def create_direct_link(self, **kwargs):

        isDevModeEnabled = kwargs.get('IsDevModeEnabled') or self.isDevModeEnabled
        isEmbedCode = kwargs.get('IsEmbedCode') or self.isEmbedCode
        isUniqueLink = kwargs.get('IsUniqueLink') or self.isUniqueLink
        linkName = kwargs.get('LinkName') or self.linkName
        turnSubtitlesOn = kwargs.get('TurnSubtitlesOn') or self.turnSubtitlesOn
        chosenLanguages = kwargs.get('ChosenLanguages') or self.chosenLanguages
        file_format = kwargs.get('Format') or self.file_format
        file_height = kwargs.get('Height') or self.file_height
        file_width = kwargs.get('Width') or self.file_width
        file_type = kwargs.get('Type') or self.file_type
        asset_id = kwargs.get('asset_id') or self.asset_id

        bulk = kwargs.get('bulk') or False

        create_json = \
            {
                "renditionSettings": {
                    "size": {
                        "type": file_type,
                        "width": file_width,
                        "height": file_height
                        },
                    "format": file_format
                },
                "linkSettings": {
                    "isDevModeEnabled": isDevModeEnabled,
                    "linkName": linkName,
                    "isEmbedCode": isEmbedCode,
                    "isUniqueLink": isUniqueLink,
                    "turnSubtitlesOn": turnSubtitlesOn,
                    "chosenLanguages": chosenLanguages
                }
            }
        
        response = self.sdk_handle.direct_link.create(
            auth=self.session.access_token,
            object_id=asset_id,
            data=json.dumps(create_json),
            bulk=bulk
            )

        return response

    def dump_current_row(self, response):
        file = pathlib.Path("exceptions.log")

        try:
            with file.open(mode='a') as f:
                f.write(f'{str(response)}\n\r')
        except OSError as error:
            self.log.error("Writing to file %s failed due to: %s", file, error)
