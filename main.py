import typer
from typing_extensions import Annotated
from typing import Optional
import json
import time

app = typer.Typer()
session = {}

@app.command()
def asset(
    action: Annotated[
        str,
        typer.Argument(
            help="The action to be applied to the asset"
        )
    ],
    asset_id: Annotated[
        str,
        typer.Option(
            help="The asset ID for the action to be taken upon"
        )
    ]
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
    if check_session(session):
        from _asset import Asset
        action = action.lower()
        _asset = Asset(session, action, asset_id)

        _asset.action()
    else:
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
            rich_help_panel="Password Flow"
        )
    ] = None,
    password: Annotated[
        Optional[str],
        typer.Option(
            help="The password to be used with password flow",
            rich_help_panel="Password Flow"
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
    from _connect import Connect
    action = action.lower()
    _connect = Connect(action, username=username, password=password, grant_type=grant_type)

    _connect.action()

@app.command()
def keyword(verb: str, **kwargs):
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
    from _keyword import Keyword
    verb = verb.lower()
    _keyword = Keyword(verb, **kwargs)

    _keyword.action()    

def get_session() -> dict:
    """
    Loads local session file
    """
    try:
        with open('.session', 'r') as session_file:
            return json.load(session_file)
    except FileNotFoundError as error:
        print(f'log fnf error for session file {error}')
        return {}

def check_session(session: dict) -> bool:
    """
    Checks if session is still valid
    """
    if session['json']['expires_at'] >= time.time():
        print(f"Log: Session expiry ({session['json']['expires_at']}) later than current time ({time.time()})")
        return True
    else:
        return False

if __name__ == "__main__":
    session = get_session()
    app()