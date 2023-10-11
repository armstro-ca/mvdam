import time
import json
import logger
import jwt

from icecream import ic

from mvdam.connect import Connect

log = logger.get_logger(__name__)

class Session:
    def __init__(self):
        """
        Loads local session file
        """
        try:
            with open('.session', 'r') as session_file:
                log.debug('session file found')
                self.session = json.load(session_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
            log.debug('Failed to load session\n%s', error)
            self.session = {}

    def check_session(self) -> bool:
        """
        Check if session is still valid
        """
        try:
            if self.expiry >= time.time():
                log.debug('Session expiry (%s) later than current time (%s)',
                          self.expiry, time.time())

                session_handle = Connect('auth', username=None, password=None, client_id=None,
                                         client_secret=None, grant_type='password')
                session_handle.action()

                return True

            else:
                log.debug('Session expiry (%s) earlier than current time (%s)',
                          self.expiry, time.time())

                session_handle = Connect('refresh', client_id=None, client_secret=None,
                                         refresh_token=self.session['refresh_token'])
                session_handle.action()

                return True

        except KeyError:
            log.info('No valid session found.')
            session_handle = Connect('auth', client_id=None, client_secret=None, grant_type='password')
            session_handle.action()

            if session_handle:
                return True

        return False

    @property
    def expiry(self) -> float:
        """
        Takes JWT from auth token and returns the unix timestamp for the expiry
        """
        token = self.session['access_token']
        decoded_data = jwt.decode(jwt=token, algorithms='RS256', options={"verify_signature": False})

        return float(decoded_data['exp'])
    
    @property
    def access_token(self) -> str:
        """
        Returns raw JWT access token
        """
        return self.session["access_token"]


current_session = None


def initalise_session():
    """
    Initialiser for Session object
    """
    global current_session
    current_session = Session()
