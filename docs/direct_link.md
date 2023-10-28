# `direct-link`
The `direct-link` operator gives you access to the direct-links and all aspects related to them.

```bash
mvdam category [ACTION] [PARAMETER]
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