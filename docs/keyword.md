### `keywords`
The keyword operator acts upon keywords in the abstract, separate from their interaction with the asset <> keyword association.

```bash
mvdam keyword [ACTION] [PARAMETER]
```
```bash
❯ python main.py keyword --help
MVDAM initiated...
                                                                                                                                                                                       
 Usage: main.py keyword [OPTIONS] ACTION                                                                                                                                               
                                                                                                                                                                                       
 Provides access to the keywords and all aspects related to them.                                                                                                                      
                                                                                                                                                                                       
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action      TEXT  Actions available are: [default: None] [required]                                                                                                            │
│                        get                                                                                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose    --no-verbose      Choose the verbosity of the response (eg: --verbosity [verbose, raw, bulk])                                                                          │
│ --help                         Show this message and exit.                                                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Single ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --keywords        TEXT  The keywords for the action to be taken upon as a comma separated string (eg: --keywords field,sky,road,sunset)                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
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