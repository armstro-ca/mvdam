"""
MAIN top level module containing MVDAM CLI
"""
import os
import logging

from typing import Optional
from typing_extensions import Annotated
import typer

from _connect import session as se

logging.basicConfig(
    filename='api.log',
    filemode='w',
    format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s',
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
            help="The asset ID for the action to be taken upon (eg: --asset-id 151b33b1-4c30-4968-bbd1-525ad812e357)",
            rich_help_panel="Single",
            show_default=False
            )
        ] = None,
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help="The keywords for the action to be taken upon as a comma seperated string (eg: --keywords field,sky,road,sunset)",
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    verbosity: Annotated[
        str,
        typer.Option(
            help="Choose the verbosity of the response (eg: --verbosity [verbose, raw, bulk])",
            show_default=False
            )
        ] = False
    ):
    """
    Interact with the MVDAM Assets.
    Actions available are currently:
    get
    get-keywords
    delete-keyword
    """
    logging.info("asset executed")
    if se.check_session(session):
        logging.debug("active session found")
        from _asset import Asset
        action = action.lower()
        _asset = Asset(session, action, asset_id, verbosity, keywords)

        logging.debug('executing %s on %s', action, asset_id)
        _asset.action()
    else:
        logging.debug("no active session found")

        print('Session expired. Please use "connect auth" to obtain a valid session first.')

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
        ],
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help="The keywords for the action to be taken upon as a comma separated string (eg: --keywords field,sky,road,sunset)",
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    verbosity: Annotated[
        str,
        typer.Option(
            help="Choose the verbosity of the response (eg: --verbosity [verbose, raw, bulk])",
            show_default=False
            )
        ] = False
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
    if se.check_session(session):
        logging.debug("active session found")
        from _keyword import Keyword
        action = action.lower()
        _keyword = Keyword(session, action, verbosity, keywords)

        logging.debug('executing %s', action)
        _keyword.action()
    else:
        logging.debug("no active session found")

        print('Session not valid. Please use "connect auth" to obtain a valid session first.')


valid_completion_items = [
    {'asset': ('get', 'get-keywords')}
]


if __name__ == "__main__":
    session = se.get_session()
    app()
