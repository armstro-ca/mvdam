"""
KEYWORD module containing Keyword class
"""
import json
import logger

from mvsdk.rest import Client


class Keyword():

    def __init__(self, session: dict, verb: str, keywords: str):
        """
        Initialise the Keyword class

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
        self.keywords = keywords

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
        response = self.sdk_handle.keyword.get(
            auth=self.session["json"]["access_token"]
            )

        if 200 <= response['status'] < 300:
            self.log.debug(json.dumps(response, indent=4))

            keywords = {}
            for keyword in response['json']['payload']:
                keywords[keyword['id']] = keyword['keywordName']

            print(f'Keywords available: {keywords}')

            return keywords

        elif response['status'] == 404:
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
