from mvsdk.rest import Client

class Keyword():
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
        Execute the asset GET call with the initialised Asset object.
        """
        self.sdk_handle.keyword.get(params={'operator':'other_thing'})

    def delete(self):
        """
        Execute the asset GET call with the initialised Asset object.
        """
        self.sdk_handle.keyword.delete(params={'operator':'other_thing'})

    def action(self):
        """
        Passthrough function calling the verb required
        """
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            print('need to throw exception here')