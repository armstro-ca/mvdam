"""
ATTRIBUTE module containing Attribute class
"""
import json
import logger

from mvsdk.rest import Client


class Attribute():

    def __init__(self, session: dict, verb: str = None):
        """
        Initialise the Attribute class

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

        self.sdk_handle = Client()

        self.verbs = [
            'get',
            'post',
            'delete'
            ]

    # --------------
    # ATTRIBUTE
    # --------------

    def get(self):
        """
        Execute the asset GET call with the Asset object.
        """
        response = self.sdk_handle.attribute.get(
            auth=self.session["access_token"]
            )

        if 200 <= response.status_code < 300:
            response_json = response.json()
            self.log.debug(json.dumps(response_json, indent=4))

            attributes = {}
            for attribute in response_json['payload']:
                attributes[attribute['id']] = attribute['name']

            self.log.debug('Attributes available:\n%s', {json.dumps(attributes, indent=4)})

            return attributes

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