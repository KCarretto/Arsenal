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
### RemoveWebhook 
### ListWebhooks

## API Tokens
Not yet implemented.
### CreateAPIToken
### DeleteAPIToken

## Targets
### CreateTarget 
#### Overview
This API call will create a Target object on the teamserver, which represents a server or machine that is being attacked.
#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| name       | yes          | yes        | str      | A human-readable unique identifier.                           |
| mac_addrs  | yes          | yes        | list<str>| A list of mac addresses. Each target must have a unique list. |
| facts      | no           | no         | dict     | Information that has been gathered about the target system.   |

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
"target": <Target Object>
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
  "target_id": <Target Object>
}
```

## Sessions
### CreateSession 
#### Overview
This API call creates a new instance of an Agent on a given Target. We call this instance a Session.
#### Parameters
| **Name**      | **Required** | **Unique** | **Type**  | **Description**                                |                       
| :------------ | :----------- | :--------- | :-------- | :--------------------------------------------- |
| mac_addrs     | yes          | yes        | list<str> | The mac addresses of the system that the agent was run on. This is used to associate the Session with a target.  |   
| servers       | no           | no         | list<str> | The C2 servers that the Agent is configured with. |
| interval      | no           | no         | float     | The amount of time a Session will wait inbetween check ins. |
| interval_delta| no           | no         | float     | The random delta to add to each interval (+ or -). |
| config_dict   | no           | no         | dict      | Any additional configuration information from the Agent. |

#### Example Response
```
{
"status": 200,
"error": False,
"session_id": "<session_id>"
}
```
### GetSession 
#### Overview
This API call retrieves Session information from the teamserver.
#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                |                         
| :--------- | :----------- | :--------- | :------- | :--------------------------------------------- |
| session_id | yes          | yes        | str      | A unique identifier.                           |

#### Example Response
```
{
"status": 200,
"error": False,
"session": <Session Object>
}
```

### SessionCheckin
#### Overview
This API call will check in a Session, and update appropriate timestamps. This will allow the Session to submit Responses to any Actions it was tasked with, and will also provide any new Actions that the Session should perform.
#### Parameters
#### Parameters
| **Name**   | **Required** | **Unique** | **Type** | **Description**                                |                         
| :--------- | :----------- | :--------- | :------- | :--------------------------------------------- |
| session_id | yes          | yes        | str      | A unique identifier.                           |
| responses  | no           | no         | list     | 
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
This API call queues an Action with the teamserver, and assigns it to a given Target. The first Session to check in for a given Target will receive any Actions in that Target's queue. On the next check in, the Session will submit responses for any Actions that were queued on the previous round. Special options may be given in the `action_string` parameter to specify how the Action is handled and executed.

#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| target_name      | yes          | yes        | str      | The name of the Target to queue the Action for.               |
| action_string    | yes          | no         | str      | Conforms to Arsenal Action Syntax.                            |
| bound_session_id | no           | yes        | str      | Optionally specify which Session the Action will be given to. |

#### Example Success Response
```
{
"status": 200,
"error": False,
"action_id": "<action_id>"
}
```

### CreateGroupAction
#### Overview
This API call queues Actions for an entire Group of Targets. It will provide an identifier for tracking the progress of each created Action.

#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| group_name       | yes          | yes        | str      | The name of the Group to queue the Actions for.               |
| action_string    | yes          | no         | str      | Conforms to Arsenal Action Syntax.                            |

#### Example Success Response
```
{
"status": 200,
"error": False,
"group_action_id": "The group action identifier."
}
```

### GetAction
#### Overview
Retrieve information about an Action object on the teamserver.

#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| action_id        | yes          | yes        | str      | The unique identifier of the Action.                          |

#### Example Success Response
```
{
"status": 200,
"error": False,
"action": <Action Object>
}
```

### GetGroupAction
#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| group_action_id  | yes          | yes        | str      | The unique identifier of the Group Action.                    |

#### Example Success Response
```
{
"status": 200,
"error": False,
"action": <GroupAction Object>
}
```

### CancelAction
#### Overview
This API call attempts to cancel an Action before it is sent. This will fail if the Action is in any state other than queued.
#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| action_id        | yes          | yes        | str      | The unique identifier of the Action.                          |

#### Example Success Response
```
{
"status": 200,
"error": False
}
```

### CancelGroupAction
#### Overview
This API call attempts to cancel all Actions associated with a Group Action. This will fail if an Action is in any state other than queued.

#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| group_action_id  | yes          | yes        | str      | The unique identifier of the Group Action.                    |

#### Example Success Response
```
{
"status": 200,
"error": False
}
```

### ListActions
#### Overview
This API call will provide a list of Action objects.
#### Parameters
None

#### Example Success Response
```
{
"status": 200,
"error": False,
"actions": [ <Action Object> ]
}
```

### ListGroupActions
#### Overview
This API call will provide a list of Group Action objects.
#### Parameters
None

#### Example Success Response
```
{
"status": 200,
"error": False,
"group_actions": [ <GroupAction Object> ]
}
```

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
Not yet implemented.
### CreateCredentials
### GetValidCredentials
### InvalidateCredentials
### ListCredentials


## Logs
### CreateLog
#### Overview
Add a log entry to the log server. This is mostly useful for Agents and C2 servers, but may be utilized by any application that wishes to have a centralized and easy place to view logs.
#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| application      | yes          | no         | str      | The name of the application submitting the log.               |

#### Example Response
```
{
"status": 200,
"error": False
}
```
### ListLogs
#### Overview
View log entries that have been stored on the log server. You may filter by application, or timestamps.
#### Parameters
| **Name**         | **Required** | **Unique** | **Type** | **Description**                                               |
| :--------------- | :----------- | :--------- | :------- | :------------------------------------------------------------ |
| application      | no           | no         | str      | The name of the application submitting the log to filter for. |
| since            | no           | no         | float    | Filter for any logs before this timestamp.                    |
| include_archived | no           | no         | bool     | Whether archived logs should be included in the search.       |

#### Example Response
```
{
"status": 200,
"error": False,
"logs": [ <Log Object> ]
}
```

