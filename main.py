"""
MAIN top level module containing MVDAM CLI
"""
from typing import Optional
import logger
from typing_extensions import Annotated
import typer

import os
from dotenv import load_dotenv

load_dotenv()

from mvdam.sdk_handler import initialise_sdk

auth_url = os.getenv('MVAPIAUTHURL')
base_url = os.getenv('MVAPIBASEURL')

initialise_sdk(auth_url=auth_url, base_url=base_url)

from mvdam.session_manager import initalise_session

initalise_session()

from mvdam.session_manager import current_session

log = logger.get_logger(__name__)
log.info("MVDAM initiated...")

app = typer.Typer()


@app.command()
def asset(
    action: Annotated[
        str,
        typer.Argument(
            help="""The action to be applied to the asset.
Actions available are currently:
get-attributes
add-keywords
delete-keywords
get-keywords
set-keywords
set-keywords-with-csv"""
        )
    ],
    asset_id: Annotated[
        Optional[str],
        typer.Option(
            help='The asset ID for the action to be taken upon (eg: --asset-id \
                151b33b1-4c30-4968-bbd1-525ad812e357)',
            rich_help_panel="Single",
            show_default=False
            )
        ] = None,
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help='The keywords for the action to be taken upon as a comma separated \
                string (eg: --keywords field,sky,road,sunset)',
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    csv: Annotated[
        Optional[str],
        typer.Option(
            help='The filename of the csv for use with set-keywords-with-csv option.',
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    verbose: Annotated[
        bool,
        typer.Option(
            help='Set the output to increased verbosity',
            show_default=False
            )
        ] = False
        ):
    """
    The `asset` operator gives you access to the assets and all aspects related to them.
    """
    if verbose:
        logger.set_console_level('debug')
        log.debug('Verbose console logging set')

    log.debug("Asset option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.asset import Asset
        action = action.lower()

        log.debug('executing %s on %s', action, asset_id)

        Asset(verb=action, asset_id=asset_id, csv=csv, keywords=keywords).action()

    else:
        log.debug("no active session found")

        log.info('Session expired.\
              Please use "mvdam auth" to obtain a valid session.')


@app.command()
def attribute(
    action: Annotated[
        str,
        typer.Argument(
            help="""The action to be applied to the asset.
Actions available are currently:
get"""
        )
    ],
    asset_id: Annotated[
        Optional[str],
        typer.Option(
            help='The asset ID for the action to be taken upon (eg: --asset-id \
                151b33b1-4c30-4968-bbd1-525ad812e357)',
            rich_help_panel="Single",
            show_default=False
            )
        ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            help='Set the output to increased verbosity',
            show_default=False
            )
        ] = False
        ):
    """
    The `attribute` operator gives you access to the assets and all aspects related to them.
    """
    if verbose:
        logger.set_console_level('debug')
        log.debug('Verbose console logging set')

    log.debug("Attribute option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.attribute import Attribute
        action = action.lower()

        log.debug('executing %s on %s', action, asset_id)

        Attribute(action).action()

    else:
        log.debug("no active session found")

        log.info('Session expired.\
              Please use "mvdam auth" to obtain a valid session.')


@app.command()
def auth(
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
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            help='Set the output to increased verbosity',
            show_default=False
            )
        ] = False
        ):
    """
    Connect the CLI to your MediaValet instance by authenticating.

    Create an authenticated session.
    Credentials can be presented as args (outlined below),
    can be set as environment variables or can be set in a .env file
    """
    if verbose:
        logger.set_console_level('debug')
        log.debug('Verbose console logging set')

    log.debug("Connect option executed")

    from mvdam.connect import Connect

    log.debug('executing auth (type: %s)', grant_type)
    Connect('auth', username=username, password=password, client_id=client_id, client_secret=client_secret,
            grant_type=grant_type).action()


@app.command()
def keyword(
    action: Annotated[
        str,
        typer.Argument(
            help="""The action to be applied to the asset.
Actions available are currently:
get"""
            )
        ],
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help='The keywords for the action to be taken upon as a comma separated \
                string (eg: --keywords field,sky,road,sunset)',
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    verbose: Annotated[
        bool,
        typer.Option(
            help='Choose the verbosity of the response \
                (eg: --verbosity [verbose, raw, bulk])',
            show_default=False
            )
        ] = False
        ):
    """
    The keyword operator acts upon keywords in the abstract.
    """
    if verbose:
        logger.set_console_level('debug')
        log.debug('Verbose console logging set')

    log.debug("Keyword option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.keyword import Keyword
        action = action.lower()
        Keyword(action, keywords).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to ',
              'obtain a valid session first.')


@app.command()
def keyword_group(
    action: Annotated[
        str,
        typer.Argument(
            help="""The action to be applied to the asset.
Actions available are currently:
get"""
            )
        ],
    group: Annotated[
        Optional[str],
        typer.Option(
            help='The keyword group for the action to be taken upon as a comma separated \
                string (eg: --keywords field,sky,road,sunset)',
            rich_help_panel="Single",
            show_default=False
            )
        ] = "",
    verbose: Annotated[
        bool,
        typer.Option(
            help='Choose the verbosity of the response \
                (eg: --verbosity [verbose, raw, bulk])',
            show_default=False
            )
        ] = False
        ):
    """
    The keyword operator acts upon keywords in the abstract.
    """
    if verbose:
        logger.set_console_level('debug')
        log.debug('Verbose console logging set')

    log.debug("KeywordGroup option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.keyword_group import KeywordGroup
        action = action.lower()
        KeywordGroup(action, group).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to obtain a valid session first.')


if __name__ == "__main__":
    app()
