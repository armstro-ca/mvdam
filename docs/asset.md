# `asset`
The `asset` operator gives you access to the assets and all aspects related to them.

```bash
mvdam asset [ACTION] [PARAMETER]
```

```bash
> mvdam asset --help
MVDAM initiated...
                                                                                                                                                                           
 Usage: main.py asset [OPTIONS] ACTION                                                                                                                                     
                                                                                                                                                                           
 Provides access to the assets and all aspects related to them.           
                                                                                                 
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action      TEXT  Actions available are: [default: None] [required]                                                               │
│                        add-keywords                                                                                                    │
│                        delete-keywords                                                                                                 │
│                        get-attributes                                                                                                  │
│                        get-keywords                                                                                                    │
│                        set-keywords                                                                                                    │
│                        set-keywords-with-csv                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose    --no-verbose      Set the output to increased verbosity                                                                   │
│ --help                         Show this message and exit.                                                                             │
╰─────────────────────────────────-----──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Single Asset ───────────────────────────────────────────────────────────--------──────────────────────────────────────────────────────╮
│ --asset-id        TEXT  The asset ID for the action to be taken upon (eg: --asset-id 151b33b1-4c30-4968-bbd1-525ad812e357)             │
│ --keywords        TEXT  The keywords for the action to be taken upon as a comma separated string (eg: --keywords field,sky,road,sunset)│
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Batch ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input-file        TEXT     The filename of the csv for use with and batch option option.                                             │
│ --offset            INTEGER  The offset from which you would like your csv processing to start [default: 0]                            │
│ --batch-size        INTEGER  The size of the batch to be processed. Default is the recommended value [default: 200]                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### Asset Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get`             | Get the asset set in `—asset-id`                             |
| `delete`          | Delete the asset set in `—asset-id`                          |
| `rename`          | [not yet implemented]                                        |

#### get
```txt
mvdam asset get --asset-id xxxx
```


### Asset Meta Action
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `find-duplicates` | Find all duplicates (by hash)                                |

### Asset Keyword Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `add-keywords`    | Adds the keywords set by `--keywords` for a given asset set in `--asset-id` |
| `delete-keywords` | Deletes the keywords set by `—keywords` for a given asset set in `--asset-id` |
| `get-keywords`    | Gets all keywords for a given asset set in `—asset-id` |
| `get-keywords-with-category`    | Gets all keywords for assets in a given category set in `—category-id` |
| `set-keywords`    | Sets the keywords set by `—keywords` for a given asset set in `--asset-id` |
| `set-keywords-with-csv`    | Sets the keywords and for the assets defined in a CSV |

| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--asset-id`  | Sets the asset-id for the action to be operated upon         | `string` | No        | `--asset-id 6099da71-4802-49dd-a963-2beae240ed2` |
| `--keywords`  | Sets the keywords for the action to operate with             | `string` | No        | `--keywords Cloud,Snowy\ Mountains,Lake` |
| `--input-file` | Sets the CSV file used for actions using batch inputs        | `string` | No        | `--output-file data/assets_w_keywords.csv` |
| `--batch-size` | Sets the size of the batches to be used when processing batch inputs      | `int`    | No        | `--batch-size 200` |
| `--offset`    | Sets the offset to be used when processing batch inputs      | `int`    | No        | `--offset 2000` |
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |


#### add-keywords
Usage:
```txt
mvdam asset add-keywords --asset-id 6099da71-4802-49dd-a963-2beae240ed26 --keywords Cloud,Snowy\ Mountains,Lake
```
Returns a string confirming that the keyword(s) were assigned to the asset

Example:
```json
Keywords fanfare added to 6099da71-4802-49dd-a963-2beae240ed26
```

#### delete-keywords
Usage:
```txt
mvdam asset delete-keywords --asset-id 6099da71-4802-49dd-a963-2beae240ed26 --keywords Cloud
```
Returns a string confirming that the keyword(s) were unassigned from the asset

Example:
```json
Keyword Cloud removed from 6099da71-4802-49dd-a963-2beae240ed26
```

#### get-keywords
Usage:
```txt
mvdam asset add-keywords --asset-id 6099da71-4802-49dd-a963-2beae240ed26
```
Returns a list of keywords that are currently assigned to the asset

Example:
```json
Keywords for asset 6099da71-4802-49dd-a963-2beae240ed26: ['fanfare', 'leadoff', 'prevaluation', 'shovelman', 'vitelline']
```

#### set-keywords
Usage:
```bash
mvdam asset add-keywords --asset-id xxxx --keywords Cloud,Snowy\ Mountains,Lake
```
Sets the keywords set by `—keywords` for a given asset set in `--asset-id`
:warning: This will overwrite existing keywords for the asset in question.

#### set-keywords-with-csv
Usage:
```bash
mvdam asset set-keywords-with-csv --input-file path-to/assets_with_keywords.csv  --offset 7500
```
Sets the keywords for assets in the CSV file set.
:warning: This will overwrite existing keywords for _any_ assets listed.

### Asset Attribute Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get-attributes`  | Gets the attributes for a given asset set in `--asset-id` |


#### Parameters
| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--asset-id`  | Sets the asset-id for the action to be operated upon         | `string` | No        | `--asset-id 6099da71-4802-49dd-a963-2beae240ed2` |
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |

#### get
Usage:
```txt
mvdam asset get-attributes --asset-id 6099da71-4802-49dd-a963-2beae240ed26
```
Returns a list of attributes that are currently assigned to the asset

Example:
```json
Attributes for asset 6099da71-4802-49dd-a963-2beae240ed26:
{
    "Image Width": "259",
    "Image Height": "316",
    "Color Mode": "sRGB",
    "Resolution": "37dpi",
    "Orientation": "Portrait",
    "Mime Type": "image/jpeg",
    "File Type": "JPG",
    "Keywords": "",
    "Dimensions": "",
    "File Name": "cat_ae3bc498-b385-47a0-8977-12fdde8f9666.jpg",
    "File Size": "100449"
}
```