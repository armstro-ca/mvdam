from mvsdk.rest import Client

class Asset():

    def __init__(self, verb: str, **kwargs):
        self.verb = verb
        self.kwargs = kwargs

        self.sdk_handle = Client()

        self.verbs =[
            'get', 
            'post', 
            'delete'
            ]


    def get(self):
        self.sdk_handle.asset.get(params={'operator':'other_thing'})

        """url = "https://api.mediavalet.com/assets/urn:uuid:bb93be4f-89d6-0086-e619-8d52e3ee08ce/keywords?includeSoftDeleted=<boolean>"

        payload={}
        headers = {
        'Ocp-Apim-Subscription-Key': '<uuid>',
        'Authorization': '<bG9sIHlvdSB0aGluayB0aGlzIHdhcyBhIHJlYWwgdG9rZW4/>'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)"""

    def delete(self):
        url = "https://api.mediavalet.com/assets/urn:uuid:bb93be4f-89d6-0086-e619-8d52e3ee08ce/keywords/esse consequat"

        payload={}
        headers = {
        'Ocp-Apim-Subscription-Key': '<uuid>',
        'Authorization': '<bG9sIHlvdSB0aGluayB0aGlzIHdhcyBhIHJlYWwgdG9rZW4/>'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)

    def action(self):
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print('need to throw exception here')