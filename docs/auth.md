### `auth`

Initialise a session or verify credential validity. 

```bash
mvdam auth [PARAMETER]
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