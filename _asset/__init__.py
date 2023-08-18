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
        """
        https://docs.mediavalet.com/#22e41739-3b8b-40e6-ade7-b70406a318e4
        
        url = "https://api.mediavalet.com/assets/urn:uuid:bb93be4f-89d6-0086-e619-8d52e3ee08ce/keywords?includeSoftDeleted=<boolean>"

        payload={}
        headers = {
        'Ocp-Apim-Subscription-Key': '<uuid>',
        'Authorization': '<bG9sIHlvdSB0aGluayB0aGlzIHdhcyBhIHJlYWwgdG9rZW4/>'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)"""
        self.sdk_handle.asset.get(params={'operator':'other_thing'})


    def put(self):
        """
        https://docs.mediavalet.com/#62f7d9bd-793a-4eb4-928c-f5d216d09de8

        url = "https://api.mediavalet.com/assets/urn:uuid:bb93be4f-89d6-0086-e619-8d52e3ee08ce"

        payload = "{\n  \"id\": \"<uuid>\",\n  \"filename\": \"<string>\",\n  \"title\": \"<string>\",\n  \"description\": \"<string>\",\n  \"fileSizeInBytes\": \"<long>\"\n}"
        headers = {
        'Ocp-Apim-Subscription-Key': '<uuid>',
        'Authorization': '<bG9sIHlvdSB0aGluayB0aGlzIHdhcyBhIHJlYWwgdG9rZW4/>'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)

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