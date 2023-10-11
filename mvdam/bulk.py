"""
ASSET module containing Asset class

Recommendation (Felipe):
Chunk up bulk requests by rate. n/y mins.
"""
import logger

from mvdam.sdk_handler import sdk_handle


class Bulk():
    """
    Bulk Class exposing the following methods:

    """

    def __init__(self, access_token: str):

        self.log = logger.get_logger(__name__)

        self.access_token = access_token

        self.sdk_handle = sdk_handle

    # --------------
    # BULK
    # --------------
    def post(self, bulk_requests: dict):
        """
        """
        response = self.sdk_handle.bulk.post(
            headers=bulk_requests['headers'],
            data=bulk_requests['payload'],
            auth=self.access_token
            )

        return response
