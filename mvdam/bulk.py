"""
ASSET module containing Asset class

Recommendation (Felipe):
Chunk up bulk requests by rate. n/y mins.
"""
import logger
from functools import wraps
import time

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
    @staticmethod
    def retry(max_retries, initial_delay=20, backoff=3):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                max_retries = 5
                delay = initial_delay
                while retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except ValueError as e:
                        print(f"Caught an exception: {e}")
                        retries += 1
                        if retries < max_retries:
                            print(f"Retrying in {delay} seconds...")
                            time.sleep(delay)
                            delay *= backoff
                        else:
                            raise  # If max_retries is reached, raise the exception

            return wrapper

        return decorator
    
    @retry(max_retries=3)
    def post(self, **kwargs):
        """
        """
        bulk_requests: dict = kwargs.get('bulk_requests')
        sync: bool = kwargs.get('sync')
        response = self.sdk_handle.bulk.post(
            headers=bulk_requests['headers'],
            data=bulk_requests['payload'],
            auth=self.access_token,
            sync=sync
            )

        if response.status_code in [429, 500]:
            raise ValueError('Response requires backoff')
        else:
            return response
