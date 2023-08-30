# MVSDK Readme.md
#project/mediavalet/mvdam

# MediaValet MVDAM CLI

A Command Line Interface (CLI) to your MediaValet DAM instance. Interact with your assets and metadata via this CLI.

## ⚡️ Quick start

First, download and install **Python**. Version `3.10` or 
higher is required. The simply pip install the MVDAM module and start using it!

```bash
# Pip install the module:
pip install mvdam
```

Ensure you have the following details for your MediaValet Instance:
- username
- password
- client id
- client secret

(If you don’t have these to hand, please contact support@mediavalet.com)

That's all you need to know to start! 🎉

## 🐳 Docker quick start

If you don't want to install Python and the MVDAM CLI module to your system, you should feel free to using our official [Docker image] and run CLI from isolated 
container:
``` bash
# Run the mvdam make script to kick off the docker container
docker run --rm -it -v ${PWD}:${PWD} -w ${PWD} nomadicj/mediavalet:latest 
```

## ⚙️ Commands & Options

### `help`

Before we do anything, lets just take a moment to familiarise ourselves with the help option that will be our guide at any time.
```bash
mvdam --help
```

❯ python3 main.py --help
``` bash                                                                                                                                                           
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                                                 
                                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                 │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation.          │
│                                                              [default: None]                                                                             │
│ --help                                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ asset        Interact with the MVDAM Assets. Actions available are currently: get get-keywords delete-keyword                                            │
│ connect      Passes verb and kwargs to same named module                                                                                                 │
│ keyword      Passes verb and kwargs to same named module.                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

You can use the `--help` option at any time to get more information on the action you are looking at.

### `connect`

Connect the CLI to your MediaValet instance by authenticating it and creating a session.

```bash
mvdam connect auth
```

| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `auth`            | Get the asset set in `—asset-id`                             |
| `delete`          | Delete the asset set in `—asset-id`                          |
| `add-keywords`    | Adds the keywords set by `--keywords` for a given asset set in `--asset-id` |
| `delete-keywords` | Deletes the keywords set by `—keywords` for a given asset set in `—asset-id` |
| `get-keywords`    | Gets all keywords for a given asset set in `—asset-id`       |
| `set-keywords`    | Sets the keywords set by `—keywords` for a given asset set in `—asset-id` |

| Option            | Description                                                  | Type     | Required? |
|-------------------|--------------------------------------------------------------|----------|-----------|
| `--client-id`     | Set the `client-id` for your MediaValet instance             | `string` | No        |
| `--client-secret` | Set the `client-secret` for your MediaValet instance         | `string` | No        |
| `--username`      | Set the `username` for your MediaValet instance              | `string` | No        |
| `--password`      | Set the `password` for your MediaValet instance              | `string` | No        |
| `--verbosity`     | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        |

### `asset`
The `asset` operator gives you access to the assets and all aspects related to them.

```bash
mvdam asset [ACTION] [PARAMETER]
```

| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get`             | Get the asset set in `—asset-id`                             |
| `delete`          | Delete the asset set in `—asset-id`                          |
| `rename`          | [not yet implemented]                                        |
| `add-keywords`    | Adds the keywords set by `--keywords` for a given asset set in `--asset-id` |
| `delete-keywords` | Deletes the keywords set by `—keywords` for a given asset set in `--asset-id` |
| `get-keywords`    | Gets all keywords for a given asset set in `—asset-id`       |
| `set-keywords`    | Sets the keywords set by `—keywords` for a given asset set in `--asset-id` |

| Parameter     | Description                                                  | Type     | Required? |
|---------------|--------------------------------------------------------------|----------|-----------|
| `--asset-id`  | Sets the asset-id for the action to be operated upon         | `string` | No        |
| `--keywords`  | Sets the keywords for the action to operate with             | `string` | No        |
| `--verbosity` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        |
| `--help`      | Get this set of options                                      |          |           |

### `keywords`
The keyword operator acts upon keywords in the abstract, separate from their interaction with the asset <> keyword association.

```bash
mvdam keyword [ACTION] [PARAMETER]
```

| Action   | Description                                                  |
|----------|--------------------------------------------------------------|
| `create` | [to be implemented]                                          |
| `get`    | Get all keywords available along with their internal `keyword-id` |
| `update` | [to be implemented]                                          |

| Parameter     | Description                                                  | Type     | Required? |
|---------------|--------------------------------------------------------------|----------|-----------|
| `--keywords`  | Sets the keywords for the action to operate with             | `string` | No        |
| `--verbosity` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        |
| `--help`      | Get this set of options                                      |          |           |

Connect the CLI to your MediaValet instance by authenticating it and creating a session.
## Product support

Say something about the right way to get support for this service