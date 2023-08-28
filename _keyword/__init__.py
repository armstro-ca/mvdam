import logging

from mvsdk.rest import Client

class Keyword():

    def __init__(self, session: dict, verb: str):
        """
        Initialise the Keyword class
        
        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.session = session
        self.verb = verb

        self.sdk_handle = Client()

        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.session["json"]["access_token"]}',
                'User-Agent': 'MVDAM_CLI/0.1.0',
                'Accept': '*/*',
                'Host': 'iam-qa.mediavalet.com'
            }

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]


    def get(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        logging.debug('Client instace is: %s', type(self.sdk_handle))
        response = self.sdk_handle.keyword.get()

        if response['status'] == 200:
            print(f'{response}')
        elif response['status'] == 404:
            print('404 returned.')
        else:
            print(f'Error: {response}')

    def delete(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        self.sdk_handle.keyword.delete(params={'operator':'other_thing'})

    def action(self):
        """
        Passthrough function calling the verb required
        """
        #try:
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        #except Exception as error:
        logging.error('need to throw exception here %s', error)