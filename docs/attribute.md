# `attribute`
The `attribute` operator gives you access to the assets and all aspects related to them.

```bash
mvdam attribute [ACTION] [PARAMETER]
```
#### Attribute Actions
| Action            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `get`             | Get the asset set in `—asset-id`                             |

| Parameter     | Description                                                  | Type     | Required? | Example |
|---------------|--------------------------------------------------------------|----------|-----------|---------|
| `--verbose` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        | `-- verbose` |
| `--help`      | Get this set of options                                      |          |           | `--help` |


#### get
```txt
mvdam attribute get
```
Returns an array of IDs and Attribute names for all assets in the given library. 

Example:
```json
Attributes available:
{
    "6f21c3aa-7f34-44c2-86cb-27548c113bec": "Alt Text",
    "ad558cd0-398f-42b7-9da4-2ea9fd2a65c4": "Approved Date",
    "0e09ddad-1612-4f7b-98b2-e4aa32007c8e": "Aspect Ratio",
    "39d97648-4b8f-4578-8e50-f82e1cbf8203": "Bit Rate",
    "0be93fea-8c1a-4b03-87cc-daead367534b": "Color Mode",
    "6565951b-5409-45d8-b0fd-5af71db4aaab": "Description",
    "a632ed14-111f-4b49-9c26-dc5fd601dca6": "Dimensions",
    "3159b2db-d9b8-40e1-a4a5-d21e460bce7e": "Disapproved Date",
    "0e361325-7cb9-41ab-bf5a-b11df471bed3": "Expiry Date",
    "b2dfae0d-db63-4213-91e8-a00a3dc5ba42": "File Name",
    "f145dec1-23ee-4c7f-89dd-1a67bf7929ca": "File Size",
    "7b4bbc16-080b-493f-b26d-2e6bb97a1a1e": "File Type",
    "322c68a5-8f16-45eb-a71f-b3b56d5323ca": "Frame Rate",
    "ff76aac6-d9f9-49db-8e27-a0af298f22e1": "Image Height",
    "01cc5954-5220-4a34-85ca-12ccfc2ab82e": "Image Width",
    "1927031a-b4bf-447e-a6b1-09058c3d21d4": "Keywords",
    "466a6298-bdd5-4cc1-a5c8-165833fd1b5a": "Length",
    "1b3f1311-56b5-4fff-91ab-2bc5c099bf55": "Mime Type",
    "a72faa89-a2ca-4341-9993-d2a3646481f6": "Modified Date",
    "28dd6157-08b3-4496-b9d7-3bd79389646a": "Orientation",
    "29f3b4be-a023-419f-af4f-d648c749c626": "Resolution",
    "5c84053d-0f2e-478e-8cb8-8120cacfcd25": "Title",
    "ec8c9243-4cd2-497e-bfeb-342df88cad52": "Uploaded Date"
}
```