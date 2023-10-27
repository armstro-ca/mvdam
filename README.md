# MediaValet MVDAM CLI

[![Lint & Unit Tests](https://github.com/armstro-ca/mvdam/actions/workflows/unittest.yml/badge.svg)](https://github.com/armstro-ca/mvdam/actions/workflows/unittest.yml) [![Compile EXE binary](https://github.com/armstro-ca/mvdam/actions/workflows/compile_binary.yml/badge.svg?event=release)](https://github.com/armstro-ca/mvdam/actions/workflows/compile_binary.yml)

A Command Line Interface (CLI) to your MediaValet DAM instance. Interact with your assets and metadata via this CLI.

## ⚡️ Quick start
### Executable

Download the executable binary that matches your operating system (Windows, MacOS, Linux) from <insert link here> and jump to [Commands & Options](#⚙️-commands--options).

### Python
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

## ⚙️ Commands & Options

### `help`

Before we do anything, lets just take a moment to familiarise ourselves with the help option that will be our guide at any time.
```bash
mvdam --help
```

``` bash
❯ python main.py --help
                                                                                                                                           
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                                
                                                                                                                                           
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                                                       Show this message and exit.                                                │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ asset        The `asset` operator gives you access to the assets and all aspects related to them.                                       │
│ connect      Connect the CLI to your MediaValet instance by authenticating it and creating a session.                                   │
│ keyword      The keyword operator acts upon keywords in the abstract.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

You can use the `--help` option at any time to get more information on the action you are looking at.

### `connect`

Initialise a session/verify
Connect the CLI to your MediaValet instance by authenticating it and creating a session.

```bash
mvdam auth
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
[asset](./docs/asset.md)

```bash
mvdam asset [ACTION] [PARAMETER]
```
#### Asset Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get`             | Get the asset set in `—asset-id`                             |
| `delete`          | Delete the asset set in `—asset-id`                          |
| `rename`          | [not yet implemented]                                        |

#### Asset Meta Action
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `find-duplicates` | Find all duplicates (by hash)                                |

#### Asset Keyword Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `add-keywords`    | Adds the keywords set by `--keywords` for a given asset set in `--asset-id` |
| `delete-keywords` | Deletes the keywords set by `—keywords` for a given asset set in `--asset-id` |
| `get-keywords`    | Gets all keywords for a given asset set in `—asset-id` |
| `get-keywords-with-category`    | Gets all keywords for assets in a given category set in `—category-id` |
| `set-keywords`    | Sets the keywords set by `—keywords` for a given asset set in `--asset-id` |
| `set-keywords-with-csv`    | Sets the keywords and for the assets defined in a CSV |

#### Asset Attribute Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get-attributes`  | Gets the attributes for a given asset set in `--asset-id` |
| `get-attributes-with-category`    | Gets all attributes for assets in a given category set in `—category-id` |

#### Parameters
| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--asset-id`  | Sets the asset-id for the action to be operated upon         | `string` | No        | `--asset-id 6099da71-4802-49dd-a963-2beae240ed2` |
| `--keywords`  | Sets the keywords for the action to operate with             | `string` | No        | `--keywords Cloud,Snowy\ Mountains,Lake` |
| `--input_csv` | Sets the CSV file used for actions using batch inputs        | `string` | No        | `--csv data/assets_w_keywords.csv` |
| `--batch-size` | Sets the size of the batches to be used when processing batch inputs      | `int`    | No        | `--batch-size 200` |
| `--offset`    | Sets the offset to be used when processing batch inputs      | `int`    | No        | `--offset 2000` |
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |


### `keywords`
The keyword operator acts upon keywords in the abstract, separate from their interaction with the asset <> keyword association.

```bash
mvdam keyword [ACTION] [PARAMETER]
```

#### Category Actions
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