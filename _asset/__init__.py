from mvsdk.rest import Client

class Asset():

    def __init__(self, verb: str, **kwargs: dict):
        """
        Initialise the Asset class
        
        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.verb = verb
        self.kwargs = kwargs

        self.sdk_handle = Client()

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]


    def get(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        self.sdk_handle.asset.get(params={'operator':'other_thing'})


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
            print('need to throw exception here')