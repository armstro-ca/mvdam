"""
USER module containing User class
"""
import json
import logger

from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK


class User():

    def __init__(self, verb: str):
        """
        Initialise the User class

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
    # USER
    # --------------

    def get_all(self):
        """
        Execute the user GET_ALL call with the USER object.
        """
        response = self.sdk_handle.user.get_all(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Users available:\n{json.dumps(response.json()["payload"], indent=4)}')

            return response.json()

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

    def get_approvers(self):
        """
        Execute the user GET_APPROVERS call with the USER object.
        """
        response = self.sdk_handle.user.get_approvers(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Approvers available:\n{json.dumps(response.json()["payload"], indent=4)}')

            return response.json()

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

    def get_current(self):
        """
        Execute the user GET_CURRENT call with the USER object.
        """
        response = self.sdk_handle.user.get_current(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Current user:\n{json.dumps(response.json()["payload"], indent=4)}')

            return response.json()

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

    def get_current_permissions(self):
        """
        Execute the user GET_CURRENT call with the USER object.
        """
        response = self.sdk_handle.user.get_current_permissions(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Users permissions:\n{json.dumps(response.json()["payload"], indent=4)}')

            return response.json()

        elif response.status_code == 404:
            self.log.warning('404 returned')
        else:
            self.log.error('Error: %s', response)

    def get_groups(self):
        """
        Execute the user GET call with the USERGROUPS object.
        """
        response = self.sdk_handle.user_group.get(
            auth=current_session.access_token
            )

        if 200 <= response.status_code < 300:
            self.log.debug(json.dumps(response.json(), indent=4))

            print(f'Users permissions:\n{json.dumps(response.json()["payload"], indent=4)}')

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
