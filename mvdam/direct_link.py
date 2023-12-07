"""
KEYWORD module containing Keyword class
"""
import json
import pathlib
import logger
import pandas as pd
from tqdm import tqdm
import uuid
import sys

from mvdam.bulk import Bulk
from mvdam.asset import Asset
from mvdam.attribute import Attribute
from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK

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
        self.attribute = Attribute()
        self.asset = Asset()

        self.verb = verb
        self.asset_id = kwargs.get('asset_id')
        self.input_file = kwargs.get('input_file')
        self.output_file = kwargs.get('output_file')
        self.offset = kwargs.get('offset') or 0
        self.asset_identifier = kwargs.get('asset_identifier') or None
        self.sync = kwargs.get('sync') or False

        self.file_format = 'JPEG'

        self.sdk_handle = SDK().handle

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
            auth=current_session.access_token,
            object_id=self.asset_id
            )

        response_json = response.json()

        if 200 <= response.status_code < 300:
            if response_json['recordCount']['totalRecordsFound'] == 0:
                self.log.info('Asset %s has no Direct Link. Use "create" to create one.',
                              self.asset_id)
            else:
                links = {}

                for link in response_json['payload']:
                    links[link['cdnLink']] = link['linkName']

                self.log.info('Direct Link(s) for %s: \n%s', self.asset_id,
                              json.dumps(links, indent=4))

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
            self.log.info('Direct Link for %s: %s', self.asset_id,
                          response_json['payload']['cdnLink'])

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
        batch_size: int = 200
        offset: int = self.offset
        error_count: int = 0
        error_limit: int = 5
        loc: int = 0

        # initiate instance of bulk endpoint
        bulk = Bulk()

        # open the csv file within context
        with open(self.input_file, 'r') as f:
            df = pd.read_csv(f)

            if self.asset_identifier:
                asset_column = self.asset_identifier
            else:
                asset_column = 'System.Id'
            try:
                _ = df[[asset_column]]
            except KeyError:
                self.log.error('Column %s not present in %s. Please use --asset-identifier to set \
                               asset-id containing column.',
                               asset_column, self.input_file)
                sys.exit()

            df_export = pd.DataFrame()

            # create batches of get keyword requests to calculate deltas
            for i in range(offset, len(df), batch_size):
                self.log.info('Processing batch of %s records (batch: %s to %s) of %s total.',
                              batch_size,
                              offset+(loc*batch_size),
                              offset+((loc+1)*batch_size),
                              len(df)
                              )
                loc += 1

                if error_count > 0:
                    self.log.info('Error encountered: %s of %s allowable', error_count, error_limit)

                df_batch = df.iloc[i:i + batch_size]

                bulk_request = BulkRequest()

                # Build a BulkRequest object to get the existing keywords for each asset_id
                for index, row in tqdm(df_batch.iterrows(), total=df_batch.shape[0],
                                       desc='Building bulk request...'):
                    asset_id = row[asset_column]

                    try:
                        _ = uuid.UUID(asset_id)
                    except ValueError:
                        self.log.error('Invalid ID in %s:%s. Please check and verify.',
                                       self.input_file, i+index)
                        exit()

                    file_attributes = self.asset.get_attributes(asset_id=asset_id)
                    format = file_attributes['File Type']

                    self.log.debug('Processing #%s [%s]',
                                   index, asset_id)
                    bulk_request.add_request(self.create_direct_link(
                            asset_id=asset_id,
                            format=format,
                            bulk=True
                        )
                    )

                # Send the BulkRequest object to the bulk handle
                request = bulk_request.get_payload()

                response = bulk.post(bulk_requests=request, sync=True)

                bulk_response = BulkResponse(response)

                self.log.info('Create DirectLinks (synchronous) status = [%s], returned in [%s]',
                              response.status_code, response.elapsed)
                try:
                    self.log.debug(bulk_response.get_response)
                except TypeError:
                    self.log.error('Request:\n%s', request)
                    self.log.error('Response:\n%s', response.text)

                links = []

                # Process the response and add the links to the dataframe
                for index, row in tqdm(df_batch.iterrows(), total=df_batch.shape[0],
                                       desc='Processing response...'):
                    try:
                        response = bulk_response.post_response[index % batch_size]

                        try:
                            payload = response['payload']
                            link = json.loads(payload)['cdnLink']
                        except KeyError as key_error:
                            self.log.error('Cannot access payload of response; %s', key_error)
                            link = None

                        if int(response['status_code']) >= 300:
                            error_count += 1
                            self.dump_current_row(f'{row[asset_column]} : {response}')
                            links.append('')
                        else:
                            links.append(link)
                    except IndexError:
                        links.append('')

                df_batch = df_batch.assign(Links=links)
                df_export = pd.concat((df_export, df_batch), axis=0)

                self.log.info("Writing to %s", self.output_file)

                df_export.to_csv(self.output_file, index=False)

    def export(self):
        """
        Execute the asset GET call with the Asset object.
        """
        if not self.output_file:
            self.log.error('No file specified for output. Please set --output-csv flag.')
            sys.exit()

        try:
            with open(self.output_file, 'wb') as file:
                response = self.sdk_handle.direct_link.export(
                    auth=current_session.access_token,
                    object_id=self.asset_id
                    )

                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024
                progress_bar = tqdm(response.iter_content(), total=total_size_in_bytes,
                                    unit='iB', unit_scale=True)
                with open(self.output_file, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                progress_bar.close()
                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    self.log.error("ERROR, something went wrong")

        except IOError:
            self.log.error('Could not write to %s. Please check write permissions and try again.',
                           self.output_file)

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

        file_format = kwargs.get('format') or self.file_format
        asset_id = kwargs.get('asset_id') or self.asset_id

        bulk = kwargs.get('bulk') or False

        create_json = \
            {
                "renditionSettings": {
                    "size": {
                        "type": "Original"
                    },
                    "format": file_format
                },
                "linkSettings": {
                    "linkName": "Default"
                }
            }

        response = self.sdk_handle.direct_link.create(
            auth=current_session.access_token,
            object_id=asset_id,
            data=json.dumps(create_json),
            bulk=bulk,
            sync=self.sync
            )

        return response

    def dump_current_row(self, response):
        file = pathlib.Path("exceptions.log")

        try:
            with file.open(mode='a') as f:
                f.write(f'{str(response)}\n\r')
        except OSError as error:
            self.log.error("Writing to file %s failed due to: %s", file, error)
