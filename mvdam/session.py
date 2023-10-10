import time
import json
import logger
import jwt

from mvdam.connect import Connect

log = logger.get_logger(__name__)


def get_session() -> dict:
    """
    Loads local session file
    """
    try:
        with open('.session', 'r') as session_file:
            log.debug('session file found')
            return json.load(session_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
        log.debug('Failed to load session\n%s', error)
        return {}


def check_session(session: dict) -> bool:
    """
    Check if session is still valid
    """
    try:
        session_expiry = float(get_expiry(session['access_token']))
        if check_session_validity(session_expiry):
            log.debug('Session expiry (%s) earlier than current time (%s)',
                      session_expiry, time.time())
            #log.debug('executing reauth')
            #Connect('auth', client_id=None, client_secret=None)
            session_handle = Connect('refresh', client_id=None, client_secret=None, refresh_token=session['refresh_token'])
            session_handle.action()

            return True

        else:
            log.debug('Session expiry (%s) later than current time (%s)',
                      session_expiry, time.time())
            session_handle = Connect('auth', username=None, password=None, client_id=None, client_secret=None, grant_type='password')
            session_handle.action()

            return True

    except KeyError:
        log.info('No valid session found.')
        session_handle = Connect('auth', client_id=None, client_secret=None, grant_type='password')
        session_handle.action()

        if session_handle:
            return True

    return False


def get_expiry(token: str) -> int:
    """
    Takes JWT from auth token and returns the unix timestamp for the expiry
    """
    decoded_data = jwt.decode(jwt=token, algorithms='RS256', options={"verify_signature": False})

    return (decoded_data['exp'])


def check_session_validity(expiry: str) -> bool:
    """
    Takes expiry timestamp and returns validity assessment
    """
    return True if expiry >= time.time() else False
