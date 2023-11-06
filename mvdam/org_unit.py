"""
ORGUNIT module containing OrgUnit class
"""
import json
import logger

from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK


class OrgUnit():

    def __init__(self, verb: str):
        """
        Initialise the OrgUnit class

        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.log = logger.get_logger(__name__)

        self.verb = verb

        self.sdk_handle = SDK().handle

        self.verbs = [
            'get',
            'post',
            'delete'
            ]

    # --------------
    # ORGUNIT
    # --------------

    def get_current(self):
        """
        Execute the orgunit GET call with the OrgUnit object.
        """
        response = self.sdk_handle.org_unit.get_current(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Org Unit details:\n{json.dumps(response.json()["payload"], indent=4)}')

            return response.json()

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

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
