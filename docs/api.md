# API Documentation

Read here about how to interact with the teamserver's API.

## Table of Contents

- [Web Hooks](#web-hooks)
  * [RegisterWebhook](#registerwebhook)
  * [RemoveWebhook](#removewebhook)
  * [ListWebhooks](#listwebhooks)
- [API Tokens](#api-tokens)
  * [CreateAPIToken](#createapitoken)
  * [DeleteAPIToken](#deleteapitoken)
- [Targets](#targets)
  * [CreateTarget](#createtarget)
  * [GetTarget](#gettarget)
  * [SetTargetFacts](#settargetfacts)
  * [ArchiveTarget](#archivetarget)
  * [ListTargets](#listtargets)
- [Sessions](#sessions)
  * [CreateSession](#createsession)
  * [GetSession](#getsession)
  * [SessionCheckin](#sessioncheckin)
  * [ListSessions](#listsessions)
- [Actions](#actions)
  * [CreateAction](#createaction)
  * [CreateGroupAction](#creategroupaction)
  * [GetAction](#getaction)
  * [CancelAction](#cancelaction)
  * [CancelGroupAction](#cancelgroupaction)
  * [ListActions](#listactions)
- [Groups](#groups)
  * [CreateGroup](#creategroup)
  * [GetGroup](#getgroup)
  * [AddGroupMembers](#addgroupmembers)
  * [RemoveGroupMembers](#removegroupmembers)
  * [ListGroups](#listgroups)
  * [DeleteGroup](#deletegroup)
- [Credentials](#credentials)
  * [CreateCredentials](#createcredentials)
  * [GetValidCredentials](#getvalidcredentials)
  * [InvalidateCredentials](#invalidatecredentials)
  * [ListCredentials](#listcredentials)
- [Logs](#logs)
  * [CreateLog](#createlog)
  * [ListLogs](#listlogs)

## Interacting with the API
### Overview
The Arsenal teamserver exposes a '/api' endpoint for users, applications, and c2 servers to integrate with. By submitting a POST request to this endpoint with JSON data, you can invoke API functions. The `method` field has been reserved to denote which API method to call. All other JSON keys will be passed as parameters to the function.

### Example Request
```
{
"method": "GetTarget",
"name": "Bob"
}
```

## Web Hooks
Not yet implemented.
### RegisterWebhook
#### Overview
#### Parameters
#### Example Request
#### Example Response
### RemoveWebhook 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListWebhooks
#### Overview
#### Parameters
#### Example Request
#### Example Response

## API Tokens
Not yet implemented.
### CreateAPIToken
#### Overview
#### Parameters
#### Example Request
#### Example Response
### DeleteAPIToken
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Targets
### CreateTarget 
#### Overview
This API call will create a Target object on the teamserver, which represents a server or machine that is being attacked.
#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                |                         
| :--------- | :----------- | :--------- | :------- | :--------------------------------------------- |
| name       | yes          | yes        | str      | A human-readable unique identifier.            |
| mac_addrs  | yes          | yes        | list<str>| A list of mac addresses. Each target must have a unique list. |
| facts      | no           | no         | dict     | Information that has been gathered about the target system. |

#### Example Success Response
```
{
"status": 200,
"error": False
}
```

### GetTarget
#### Overview
This API call will fetch Target information from the teamserver.
#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                |                         
| :--------- | :----------- | :--------- | :------- | :--------------------------------------------- |
| name       | yes          | yes        | str      | A human-readable unique identifier.            |

#### Example Success Response
```
{
"status": 200,
"error": False,
"target": {
  "name": "<target_name>",
  "status": "<target_status>",
  "lastseen": <timestamp>,
  "mac_addrs": ["Some Mac Addresses"],
  "facts": {
    "A Fact": "A Value"   
  },
  "sessions": [],
  "credentials": "Not yet implemented",
 }
}
```
### SetTargetFacts
#### Overview
Update the Target's fact dictionary. This will override any existing facts.

#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                |                         
| :--------- | :----------- | :--------- | :------- | :--------------------------------------------- |
| name       | yes          | yes        | str      | A human-readable unique identifier.            |
| facts      | yes          | no         | dict     | A dictionary with key value pairs to update.   |

#### Example Success Response
```
{
"status": 200,
"error": False,
"target": {
  "name": "<target_name>",
  "facts": {
    "A Fact": "A Value",
    "Old Fact": "Old Value"
  }
}
}
```
### ArchiveTarget
Not yet implemented.
#### Overview
#### Parameters
#### Example Request
#### Example Response

### ListTargets
#### Overview
Return a list of Target objects tracked by the teamserver.
#### Parameters
None.
#### Example Success Response
```
{
"status": 200,
"error": False,
"targets": {
  "target_id": {
      "name": "<target_name>",
      "status": "<target_status>",
      "lastseen": <timestamp>,
      "mac_addrs": ["Some Mac Addresses"],
      "facts": {
        "A Fact": "A Value"   
      },
      "sessions": [],
      "credentials": "Not yet implemented"
  }
}
}
```

## Sessions
### CreateSession 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetSession 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### SessionCheckin
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListSessions
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Actions
### CreateAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CreateGroupAction 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CancelAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CancelGroupAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListActions
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Groups
### CreateGroup 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetGroup
#### Overview
#### Parameters
#### Example Request
#### Example Response
### AddGroupMembers
#### Overview
#### Parameters
#### Example Request
#### Example Response
### RemoveGroupMembers
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListGroups
#### Overview
#### Parameters
#### Example Request
#### Example Response
### DeleteGroup
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Credentials
### CreateCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetValidCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### InvalidateCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Logs
### CreateLog
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListLogs
#### Overview
#### Parameters
#### Example Request
#### Example Response


