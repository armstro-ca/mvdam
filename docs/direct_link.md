# `direct-link`
The `direct-link` operator gives you access to the direct-links and all aspects related to them.

```bash
mvdam category [ACTION] [PARAMETER]
```
```bash
❯ mvdam direct-link --help
MVDAM initiated...
                                                                                                                                                                                       
 Usage: main.py direct-link [OPTIONS] ACTION                                                                                                                                           
                                                                                                                                                                                       
 Provides access to the direct links and all aspects related to them.                                                                                                                  
                                                                                                                                                                                       
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action      TEXT  Actions available are:  [default: None] [required]                                                                                                           │
│                        get                                                                                                                                                          │
│                        create                                                                                                                                                       │
│                        create-with-csv (batch)                                                                                                                                      │
│                        export                                                                                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose    --no-verbose      Choose the verbosity of the response (eg: --verbosity [verbose, raw, bulk])                                                                          │
│ --help                         Show this message and exit.                                                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Single Asset ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --asset-id        TEXT  The asset ID for the action to be taken upon (eg: --asset-id 151b33b1-4c30-4968-bbd1-525ad812e357)                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Batch ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input-file                              TEXT     The filename of the input csv for use with batch options.                                                                        │
│ --output-file                             TEXT     The filename of the output csv for use with batch options.                                                                       │
│ --offset                                  INTEGER  The offset from which you would like your csv processing to start [default: 0]                                                   │
│ --asset-identifier                        TEXT     The header of the column containing the asset IDs.                                                                               │
│ --synchronous         --no-synchronous             Option to indicating synchronous rather than asynchronous operation.                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
#### Category Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get`             | Get the asset set in `—asset-id`                             |
| `create`             | Get the asset set in `—asset-id`                             |
| `create-with-csv`             | Get the asset set in `—asset-id`                             |
| `export`             | Get the asset set in `—asset-id`                             |


| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--input-file` | Sets the CSV file used for reading asset IDs from       | `string` | No        | `--input-file data/direct-link-create-assets.csv` |
| `--output-file` | Sets the CSV file used for writing output to       | `string` | No        | `--output-file data/asset-created-direct-links.csv` |
| `--asset-identifier` | Sets the column name from which to take the asset IDs (Default: `System.Id`)     | `string` | No        | `--output-file data/asset-created-direct-links.csv` |
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |


#### get
```txt
mvdam direct-link get --asset-id 698ae72a-7f3e-40fa-83f5-19ac64442b80
```
Returns an array of Direct Links and Aliases for the given asset ID.

Example console output:
```json
Direct Link(s) for 698ae72a-7f3e-40fa-83f5-19ac64442b80: 
{
    "https://mv-cdn-endpoint-ustx-whistler.azureedge.net/qa/mvdamcli/KueKaT5_-kCD9RmsZEQrgA/q5V1I7jObUiWzJfxYH_WrQ/Original/catTitle799402.jpg.jpg": "Default"
}
```

#### create
```txt
mvdam direct-link create --asset-id 698ae72a-7f3e-40fa-83f5-19ac64442b80
```
Creates and returns an a direct-link for the asset ID provided. 

Example console output:
```txt
Direct Link for 698ae72a-7f3e-40fa-83f5-19ac64442b80: https://mv-cdn-endpoint-ustx-whistler.azureedge.net/qa/mvdamcli/KueKaT5_-kCD9RmsZEQrgA/q5V1I7jObUiWzJfxYH_WrQ/Original/catTitle799402.jpg.jpg
```

#### create-with-csv
```txt
mvdam direct-link create_with_csv --input-file data/direct-link-create-assets.csv --output-file data/asset-created-direct-links.csv --asset-identifier AssetId
```
Writes the contents of the file specified in --input-file to that specified in --output-file with the newly created Direct Link appended.

#### export
```txt
mvdam direct-link export --output-file data/links.zip
```
Creates a zip file containing a CSV of all links for all assets in a library in the file specified in --output-file