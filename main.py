import typer

app = typer.Typer()

@app.command()
def auth():
    client = Client()

@app.command()
def account(operator: str, other_thing: str):
    """
    docstring
    """
    client = Client()
    client.account.get(params={operator:other_thing})

@app.command()
def asset(verb: str, **kwargs):
    """
    docstring
    """
    from _asset import Asset
    verb = verb.lower()
    _asset = Asset(verb, **kwargs)

    _asset.action()

@app.command()
def keyword(verb: str, **kwargs):
    """
    docstring
    """
    from _keyword import Keyword
    verb = verb.lower()
    _keyword = Keyword(verb, **kwargs)

    _keyword.action()

if __name__ == "__main__":
    app()