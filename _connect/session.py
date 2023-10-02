import time
import json
import logger

from _connect import Connect

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
    Checks if session is still valid
    """
    # TODO: move to checking against contents of JWT, not of my own assessed value

    # token = jwt.decode(session['json']['id_token'])
    # print(f'Expiry: {token}')
    # https://auth0.com/blog/how-to-handle-jwt-in-python/

    try:
        if session['expires_at'] >= time.time():
            log.debug("Log: Session expiry (%s) later than current time (%s)",
                    session['expires_at'], time.time())

            # TODO: check if session is within n period of expiring and _then_ refresh
            log.debug('executing refresh')
            Connect('refresh', client_id=None, client_secret=None, refresh_token=session['refresh_token']).action()
            return True
    except KeyError:
        log.info('No valid session found. Please reauthenticate.')
        
    return False
