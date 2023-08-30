import time
import json
import logging
#import jwt

from _connect import Connect

def get_session() -> dict:
    """
    Loads local session file
    """
    try:
        with open('.session', 'r') as session_file:
            logging.debug('session file found')
            return json.load(session_file)
    except FileNotFoundError:
        logging.debug('no session file found')
        return {}

def check_session(session: dict) -> bool:
    """
    Checks if session is still valid
    """
    ## TODO: move to checking against contents of JWT, not of my own assessed value

    #token = jwt.decode(session['json']['id_token'])
    #print(f'Expiry: {token}')
    # https://auth0.com/blog/how-to-handle-jwt-in-python/

    if session['json']['expires_at'] >= time.time():
        logging.debug("Log: Session expiry (%s) later than current time (%s)", session['json']['expires_at'], time.time())

        ## TODO: check if session is within n period of expiring and _then_ refresh
        logging.debug('executing refresh')
        _connect = Connect('refresh', client_id = None, client_secret = None, refresh_token=session['json']['refresh_token'])

        _connect.action()
        return True
    else:
        return False