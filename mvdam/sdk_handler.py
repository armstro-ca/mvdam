from mvsdk.rest import Client


class SDK(object):
    _instance = None
    _auth_url = None
    _base_url = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(SDK, cls).__new__(cls)
            cls.auth_url = kwargs.get("auth_url")
            cls.base_url = kwargs.get("base_url")

            cls._instance.handle = Client(auth_url=cls.auth_url, base_url=cls.base_url)

        return cls._instance

    @property
    def auth_url(self) -> str:
        return self._auth_url

    @auth_url.setter
    def auth_url(self, auth_url: str):
        self._auth_url = auth_url

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self._base_url = base_url

    @property
    def handle(self) -> Client:
        return self._handle

    @handle.setter
    def handle(self, handle: Client):
        self._handle = handle
