# `category`
The `category` operator gives you access to the categories and all aspects related to them.

```bash
mvdam category [ACTION] [PARAMETER]
```
#### Category Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get-assets`             | Get the asset set in `—asset-id`                             |
| `get-asset-keywords`             | Get the asset set in `—asset-id`                             |
| `get-asset-attributes`             | Get the asset set in `—asset-id`                             |


| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--output-file` | Sets the CSV file used for writing output to       | `string` | No        | `--output-file data/category-assets.csv` |
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |


#### get-assets
```txt
mvdam category get-assets
```
Returns an array of IDs and Attribute names for all assets in the given library. 

Example console output:
```json
Category a91a2a86-c015-4924-b6b8-9c62ced18d74 contains assets:
[
    "5a71c7da-72af-4700-833a-987c2005000d",
    "151b33b1-4c30-4968-bbd1-525ad812e357",
    "45479c1b-186f-47ec-9b44-8c4cb23e5b85"
]
```
Example CSV output:
```csv
System.Id
5a71c7da-72af-4700-833a-987c2005000d
151b33b1-4c30-4968-bbd1-525ad812e357
45479c1b-186f-47ec-9b44-8c4cb23e5b85
```

#### get-asset-keywords
```txt
mvdam attribute get-asset-keywords --category-id a91a2a86-c015-4924-b6b8-9c62ced18d74
```
Returns an array of IDs and Keywords for all assets in the given category. 

Example console output:
```json
{
    "5a71c7da-72af-4700-833a-987c2005000d": "ConTest, furball, lemons, portal_test, PostmanBulk, spud, test1",
    "151b33b1-4c30-4968-bbd1-525ad812e357": ", cloud, clouds, field, lemon, mountain, mountains, sheep",
    "45479c1b-186f-47ec-9b44-8c4cb23e5b85": "PostmanBulk, test1"
}
```
Example CSV output:
```csv
System.Id,Keywords
5a71c7da-72af-4700-833a-987c2005000d,"ConTest, furball, lemons, portal_test, PostmanBulk, spud, test1"
151b33b1-4c30-4968-bbd1-525ad812e357,", cloud, clouds, field, lemon, mountain, mountains, sheep"
45479c1b-186f-47ec-9b44-8c4cb23e5b85,"PostmanBulk, test1"
```

#### get-asset-attributes
```txt
mvdam attribute get-asset-attributes --category-id a91a2a86-c015-4924-b6b8-9c62ced18d74
```
Returns an array of IDs and Attribute IDs for all assets in the given category. 

Example console output:
```json
{
    "5a71c7da-72af-4700-833a-987c2005000d": "01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a, 1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca",
    "151b33b1-4c30-4968-bbd1-525ad812e357": "1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca, 01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a",
    "45479c1b-186f-47ec-9b44-8c4cb23e5b85": "1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca, 01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a"
}
```
Example CSV output:
```csv
System.Id,Attributes
5a71c7da-72af-4700-833a-987c2005000d,"01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a, 1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca"
151b33b1-4c30-4968-bbd1-525ad812e357,"1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca, 01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a"
45479c1b-186f-47ec-9b44-8c4cb23e5b85,"1b3f1311-56b5-4fff-91ab-2bc5c099bf55, 7b4bbc16-080b-493f-b26d-2e6bb97a1a1e, 1927031a-b4bf-447e-a6b1-09058c3d21d4, a632ed14-111f-4b49-9c26-dc5fd601dca6, b2dfae0d-db63-4213-91e8-a00a3dc5ba42, f145dec1-23ee-4c7f-89dd-1a67bf7929ca, 01cc5954-5220-4a34-85ca-12ccfc2ab82e, ff76aac6-d9f9-49db-8e27-a0af298f22e1, 0be93fea-8c1a-4b03-87cc-daead367534b, 29f3b4be-a023-419f-af4f-d648c749c626, 28dd6157-08b3-4496-b9d7-3bd79389646a"
```