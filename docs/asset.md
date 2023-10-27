### `asset`
The `asset` operator gives you access to the assets and all aspects related to them.

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
