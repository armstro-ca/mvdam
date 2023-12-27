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

from mvdam.sdk_handler import SDK

log = logger.get_logger(__name__)
log.info("MVDAM initiated...")

auth_url = os.getenv("MVAPIAUTHURL")
base_url = os.getenv("MVAPIBASEURL")

sdk = SDK(auth_url=auth_url, base_url=base_url)

log.debug("Auth URL: %s", sdk.auth_url)
log.debug("Base URL: %s", sdk.base_url)

from mvdam.session_manager import initialise_session

initialise_session()

from mvdam.session_manager import current_session


app = typer.Typer()


@app.command()
def asset(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get\r\n
get-related\r\n
get-attributes\r\n
get-categories\r\n
get-comments\r\n
get-history\r\n
add-keywords\r\n
delete-keywords\r\n
get-keywords\r\n
set-keywords\r\n
set-keywords-with-csv\r\n
get-renditions\r\n
get-video-intelligence-status"""
        ),
    ],
    asset_id: Annotated[
        Optional[str],
        typer.Option(
            help="The asset ID for the action to be taken upon (eg: --asset-id "
            + "151b33b1-4c30-4968-bbd1-525ad812e357)",
            rich_help_panel="Single Asset",
            show_default=False,
        ),
    ] = None,
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help="The keywords for the action to be taken upon as a "
            + "comma separated string (eg: --keywords field,sky,road,sunset)",
            rich_help_panel="Single Asset",
            show_default=False,
        ),
    ] = "",
    input_file: Annotated[
        Optional[str],
        typer.Option(
            help="The filename of the csv for use with and batch option.", rich_help_panel="Batch", show_default=False
        ),
    ] = "",
    output_location: Annotated[
        Optional[str],
        typer.Option(
            help="The directory for use with and get file option.", rich_help_panel="Single", show_default=False
        ),
    ] = "",
    offset: Annotated[
        Optional[int],
        typer.Option(
            help="The offset from which you would like your csv processing to start", rich_help_panel="Batch"
        ),
    ] = 0,
    batch_size: Annotated[
        Optional[int],
        typer.Option(
            help="The size of the batch to be processed. Default is the recommended value", rich_help_panel="Batch"
        ),
    ] = 200,
    raw: Annotated[bool, typer.Option(help="Get the raw json response", show_default=False)] = False,
    verbose: Annotated[bool, typer.Option(help="Set the output to increased verbosity", show_default=False)] = False,
):
    """
    Provides access to the assets and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Asset option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.asset import Asset

        action = action.lower()

        log.debug("executing %s on %s", action, asset_id)

        Asset(
            verb=action,
            asset_id=asset_id,
            input_file=input_file,
            keywords=keywords,
            output_location=output_location,
            batch_size=batch_size,
            offset=offset,
            raw=raw,
        ).action()

    else:
        log.info(
            'Session expired.\
              Please use "mvdam auth" to obtain a valid session.'
        )


@app.command()
def attribute(
    action: Annotated[str, typer.Argument(help="Actions available are:\r\n" + "get")],
    verbose: Annotated[bool, typer.Option(help="Set the output to increased verbosity", show_default=False)] = False,
):
    """
    Provides access to the attributes and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Attribute option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.attribute import Attribute

        action = action.lower()

        log.debug("executing %s", action)

        Attribute(action).action()

    else:
        log.info(
            'Session expired.\
              Please use "mvdam auth" to obtain a valid session.'
        )


@app.command()
def auth(
    grant_type: Annotated[
        Optional[str], typer.Option(help="Either password or auth-code flow", show_default=False)
    ] = "password",
    username: Annotated[
        Optional[str],
        typer.Option(
            help="The username to be used with password flow",
            rich_help_panel="Password Flow",
        ),
    ] = None,
    password: Annotated[
        Optional[str], typer.Option(help="The password to be used with password flow", rich_help_panel="Password Flow")
    ] = None,
    client_id: Annotated[
        Optional[str],
        typer.Option(
            help="The clientId to be used with password flow",
            rich_help_panel="Password Flow",
        ),
    ] = None,
    client_secret: Annotated[
        Optional[str],
        typer.Option(
            help="The clientSecret to be used with password flow",
            rich_help_panel="Password Flow",
        ),
    ] = None,
    verbose: Annotated[bool, typer.Option(help="Set the output to increased verbosity", show_default=False)] = False,
):
    """
    Provides access to authentication verification and session management

    Connect the CLI to your MediaValet instance by authenticating.

    Create an authenticated session.
    Credentials can be presented as args (outlined below),
    can be set as environment variables or can be set in a .env file
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Connect option executed")

    from mvdam.connect import Connect

    log.debug("executing auth (type: %s)", grant_type)
    Connect(
        "auth",
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        grant_type=grant_type,
    ).action()


@app.command()
def category(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get-assets\r\n
get_asset_keywords\r\n
get_asset_attributes"""
        ),
    ],
    category_id: Annotated[
        Optional[str],
        typer.Option(
            help="The keyword group for the action to be taken upon as a comma separated "
            + "string (eg: --keywords field,sky,road,sunset)",
            rich_help_panel="Single",
            show_default=False,
        ),
    ] = None,
    output_file: Annotated[
        Optional[str],
        typer.Option(
            help="The filename of the output csv for use with set-keywords-with-csv option.",
            rich_help_panel="Single",
            show_default=False,
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            help="Choose the verbosity of the response " + "(eg: --verbosity [verbose, raw, bulk])", show_default=False
        ),
    ] = False,
):
    """
    Provides access to keywords and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Category option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.category import Category

        action = action.lower()
        Category(action, category_id=category_id, output_file=output_file).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to obtain a valid session first.')


@app.command()
def direct_link(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get\r\n
create\r\n
create-with-csv (batch)\r\n
export"""
        ),
    ],
    asset_id: Annotated[
        Optional[str],
        typer.Option(
            help="The asset ID for the action to be taken upon (eg: --asset-id "
            + "151b33b1-4c30-4968-bbd1-525ad812e357)",
            rich_help_panel="Single Asset",
            show_default=False,
        ),
    ] = None,
    input_file: Annotated[
        Optional[str],
        typer.Option(
            help="The filename of the input csv for use with batch options.",
            rich_help_panel="Batch",
            show_default=False,
        ),
    ] = "",
    output_file: Annotated[
        Optional[str],
        typer.Option(
            help="The filename of the output csv for use with batch options.",
            rich_help_panel="Batch",
            show_default=False,
        ),
    ] = "",
    offset: Annotated[
        Optional[int],
        typer.Option(
            help="The offset from which you would like your csv processing to start", rich_help_panel="Batch"
        ),
    ] = 0,
    asset_identifier: Annotated[
        Optional[str],
        typer.Option(
            help="The header of the column containing the asset IDs.", rich_help_panel="Batch", show_default=False
        ),
    ] = None,
    synchronous: Annotated[
        Optional[bool],
        typer.Option(
            help="Option to indicating synchronous rather than asynchronous operation.",
            rich_help_panel="Batch",
            show_default=False,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            help="Choose the verbosity of the response " + "(eg: --verbosity [verbose, raw, bulk])", show_default=False
        ),
    ] = False,
):
    """
    Provides access to the direct links and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Keyword option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.direct_link import DirectLink

        action = action.lower()
        DirectLink(
            action,
            asset_id=asset_id,
            input_file=input_file,
            output_file=output_file,
            offset=offset,
            asset_identifier=asset_identifier,
            sync=synchronous,
        ).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to ', "obtain a valid session first.")


@app.command()
def keyword(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get\r\n
get-groups"""
        ),
    ],
    keywords: Annotated[
        Optional[str],
        typer.Option(
            help="The keywords for the action to be taken upon as a comma separated "
            + "string (eg: --keywords field,sky,road,sunset)",
            rich_help_panel="Single",
            show_default=False,
        ),
    ] = "",
    verbose: Annotated[
        bool,
        typer.Option(
            help="Choose the verbosity of the response " + "(eg: --verbosity [verbose, raw, bulk])", show_default=False
        ),
    ] = False,
):
    """
    Provides access to the keywords and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("Keyword option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.keyword import Keyword

        action = action.lower()
        Keyword(action, keywords).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to ', "obtain a valid session first.")


@app.command()
def user(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get-all\r\n
get-approvers\r\n
get-current\r\n
get-current-permissions\r\n
get-groups"""
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            help="Choose the verbosity of the response " + "(eg: --verbosity [verbose, raw, bulk])", show_default=False
        ),
    ] = False,
):
    """
    Provides access to users and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("User option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.user import User

        action = action.lower()
        User(action).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to obtain a valid session first.')


@app.command()
def org_unit(
    action: Annotated[
        str,
        typer.Argument(
            help="""
Actions available are:\r\n
get-current"""
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            help="Choose the verbosity of the response " + "(eg: --verbosity [verbose, raw, bulk])", show_default=False
        ),
    ] = False,
):
    """
    Provides access to keywords and all aspects related to them.
    """
    if verbose:
        logger.set_console_level("debug")
        log.debug("Verbose console logging set")

    log.debug("OrgUnit option executed")

    if current_session.check_session():
        log.debug("active session found")
        from mvdam.org_unit import OrgUnit

        action = action.lower()
        OrgUnit(action).action()

    else:
        log.debug("no active session found")

        print('Session not valid. Please use "mvdam auth" to obtain a valid session first.')


if __name__ == "__main__":
    app()
