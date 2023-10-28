### `auth`

Initialise a session or verify credential validity. 

```bash
mvdam auth [PARAMETER]
```
As long as the session is valid, the session created by calling this method is persisted and renewed as long as is possible in the local file `.session`. If this is not called before other interactions, it will be invoked silently with environment variables.

Parameters can be presented in one of three ways:
- command line
- environment file
- environment variables

#### Command Line
| Option            | Description                                                  | Type     | Example | Default |
|-------------------|--------------------------------------------------------------|----------|---------|---------|
| `--client-id`     | Set the `client id` for your MediaValet instance             | `string` | `--client-id xxxx` | `None` |
| `--client-secret` | Set the `client secret` for your MediaValet instance         | `string` | `--client-secret xxxx` | `None` |
| `--username`      | Set the `username` for your MediaValet instance              | `string` | `--username xxxx` | `None` |
| `--password`      | Set the `password` for your MediaValet instance              | `string` | `--password xxxx` | `None` |
| `--base-url`      | Set the `base-url` for your MediaValet instance              | `string` | `--base-url api.mediavalet.com` | `api.mediavalet.com` |
| `--auth-url`      | Set the `auth-url` for your MediaValet instance              | `string` | `--auth-url login.mediavalet.com` | `login.mediavalet.com` |
| `--verbose`       | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` |

#### Environment File

```env
MVCLIENTID=xxxx
MVCLIENTSECRET=xxxx
MVUSERNAME=xxxx
MVPASSWORD=xxxx
MVAPIBASEURL=xxxx
MVAPIAUTHURL=xxxx
```

#### Environment Variables

```bash
export MVCLIENTID=xxxx
export MVCLIENTSECRET=xxxx
export MVUSERNAME=xxxx
export MVPASSWORD=xxxx
export MVAPIBASEURL=xxxx
export MVAPIAUTHURL=xxxx
```

### Advanced Configuration

It is possible to derive configuration from multiple of the sources listed above. They are read in the following priority order:
- command line
- environment file
- environment variables

Meaning that a variable set as an environment variable will be overwritten by one set in the environment file and that will be overwritten by one set on the command line.