"""
ASSET module containing Asset class

Recommendation (Felipe):
Chunk up bulk requests by rate. n/y mins.
"""
import logging

from mvsdk.rest import Client
from _bulk.bulk_object import BulkObject


class Bulk():
    """
    Bulk Class exposing the following methods:

    """

    def __init__(self, session: dict, verbosity: str):
        self.session = session
        self.verbosity = verbosity

        self.sdk_handle = Client()

    # --------------
    # BULK
    # --------------
    def post(self, bulk_requests: dict):
        """
        """
        headers = bulk_requests['headers']
        payload = bulk_requests['payload']

        logging.debug(headers)

        response = self.sdk_handle.bulk.post(
            headers=headers,
            data=payload,
            auth=self.session["json"]["access_token"]
            )
        
        return response
