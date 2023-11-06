### `user`
The user operator acts upon users.

```bash
mvdam user [ACTION] [PARAMETER]
```
```bash
❯ python main.py user --help
MVDAM initiated...
                                                                                                                                                                                       
 Usage: main.py user [OPTIONS] ACTION                                                                                                                                               
                                                                                                                                                                                       
 Provides access to users and all aspects related to them.      

─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action      TEXT  Actions available are:  [default: None] [required]                                                                                                        │
│                        get-all                                                                                                                                                   │
│                        get-approvers                                                                                                                                             │
│                        get-current                                                                                                                                               │
│                        get-current-permissions                                                                                                                                   │
│                        get-groups                                                                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose    --no-verbose      Choose the verbosity of the response (eg: --verbosity [verbose, raw, bulk])                                                                          │
│ --help                         Show this message and exit.                                                                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

#### Category Actions
| Action   | Description                                                  |
|----------|--------------------------------------------------------------|
| `get-all` | Get all users for the given library                                          |
| `get-approvers`    | Get all approvers for the given library |
| `get-current` | Get all details regarding the current                                          |
| `get-current-permissions` | [to be implemented]                                          |
| `get-groups` | [to be implemented]                                          |


| Parameter     | Description                                                  | Type     | Required? |
|---------------|--------------------------------------------------------------|----------|-----------|
| `--verbosity` | Set the verbosity level for elevated verbosity in the interaction. Options are [verbose, raw] | `string` | No        |
| `--help`      | Get this set of options                                      |          |           |

#### get-all
Usage:
```txt
mvdam user get-all
```
Returns all users in a given library

Example:
```json
```

#### get-approvers
Usage:
```txt
mvdam user get-approvers
```
Returns all approvers for a given library

Example:
```json
```

#### get-current
Usage:
```txt
mvdam user get-current
```
Returns details of current user

Example:
```json
Current user:
{
    "id": "6e8a34d6-6fbe-4c86-91c4-0da6fa9d08a8",
    "userName": "mvdamcliadmin@mediavalet.net",
    "address": "",
    "orgUnitId": "c6800dd4-2ace-4e45-b7e6-40c872ebe704",
    "applicationName": "MediaValet",
    "defaultGroup": "Administrators",
    "userDomain": "",
    "firstName": "James",
    "lastName": "Armstrong",
    "department": "",
    "position": "",
    "title": "",
    "officeNumber": "",
    "cellularNumber": "",
    "faxNumber": "",
    "emailAddress": "mvdamcliadmin@mediavalet.net",
    "comment": "",
    "defaultSkin": "",
    "additionalMessage": "",
    "adminNotes": "",
    "lastActiveAt": "1753-01-01T00:00:00",
    "lastLockedOutAt": "1753-01-01T00:00:00",
    "lastLoginAt": "2023-11-06T04:31:36.953",
    "createdAt": "2023-08-22T18:48:04.38",
    "expiresAt": "2023-11-11T02:48:04",
    "termsandconditionsacceptedat": "2023-08-22T18:54:46.193",
    "termsConditionsAcceptanceStatus": "Accepted",
    "website": "",
    "alertsEnabled": false,
    "newUserNotification": false,
    "password": null,
    "organizationName": "mvdamcli",
    "isLockedOut": false,
    "isSuspended": false,
    "isApproved": true,
    "userType": "MediaValet",
    "isExternalUser": false,
    "roleId": "272fe2fd-ac03-4b4a-98ce-ef3a34effece",
    "_links": {
        "self": "user",
        "functions": [
            "users",
            "usersCurrent",
            "usersListApprovers",
            "usersCustomFields"
        ]
    },
    "translationKeys": {
        "DefaultGroup": "Administrators",
        "namespace": "UserGroup"
    },
    "interpolations": {}
}
```

#### get-current-permissions
Usage:
```txt
mvdam user get-current-permissions
```
Returns all users in a given library

Example:
```json
Users permissions:
{
    "roleName": "Administrators",
    "roleDescription": "Administrators",
    "inheritedFrom": [
        "Administrators"
    ],
    "permissions": [
        "CMISRead",
        "List",
        "View",
        "DownloadOriginal",
        "AddToCart",
        "ApproveDownload",
        "ApproveSubmission",
        "CreateAsset",
        "CreateFolder",
        "DeleteFolder",
        "EditMetadata",
        "ClassifyAssetOnly",
        "EditAsset",
        "LinkAsset",
        "DeleteAsset",
        "AdministerRepository",
        "AdministerOrgUnit",
        "AdministerSystem",
        "CMISWrite",
        "ViewVersions",
        "ViewLinkedAssets",
        "RunReports",
        "ApproveKeywords",
        "CreateKeywords",
        "ViewUsers",
        "ManageAttributes",
        "ShareAssetsAsRendition",
        "ShareAssetsAsOriginal",
        "ShareLightboxAsRendition",
        "ShareLightboxAsOriginal",
        "ViewAssetComments",
        "ViewAssetHistory",
        "ApproveUsers",
        "ManageBrandedPortals",
        "SSOAuthorizationRules",
        "AccessPrintUI",
        "Crop",
        "CropTemplates",
        "ManageCropTemplates",
        "AccessEasyBuild",
        "VideoIntelligenceViewEditIndex",
        "GenerateDirectLinkForOriginalOrRenditions",
        "ProvisionWebhooks",
        "ManagePeople"
    ],
    "id": "272fe2fd-ac03-4b4a-98ce-ef3a34effece",
    "repositories": [
        "3d2e9b95-ea11-41ad-ac1f-48b76403a2d5"
    ],
    "orgUnitId": "c6800dd4-2ace-4e45-b7e6-40c872ebe704",
    "orgUnitName": "mvdamcli",
    "libraryName": [
        "mvdamcli Library"
    ],
    "isDefaultGroup": true,
    "_links": {
        "self": "group",
        "functions": [
            "groups"
        ]
    },
    "translationKeys": {
        "roleName": "Administrators",
        "roleDescription": "Administrators",
        "namespace": "UserGroup"
    },
    "interpolations": {}
}
```

#### get-groups
Usage:
```txt
mvdam user get-groups
```
Returns all users in a given library

Example:
```json
```