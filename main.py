import json
import time
import os
import logging

from typing import Optional
from typing_extensions import Annotated
import typer


logging.basicConfig(
    filename='api.log', 
    filemode='w', 
    format='%(name)s - %(levelname)s - %(message)s', 
    level=os.getenv('LOGLEVEL') or logging.DEBUG
    )

app = typer.Typer()
session = {}

def autocomplete(endpoint: str, incomplete: str):
    completion = []
    for name, help_text in valid_completion_items[endpoint]:
        if name.startswith(incomplete):
            completion_item = (name, help_text)
            completion.append(completion_item)
    return completion

def get_session() -> dict:
    """
    Loads local session file
    """
    try:
        with open('.session', 'r') as session_file:
            logging.debug('active session file found')
            return json.load(session_file)
    except FileNotFoundError:
        logging.debug('no active session file found')
        return {}

def check_session(session: dict) -> bool:
    """
    Checks if session is still valid
    """
    if session['json']['expires_at'] >= time.time():
        logging.debug(f"Log: Session expiry ({session['json']['expires_at']}) later than current time ({time.time()})")
        return True
    else:
        return False

@app.command()
def asset(
    action: Annotated[
        str,
        typer.Argument(
            help="The action to be applied to the asset"
        )
    ],
    asset_id: Annotated[
        Optional[str],
        typer.Option(
            help="The asset ID for the action to be taken upon",
            rich_help_panel="Single",
            show_default=False
            )
        ] = None,
    bulk: Annotated[
        Optional[str],
        typer.Option(
            help="The username to be used with password flow",
            rich_help_panel="Bulk",
            show_default=False
            )
        ] = None,
    verbose: bool = False,
    ):
    """
    Actions available are currently:
    get
    get-keywords
    """
    logging.info("asset executed")
    if check_session(session):
        logging.debug("active session found")
        from _asset import Asset
        action = action.lower()
        _asset = Asset(session, action, asset_id, verbose)

        logging.debug('executing %s on %s', action, asset_id)
        _asset.action()
    else:
        logging.debug("no active session found")

        print('Session not valid. Please use "connect auth" to obtain a valid session first.')

@app.command()
def connect(
    action: Annotated[
        str,
        typer.Argument(
            help="Either auth or renew credentials"
        )
    ], 
    grant_type: Annotated[
        Optional[str],
        typer.Option(
            help="Either password or auth-code flow",
            show_default=False
        )
    ] = "password",
    username: Annotated[
        Optional[str],
        typer.Option(
            help="The username to be used with password flow",
            rich_help_panel="Password Flow",
        )
    ] = None,
    password: Annotated[
        Optional[str],
        typer.Option(
            help="The password to be used with password flow",
            rich_help_panel="Password Flow"
        )
    ] = None,
    client_id: Annotated[
        Optional[str],
        typer.Option(
            help="The clientId to be used with password flow",
            rich_help_panel="Password Flow",
        )
    ] = None,
    client_secret: Annotated[
        Optional[str],
        typer.Option(
            help="The clientSecret to be used with password flow",
            rich_help_panel="Password Flow",
        )
    ] = None
    ):
    """
    Passes verb and kwargs to same named module

    This is intentionally permissive to allow validation
    to be maintained solely in the module.

    Parameters
    ----------
    verb : str
        The action to be executed
    **kwargs
        The args to be passed

    """
    logging.info("connect executed")

    from _connect import Connect
    action = action.lower()
    logging.debug('executing %s (type: %s)', action, grant_type)
    _connect = Connect(action, username=username, password=password, client_id=client_id, 
                       client_secret=client_secret, grant_type=grant_type)

    _connect.action()

@app.command()
def keyword(
        action: Annotated[
        str,
        typer.Argument(
            help="The action to be applied to the asset"
            )
        ]
    ):
    """
    Passes verb and kwargs to same named module.

    This is intentionally permissive to allow validation
    to be maintained solely in the module.
    
    Parameters
    ----------
    verb : str
        The action to be executed
    **kwargs
        The args to be passed
    """
    logging.info("keyword executed")
    if check_session(session):
        logging.debug("active session found")
        from _keyword import Keyword
        action = action.lower()
        _keyword = Keyword(session, action)

        logging.debug('executing %s', action)
        _keyword.action()
    else:
        logging.debug("no active session found")

        print('Session not valid. Please use "connect auth" to obtain a valid session first.')


valid_completion_items = [
    {'asset': ('get', 'get-keywords')}
]


if __name__ == "__main__":
    session = get_session()
    app()