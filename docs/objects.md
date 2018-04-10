# Objects Documentation
This will outline the contents of each object, as well as detail any special properties or other important information about each object.

## Target
### Overview
A Target represents a system to attack.

### Example
```
{
"name": "Target A",
"status": "inactive",
"lastseen": 1522096823,
"mac_addrs": ["AA:BB:CC:DD:EE:FF", "DD:BB:CC:EE:AA:FF"],
"facts": {
  "hostname": "example",
  "os_arch": "x86_64",
},
"sessions": [ <Session Object> ],
}
```

### Field Description
| **Name**   | **Unique** | **Type**   | **Description**                                                   |
| :--------- | :--------- | :--------- | :---------------------------------------------------------------- |
| name       | yes        | str        | A human-readable unique identifier.                               |
| status     | no         | str        | The current status of the Target. This will assume the value of the "best" status of any of the Target's sessions.|
| lastseen   | no         | float      | The timestamp of the last time the Target had an Agent call back. |
| mac_addrs  | yes        | list<str>  | A list of mac addresses. Each target must have a unique list.     |
| facts      | no         | dict       | Information that has been gathered about the target system.       |
| sessions   | no         | list<dict> | A list of Session objects associated with this Target.            |

## Session
### Overview
A Session represents a running instance of an Agent on the Target system.

### Example 
```
{
"session_id": "ac198dd6-94be-4b6a-988f-dd9e0ba61f0e",
"target_name": "Target A",
"status": "inactive",
"timestamp": 1522096823,
"config": {
  "interval": 600,
  "interval_delta": 60,
  "servers": [ "8.8.8.8" ],
  "some_configuration_option": True
}
}
```

### Field Description
| **Name**    | **Unique** | **Type**   | **Description**                                                   |
| :---------- | :--------- | :--------- | :---------------------------------------------------------------- |
| session_id  | yes        | str        | A  unique identifier.                                             |
| target_name | no         | str        | The human-readable unique identifier of the associated Target.    |
| status      | no         | str        | The current status of the Session. See below for details.         |
| timestamp   | no         | float      | The time of the Session's last check in.                          |
| config      | no         | dict       | Contains the current configuration information for the Session.   |
| agent_version | no       | str        | The agent version provided by the agent. May be None.             |

### Session Statuses
| **Status** | **Description**                                                 |
| :--------- | :-------------------------------------------------------------- |
| active     | The Session has checked in within it's interval +/- it's delta. |
| missing    | The Session has missed it's expected check in time.             | 
| inactive   | The Session has not been seen in a significant amount of time.  |

## Action
### Overview
An Action represents something for an Agent to execute, such as a command or configuration update.
### Example
```
{
"action_id": "14a10277-9d89-40f6-8174-4c8dc6fbea22",
"action_string": "exec ls",
"action_type": 1,
"args": [],
"bound_session_id": "",
"command": "ls",
"complete_time": None,
"queue_time": 1521675403.4228077,
"sent_time": None,
"session_id": None,
"status": "stale",
"target_name": "test"
}
```
### Field Description
| **Name**         | **Unique** | **Type**   | **Description**                                                   |
| :--------------- | :--------- | :--------- | :---------------------------------------------------------------- |
| action_id        | yes        | str        | A  unique identifier.                                             |
| action_string    | no         | str        | The Arsenal Action Syntax action to perform.                      |
| action_type      | no         | int        | The parsed type of the Action.                                    |
| bound_session_id | no         | str        | Restrict Action such that only this Session may retrieve the Action. Used for configuration updates. |
| session_id       | no         | str        | The unique identifier of the Session that has retrieved the Action, or None if unretrieved. |
| queue_time       | no         | float      | The timestamp of when the Action was queued.                      |     
| sent_time        | no         | float      | The timestamp of when the Action was sent to a Session.           |     
| complete_time    | no         | float      | The timestamp of when the Action response was recieved.           |    
| status           | no         | str        | The current status of the Action. See below for details.          |    
| command          | no         | str        | **PARAMETER** Only included for execution based Action types. A command to perform. |
| args             | no         | list<str>  | **PARAMETER** Only included for execution based Action types. A list of string arguments to provide to the given command. |

### Action Statuses
| **Status** | **Description**                                                 |
| :--------- | :-------------------------------------------------------------- |
| cancelled  | The Action has been cancelled and will not be sent.             |
| queued     | The Action is queued for a Target, and awaiting retrieval.      |
| stale      | The Action has been queued for a significant amount of time.    |
| sent       | The Action has been sent to a Session.                          |
| failing    | The Action has been sent to a Session that is now missing.      |
| failed     | The Action has been sent to a Session that is now inactive.     |
| error      | The Action has a submitted response, but there was an error while executing the Action. |
| complete   | The Action has a submitted response, and has been completed successfully. |


## Group
### Overview
A Group represents a collection of Targets.
### Example
```
{
"name": "Team 1",
"whitelist_members": ["Target A", "Target B"],
"blacklist_members": ["Target C"],
}
```
### Field Description
| **Name**          | **Unique** | **Type**   | **Description**                                                   |
| :---------------- | :--------- | :--------- | :---------------------------------------------------------------- |
| name              | yes        | str        | A human-readable unique identifier.                               |
| whitelist_members | no         | list<str>  | A list of Target members of the Group (Will change once automember rules are implemented) |
| blacklist_members | no         | list<str>  | A list of Targets that have been blacklisted from the Group.      |

## GroupAction
### Overview
A GroupAction tracks Action objects that were queued for a Group of Targets.
### Example
```
{
"group_action_id": "7447dbac-e974-4833-a407-e1e2c05f962c",
"action_string": "exec ls -al",
"status": "in progress",
"action_ids": ["14a10277-9d89-40f6-8174-4c8dc6fbea22"],
"actions": [ <Action Object> ]
}
```
### Field Description
| **Name**         | **Unique** | **Type**   | **Description**                                                   |
| :--------------- | :--------- | :--------- | :---------------------------------------------------------------- |
| group_action_id  | yes        | str        | A unique identifier.                                              |
| action_string    | no         | str        | The Arsenal Action Syntax action to perform.                      |
| status           | no         | str        | The current status of the Action. See below for details.          |
| action_ids       | no         | list<str>  | An array containing Action ID's for each tracked Action.          |
| actions          | no         | list<dict> | An array of associated Action Objects.                            |

### Group Action Statuses
| **Status**    | **Description**                                                 |
| :------------ | :-------------------------------------------------------------- |
| cancelled     | The Group Action has been cancelled.                            |
| queued        | All Actions are still awaiting retrieval.                       |
| in progress   | One or more Actions have been sent.                             |
| mixed success | Some Actions have been completed successfully.                  |
| success       | All Actions were completed successfully.                        |
| failed        | No Actions were completed successfully.                         |

## Log
### Overview
A Log object represents an entry of a log message that was submitted to the log server.

### Example
```
{
"timestamp": 1522109247.231,
"application": "teamserver-internal",
"level": "DEBUG",
"message": "Calling API method CancelAction"
}
```

### Field Jobs
| **Name**         | **Unique** | **Type**   | **Description**                                                   |
| :--------------- | :--------- | :--------- | :---------------------------------------------------------------- |
| timestamp        | no         | float      | The timestamp when the log was submitte.                          |
| application      | no         | str        | The application that submitted the log.                           |
| level            | no         | str        | The level that the message was logged at. (DEBUG, INFO, WARN, CRIT, FATAL)|
| message          | no         | str        | The message being recorded.                                       |

