import time
import json
import logger
import jwt

from mvdam.connect import Connect

log = logger.get_logger(__name__)


class Session:

    def __init__(self):
        """
        Loads local session file
        """
        self.session = self.read_session()

    def check_session(self) -> bool:
        """
        Check if session is still valid
        """
        try:
            if self.expiry >= time.time():
                log.debug('Session expiry (%s) later than current time (%s)',
                          self.expiry, time.time())

                session_update = Connect('refresh', client_id=None, client_secret=None,
                                         refresh_token=self.session['refresh_token']).action()

                self.session = self.read_session()

                return session_update

            else:
                log.debug('Session expiry (%s) earlier than current time (%s)',
                          self.expiry, time.time())

                session_update = Connect('auth', username=None, password=None, client_id=None,
                                         client_secret=None, grant_type='password').action()

                self.session = self.read_session()

                return session_update

        except KeyError:
            log.info('No valid session found.')
            session_update = Connect('auth', client_id=None, client_secret=None,
                                     grant_type='password').action()

            self.session = self.read_session()

            return session_update

    def refresh_session(self) -> bool:
        try:
            log.debug('Refreshing session...')
            try:
                Connect('refresh', client_id=None, client_secret=None,
                        refresh_token=self.session['refresh_token']).action()
                self.session = self.read_session()
            except Exception:
                return False
            return True

        except Exception as error:
            log.error('Session refresh failed: %s', error)
            return False

    def read_session(self) -> dict:
        try:
            with open('.session', 'r') as session_file:
                log.debug('session file found')
                session = json.load(session_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
            log.debug('Failed to load session\n%s', error)
            session = {}

        return session

    @property
    def expiry(self) -> float:
        """
        Takes JWT from auth token and returns the unix timestamp for the expiry
        """
        token = self.session['access_token']
        decoded_data = jwt.decode(jwt=token, algorithms='RS256',
                                  options={"verify_signature": False})

        return float(decoded_data['exp'])

    @property
    def has_expired(self) -> bool:
        """
        Takes JWT from auth token and returns the boolean to indicate whether it it valid
        """
        return True if self.expiry <= time.time() else False

    @property
    def access_token(self) -> str:
        """
        Returns raw JWT access token
        """
        if self.has_expired:
            self.refresh_session()

        return self.session["access_token"]


current_session = None


def initialise_session():
    """
    Initialiser for Session object
    """
    global current_session
    current_session = Session()
