from mvsdk.rest import Client

class Asset():

    def __init__(self, session: dict, verb: str, asset_id: str):
        """
        Initialise the Asset class
        
        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.session = session
        self.verb = verb
        self.asset_id = asset_id
        
        self.sdk_handle = Client()

        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.session["json"]["access_token"]}',
                'User-Agent': 'PostmanRuntime/7.32.3',
                'Accept': '*/*',
                'Host': 'iam-qa.mediavalet.com'
            }
        
        self.verbs =[
            'get', 
            'post', 
            'delete',
            'get-keywords'
            ]

    def delete_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
        response = self.sdk_handle.asset.delete_keywords(
            headers=self.headers,
            object_id=f'urn:uuid:{self.asset_id}'
            )
        
        if response['status'] == 200:
            print(f'{response}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')

    def get(self):
        """
        Execute the GET asset call with the initialised Asset object.
        """
        self.sdk_handle.asset.get(params={'operator':'other_thing'})

    def get_keywords(self):
        """
        Execute the GET asset keywords call with the initialised Asset object.
        """
        response = self.sdk_handle.asset.get_keywords(
            headers=self.headers,
            object_id=f'urn:uuid:{self.asset_id}'
            )
        
        if response['status'] == 200:
            print(f'{response}')
        elif response['status'] == 404:
            print(f'Asset with ID {self.asset_id} was not found.')
        else:
            print(f'Error: {response}')

    def put(self):
        """
        
        """

    def delete(self):
        """
        https://docs.mediavalet.com/#03402a0b-4509-4338-aa2f-478f99fb996c
        
        url = "https://api.mediavalet.com/assets/urn:uuid:bb93be4f-89d6-0086-e619-8d52e3ee08ce/keywords/esse consequat"

        payload={}
        headers = {
        'Ocp-Apim-Subscription-Key': '<uuid>',
        'Authorization': '<bG9sIHlvdSB0aGluayB0aGlzIHdhcyBhIHJlYWwgdG9rZW4/>'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)"""

    def action(self):
        """
        Passthrough function calling the verb required
        """
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print('Action passed did not match valid options')