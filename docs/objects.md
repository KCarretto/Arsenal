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

### Session Statuses
| **Status** | **Description**                                                 |
| :--------- | :-------------------------------------------------------------- |
| active     | The Session has checked in within it's interval +/- it's delta. |
| missing    | The Session has missed it's expected check in time.             | 
| inactive   | The Session has not been seen in a significant amount of time.  |

## Action
## Group
## GroupAction
## Log
