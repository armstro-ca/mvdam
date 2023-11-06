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

#### get-current
Usage:
```txt
mvdam org-unit get-current
```
Returns details of current library

Example:
```json
Org Unit details:
{
    "id": "c6800dd4-2ace-4e45-b7e6-40c872ebe704",
    "names": {
        "name": "mvdamcli",
        "canonicalName": "MediaValet\\mvdamcli"
    },
    "contactInformation": {
        "street": "",
        "city": "",
        "stateProvince": "",
        "country": "",
        "postalCode": "",
        "region": "",
        "phoneNumber": "",
        "website": ""
    },
    "storage": {
        "quota": 0,
        "usage": 2169247411
    },
    "customization": {
        "headerImageAndLogos": {
            "logoImageMedium": "MV_Logo (1).png",
            "logoImageLarge": "MV_Logo (1).png",
            "headerImage": ""
        },
        "doNotDisplayRequestUserLink": false,
        "skinColors": {
            "backgroundAssetCardColor": "",
            "backgroundAssetCardHeaderColor": "",
            "backgroundHeaderColor": "",
            "backgroundMainColor": "",
            "backgroundPageColor": "",
            "backgroundReviewActionsColor": "",
            "buttonColor": "",
            "buttonInactiveColor": "",
            "highlightColor": "",
            "lineColor": "",
            "overlayColor": "",
            "tableOddRowColor": "",
            "textColor": "",
            "textHighlightColor": "",
            "textInactiveColor": "",
            "treeFolderColor": "",
            "textTreeColor": "",
            "backgroundTableHeaderColor": "",
            "backgroundModalHeaderColor": ""
        },
        "dafaultSkin": ""
    },
    "customRoot": "Library",
    "printUIClientId": null,
    "sendForApprovalNotice": "",
    "applyWatermark": true,
    "watermarkFilePath": "https://mvappustxwhistler.blob.core.windows.net/watermarks/MV-Watermark.png?sv=2017-04-17&sr=b&sig=aNX1n2hnLsS3mqjMQLjFz4hE0Zwtktn63QFl7%2B87KuE%3D&st=2023-11-06T04%3A21%3A04Z&se=2033-11-05T14%3A48%3A04Z&sp=r",
    "isAmsEnabled": false,
    "launchDarklyConfigs": null,
    "features": {
        "AdvancedDamSearchSintax": "Active",
        "AssetPicker_Search": "Active",
        "AutodeskRenditionGeneration": "Inactive",
        "BrandedPortalsSync": "Inactive",
        "CDN": "Active",
        "ClippingPath": "Inactive",
        "Crop": "Active",
        "DynamicWebGallery": "Active",
        "FaceRecognitionUnidentifiableBadFacesEnabled": "Active",
        "IAMInPortal": "Active",
        "IAMInPortalPasswordFlow": "Inactive",
        "MultiLanguage": "Inactive",
        "NotificationsDirect": "Active",
        "NotificationsFollowAsset": "Active",
        "NotificationsInApp": "Active",
        "NotificationsTrayV4": "Inactive",
        "OfficeIntegration": "Active",
        "PackageMvCategories": "Active",
        "ReportingV2BP": "Active",
        "RestrictedCategories": "Active",
        "SSOManagement": "Active",
        "SearchInFileNameV3": "Active",
        "SergeyTimeMachineTest": "Inactive",
        "SergeyTimeMachineTest1": "Active",
        "UIEnhancements": "Active",
        "V4Users": "Active",
        "V5WebGallery": "Active",
        "V5_Use_Launch_Darkly_Flags": "Active",
        "AdvancedSearch": "Active",
        "AutodeskViewer": "Inactive",
        "BrandedPortals": "Active",
        "EasyBuild": "Inactive",
        "FileNameVersioning": "Inactive",
        "ReadFromAzureSearch": "Active",
        "RequestDownloadOriginals": "Inactive",
        "SearchInCustomAttributes": "Active",
        "SearchInNestedCategories": "Active",
        "ShowAssetsBeforeFullyIngested": "Active",
        "SoftDelete": "Inactive",
        "V3ServicesShutdown": "Active",
        "V4AssetHistory": "Active",
        "V4AssetReports": "Active",
        "V4Assets": "Active",
        "V4Attributes": "Active",
        "V4Categories": "Active",
        "V4Downloads": "Active",
        "V4Emails": "Active",
        "V4KeywordGroups": "Active",
        "V4KeywordSuggestion": "Active",
        "V4Keywords": "Active",
        "V4Libraries": "Active",
        "V4Lightboxes": "Active",
        "V4Passthrough": "Active",
        "V4ReadModels": "Active",
        "V4Searches": "Active",
        "V4Sharing": "Active",
        "V4Uploads": "Active",
        "Workfront": "Inactive",
        "WriteBothSearchIndexes": "Active",
        "attributesDropdownType": "Active",
        "customAttributesFullScreenFeatureFlag": "Active",
        "fullscreenComments": "Active",
        "fullscreenGridOverlay": "Active",
        "multiPageDocumentPreview": "Active"
    },
    "featuresLastModified": {
        "AdvancedDamSearchSintax": "2023-09-21T11:59:17.7276434+00:00",
        "AssetPicker_Search": "2023-10-12T21:49:14.2208051+00:00",
        "AutodeskRenditionGeneration": "2023-09-12T19:09:11.5674062+00:00",
        "BrandedPortalsSync": "2022-08-19T05:58:13.4674985+00:00",
        "CDN": "2021-03-05T10:32:46.9561172+00:00",
        "ClippingPath": "2021-10-25T19:16:12.097065+00:00",
        "Crop": "2023-08-22T18:52:03.9512941+00:00",
        "DynamicWebGallery": "2022-11-18T00:58:55.0691508+00:00",
        "FaceRecognitionUnidentifiableBadFacesEnabled": "2023-07-12T22:59:39.3967424+00:00",
        "IAMInPortal": "2023-08-22T18:52:01.4087466+00:00",
        "IAMInPortalPasswordFlow": "2020-03-05T21:12:55.9677471+00:00",
        "MultiLanguage": "2022-11-19T00:22:46.700214+00:00",
        "NotificationsDirect": "2022-09-08T15:46:12.38338+00:00",
        "NotificationsFollowAsset": "2022-10-27T13:41:50.0337814+00:00",
        "NotificationsInApp": "2023-04-19T21:40:49.4514001+00:00",
        "NotificationsTrayV4": "2023-07-05T20:50:47.0074016+00:00",
        "OfficeIntegration": "2021-02-23T19:17:55.8620868+00:00",
        "PackageMvCategories": "2022-08-10T12:46:34.8153439+00:00",
        "ReportingV2BP": "2023-03-31T19:44:42.4955497+00:00",
        "RestrictedCategories": "2023-09-20T23:11:14.6757201+00:00",
        "SSOManagement": "2021-10-01T03:43:10.3844981+00:00",
        "SearchInFileNameV3": "2023-09-21T11:58:55.8773605+00:00",
        "SergeyTimeMachineTest": "2021-12-08T20:42:05.2854457+00:00",
        "SergeyTimeMachineTest1": "2021-12-08T01:02:22.1547838+00:00",
        "UIEnhancements": "2023-08-22T18:52:07.0445271+00:00",
        "V4Users": "2019-02-06T21:17:24.3579074+00:00",
        "V5WebGallery": "2023-01-20T14:37:41.2180337+00:00",
        "V5_Use_Launch_Darkly_Flags": "2023-06-08T20:37:15.3279624+00:00",
        "AdvancedSearch": "2023-08-22T18:51:58.3125151+00:00",
        "AutodeskViewer": "2023-08-22T18:51:53.655176+00:00",
        "BrandedPortals": "2023-08-22T18:52:00.6331895+00:00",
        "EasyBuild": "2023-08-22T18:51:56.7653994+00:00",
        "FileNameVersioning": "2023-08-22T18:51:52.8796192+00:00",
        "ReadFromAzureSearch": "2023-08-22T18:51:37.3484896+00:00",
        "RequestDownloadOriginals": "2023-08-22T18:51:59.8626305+00:00",
        "SearchInCustomAttributes": "2023-08-22T18:52:05.4954122+00:00",
        "SearchInNestedCategories": "2023-08-22T18:52:02.3642013+00:00",
        "ShowAssetsBeforeFullyIngested": "2023-08-22T18:51:57.543954+00:00",
        "SoftDelete": "2023-08-22T18:52:06.2699696+00:00",
        "V3ServicesShutdown": "2023-08-22T18:51:59.0880725+00:00",
        "V4AssetHistory": "2023-08-22T18:51:38.1430359+00:00",
        "V4AssetReports": "2023-08-22T18:51:38.9175931+00:00",
        "V4Assets": "2023-08-22T18:51:39.6981476+00:00",
        "V4Attributes": "2023-08-22T18:51:40.4707062+00:00",
        "V4Categories": "2023-08-22T18:51:41.2412662+00:00",
        "V4Downloads": "2023-08-22T18:51:42.0168237+00:00",
        "V4Emails": "2023-08-22T18:51:42.7943789+00:00",
        "V4KeywordGroups": "2023-08-22T18:51:43.5669375+00:00",
        "V4KeywordSuggestion": "2023-08-22T18:51:44.3434942+00:00",
        "V4Keywords": "2023-08-22T18:51:45.1230494+00:00",
        "V4Libraries": "2023-08-22T18:51:45.9155962+00:00",
        "V4Lightboxes": "2023-08-22T18:51:46.7001479+00:00",
        "V4Passthrough": "2023-08-22T18:51:47.4717072+00:00",
        "V4ReadModels": "2023-08-22T18:51:48.2422671+00:00",
        "V4Searches": "2023-08-22T18:51:49.0188237+00:00",
        "V4Sharing": "2023-08-22T18:51:51.3295038+00:00",
        "V4Uploads": "2023-08-22T18:51:49.7863852+00:00",
        "Workfront": "2023-08-22T18:52:03.1817342+00:00",
        "WriteBothSearchIndexes": "2023-08-22T18:51:50.5569453+00:00",
        "attributesDropdownType": "2023-08-22T18:51:52.1060607+00:00",
        "customAttributesFullScreenFeatureFlag": "2023-08-22T18:52:04.7218542+00:00",
        "fullscreenComments": "2023-08-22T18:51:55.9908422+00:00",
        "fullscreenGridOverlay": "2023-08-22T18:51:55.2052899+00:00",
        "multiPageDocumentPreview": "2023-08-22T18:51:54.429733+00:00"
    },
    "activeDirectoryTenantId": null,
    "userIdleTimeOutInMinutes": 0,
    "deactivateVersioning": false,
    "oktaOrgUrl": null,
    "iamExternalIdentityProviderName": null,
    "overwriteGroups": null,
    "_links": {
        "self": "organizationalUnit",
        "functions": [
            "organizationalUnits",
            "currentOrganizationalUnit",
            "currentOrganizationalUnitPortals"
        ]
    }
}
```