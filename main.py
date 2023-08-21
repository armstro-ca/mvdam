import typer

app = typer.Typer()

@app.command()
def auth():
    client = Client()

@app.command()
def account(verb: str, **kwargs: dict):
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
    from _account import Account
    verb = verb.lower()
    _account = Account(verb, **kwargs)

    _account.action()

@app.command()
def asset(verb: str, **kwargs: dict):
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
    from _asset import Asset
    verb = verb.lower()
    _asset = Asset(verb, **kwargs)

    _asset.action()

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

if __name__ == "__main__":
    app()