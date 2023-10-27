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