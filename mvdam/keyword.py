"""
KEYWORD module containing Keyword class
"""
import json
import logger

from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK


class Keyword():

    def __init__(self, verb: str, keywords: str):
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

        self.verb = verb
        self.keywords = keywords

        self.sdk_handle = SDK().handle

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
                auth=current_session.access_token,
                data=keyword)

    def get(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.sdk_handle.keyword.get(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            response_json = response.json()
            self.log.debug(json.dumps(response_json, indent=4))

            keywords = {}
            for keyword in response_json['payload']:
                keywords[keyword['id']] = keyword['keywordName']

            print(f'Keywords available:\n{json.dumps(keywords, indent=4)}')

            return keywords

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
