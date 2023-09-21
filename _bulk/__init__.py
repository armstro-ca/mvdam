"""
ASSET module containing Asset class

Recommendation (Felipe):
Chunk up bulk requests by rate. n/y mins.
"""
import logger

from mvsdk.rest import Client

class Bulk():
    """
    Bulk Class exposing the following methods:

    """

    def __init__(self, session: dict):
        
        self.log = logger.get_logger(__name__)

        self.session = session

        self.sdk_handle = Client()

    # --------------
    # BULK
    # --------------
    def post(self, bulk_requests: dict):
        """
        """
        headers = bulk_requests['headers']
        payload = bulk_requests['payload']

        self.log.debug(headers)

        response = self.sdk_handle.bulk.post(
            headers=headers,
            data=payload,
            auth=self.session["json"]["access_token"]
            )

        return response
