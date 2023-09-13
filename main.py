"""
MAIN top level module containing MVDAM CLI
"""
import os
import logging

from typing import Optional
from typing_extensions import Annotated
import typer

from _connect import session as se
from _bulk import BulkObject, Bulk

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
    The `asset` operator gives you access to the assets and all aspects related to them.

    Actions available are currently:
    add-keywords
    delete-keywords
    get-keywords
    set-keywords
    """
    logging.info("asset executed")
    if se.check_session(session):
        logging.debug("active session found")
        from _asset import Asset
        action = action.lower()
        _asset = Asset(session, action, asset_id, verbosity, keywords)

        logging.debug('executing %s on %s', action, asset_id)
        response = _asset.action()
        if isinstance(response, BulkObject):
            bulk_requests = response.get_bulk_body()

            bulk_requests['headers']['Content-Length'] = str(len(bulk_requests['payload']))

            print(f'{bulk_requests["headers"]}')
            print(f'{bulk_requests["payload"]}')

            _bulk = Bulk(session, verbosity)

            print(f'{_bulk.post(bulk_requests)}')
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
    Connect the CLI to your MediaValet instance by authenticating it and creating a session.

    Actions available are currently:
    auth
    """
    logging.info("connect executed")

    from _connect import Connect
    action = action.lower()
    logging.debug('executing %s (type: %s)', action, grant_type)
    _connect = Connect(action, username=username, password=password,
                       client_id=client_id, client_secret=client_secret,
                       grant_type=grant_type, auth_url=None, api_url=None)

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
    The keyword operator acts upon keywords in the abstract.

    Actions available are currently:
    get
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
