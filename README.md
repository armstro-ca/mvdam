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

### `auth`

Initialise a session or verify credential validity. 

```bash
mvdam auth [PARAMETER]
```

### [`asset`](./docs/asset.md)
The `asset` operator gives you access to the assets and all aspects related to them.

```bash
mvdam asset [ACTION] [PARAMETER]
```

### [`attribute`](./docs/attribute.md)
The `attribute` operator gives you access to the assets and all aspects related to them.

```bash
mvdam attribute [ACTION] [PARAMETER]
```

### [`category`](./docs/category.md)
The category operator acts upon categories in the abstract, separate from their interaction with the asset <> keyword association.

```bash
mvdam category [ACTION] [PARAMETER]
```

### [`direct-link`](./docs/direct_link.md)
The keyword operator acts upon direct links.

```bash
mvdam direct-link [ACTION] [PARAMETER]
```

### [`keyword`](./docs/keyword.md)
The keyword operator acts upon keywords in the abstract, separate from their interaction with the asset <> keyword association.

```bash
mvdam keyword [ACTION] [PARAMETER]
```

### [`keyword-group`](./docs/keyword-group.md)
The keyword group operator acts upon keyword groups.

```bash
mvdam keyword-group [ACTION] [PARAMETER]
```

## Product support

Say something about the right way to get support for this service