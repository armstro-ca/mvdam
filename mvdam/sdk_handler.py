from mvsdk.rest import Client

sdk_handle = None


def initialise_sdk(auth_url: str = None, base_url: str = None):
    """
    Initialiser for the MV SDK
    """
    global sdk_handle

    sdk_handle = Client(auth_url=auth_url, base_url=base_url)
