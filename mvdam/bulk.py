"""
ASSET module containing Asset class
"""
from functools import wraps
import time
import logger

from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK


class Bulk():
    """
    Bulk Class exposing the following methods:

    """

    def __init__(self):

        self.log = logger.get_logger(__name__)

        self.sdk_handle = SDK().handle

    # --------------
    # BULK
    # --------------
    @staticmethod
    def retry(max_retries, initial_delay=20, backoff=3):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                delay = initial_delay
                while retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except ValueError as e:
                        print("Caught an exception: %s", e)
                        retries += 1
                        if current_session.has_expired:
                            print("Session has expired. Refreshing token.")
                            session_refresh_success = current_session.refresh_session()
                            print("Session refresh ",
                                  'successful' if session_refresh_success else 'unsuccessful')

                        if retries < max_retries:
                            print("Retrying in %s seconds...", delay)
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

        response = self.sdk_handle.bulk.post(
            headers=bulk_requests['headers'],
            data=bulk_requests['payload'],
            auth=current_session.access_token
            )

        if response.status_code in [429, 500]:
            self.log.warning('API returned sub-optimal response [%s].', response.status_code)
            raise ValueError(f'Response requires backoff [{response.status_code}]')
        else:
            return response
