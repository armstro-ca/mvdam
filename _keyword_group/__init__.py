"""
KEYWORD module containing Keyword class
"""
import json
import logger

from mvsdk.rest import Client


class KeywordGroup():

    def __init__(self, session: dict, verb: str, keyword_group: str):
        """
        Initialise the KeywordGroup class

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
        self.keyword_group = keyword_group

        self.sdk_handle = Client()

        self.verbs = [
            'get',
            'post',
            'delete'
            ]

    # --------------
    # KEYWORD
    # --------------

    def create(self):
        """
        Execute the asset GET call with the Asset object.
        """
        for keyword in self.keywords.split(','):
            self.sdk_handle.keyword.create(
                auth=self.session["json"]["access_token"],
                data=keyword)

    def get(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.sdk_handle.keyword_group.get(
            auth=self.session["access_token"]
            )

        if 200 <= response.status_code < 300:
            self.log.info(json.dumps(response.json(), indent=4))

            return response

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
