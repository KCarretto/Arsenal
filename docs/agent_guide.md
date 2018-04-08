# Creating an Agent


## Table of Contents

- [Overview](#overview)
- [Agent Requirements](#agent-requirements)
    - [Target Identification Information](#target-identification-information)
    - [Session ID Tracking](#session-id-tracking)
    - [Config Tracking](#config-tracking)
    - [Action ID Tracking](#action-id-tracking)
    - [Action Types](#action-types)
    - [Fact Collection](#fact-collection)
- [Working with the Arsenal HTTP C2](#working-with-the-arsenal-http-c2)
    - [Initial Beacon](#initial-beacon)
    - [Standard Response](#standard-response)
    - [Standard Beacon](#standard-beacon)



## Overview
An Agent is a program that will be run on a target system, and will callback to a C2 that has been integrated with Arsenal. The goal of Arsenal is to allow Red Teamers to create their own Agents and C2 servers, but not need to deal with any of the backend management. This guide will cover how to create an Agent to work with the Arsenal HTTP C2 Server. It is recommended that you review the contents of this guide before attempting to create your own Agent / C2, because the framework does impose some light requirements on the Agent.

## Agent Requirements
### Target Identification Information
When an Agent calls back to a C2, it is important that the Teamserver is able to identify what machine / target the Agent is running on. IP Addresses alone cannot accurately identify a system, because NAT would cause many systems to appear the same from the C2's perspective. To solve this asset management problem, Arsenal allows the session to specify a `uuid` field, which is a string that can be set based on your environment that should be unique between targets. Our recommendation is to concatenate the machine-uuid and the mac address of the primary interface. It does not matter what value you use, as long as it is consistent across all agents, and is different between targets. If this criteria changes, a new target will be created on the teamserver automatically. The `MigrateSessions` API endpoint was created in order to attach all session objects from the old target object onto the newly created target object.

When a Session calls back with that criteria, identical to an already existing Target, the Session is associated with the already existing Target. If no Target with the given criteria exists, a new Target is created and is given an automatically generated name. 

_Upcoming Feature_: Target naming rules may be created to assign Target names in an automated fashion.

### Session ID Tracking
When an Agent calls back to the C2 for the first time, the C2 must register the newly created Session with the Arsenal Teamserver (If you are unfamiliar, we define a Session as a running instance of an Agent). It uses the Arsenal Teamserver API to do this. Once registered, the C2 is then provided with a Session ID that the Agent must keep track of, and send in every callback request. Without this, the Teamserver will be unable to track which Target a Session belongs to.

### Config Tracking
Each Agent should be configured with a (preferably JSON, or you will need to convert to JSON) config, that instructs the Agent on how to behave. The following configuration options must be supported, but you may add custom options as you see fit.
```json
{
  "servers": ["192.168.10.1", "129.25.24.23"],
  "interval": 123,
  "interval_delta": 5
}
```
* **servers** - Defines an array of C2 servers that the Agent should connect to. It is your decision on the failover process.<br>
* **interval** - The base number of seconds that an Agent should sleep for.<br>
* **interval_delta** - The maximum value that can be added or subtracted from the interval for randomization. This means that the actual interval delta should be calculated as interval + Random.Range(-interval_delta, interval_delta) where Random.Range would return a floating point value between the two parameters given (inclusive).<br>

### Action ID Tracking
When a Red Teamer wishes to run a command or perform some other action on the Target system, they queue an Action with the Arsenal Teamserver. Upon creation, that Action is given a unique identifier. Agents should receive this information with every command that they run, and upon completion, ensure that the Response also includes this Action identifier. Without this information, the Arsenal Teamserver cannot associate the given Response with an Action.

### Action Types
It is required that Agents support the following action types, or return a specified error when an unsupported action type is attempted.

| **Name**   | **Code** | **Description**                                                                                             | **Required Parameters**                                                                                          |
| :--------- | :------- | :---------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| config     | 0        | Set the agents configuration JSON<br> Agent is responsible for ignoring invalid JSON                        | config: {}  
| exec       | 1        | Run a command.                                                                                              | command: "string"<br>args: ["list", "of", "args"]                                                                |
| spawn      | 2        | Run a command and disown child process.<br>Do not wait for output.                                          | command: "string"<br>args: ["list", "of", "args"]                                                                |
| timed_exec | 3        | Run a command at a given time.<br>Based off of the time provided, not the system time.                      | command: ‘string’<br>args: [‘list’, ‘of’, ‘args’]<br>activate_time: 123123.23<br>current_time: 123122.01 |
| timed_spawn | 4      | Spawn a process at the given time.<br>A combination of action types 2 and 3. |
| upload     |   5      | Upload a file to the remote system.                   | remote_path: "/target/destination/path"<br>file: [byte array of file contents]                                      |
| download   | 6        | Retrieve a file from the target system.                                                                     | remote_path: "/target/source/path"                                                                               |
| gather     | 7        | Gather and report updated facts.                                                                            | subset: "all"                                                                                                    |                                                                                                     |
| reset      | 999      | Reinitialize session.<br>Agent should perform another initial beacon.<br> C2 will provide a new Session ID. | N/A                                                                                                              |
More information on Actions can be found in the database.md documentation file.

### Fact Collection
It is recommended that the Agent be capable of collecting facts about a Target system for ease of use. While the only two required facts are the Target's hostname and MAC addresses, many other facts are useful for collection. Please see the database.md documentation's Target section for more information on the default factsets.

## Working with the Arsenal HTTP C2

The existing Arsenal HTTP C2 utilizes JSON as a communication Format. The JSON tokens that it will receive from and send to the Agent are as follows (in order):

### Initial Beacon
```json
{
  "session_id": "",
  "config": {
    "interval": 60,
    "interval_delta": 120,
    "servers": ["10.0.0.1", "https://something.com"] 
  },
  "facts": {  
    "hostname": "host",
    "interfaces":  [
      {
        "name": "lo",
        "mac_addr": "AA:BB:CC:DD:EE:FF",
        "ip_addrs": ["127.0.0.1","127.0.0.2"]
      },
      {
        "name": "eth0",
        "mac_addr": "FF:EE:DD:CC:BB:AA",
        "ip_addrs": ["192.168.0.1","64.1.1.5"]
      }
    ]
  }
}
```
* **session_id** - Must be empty string or not present in the initial beacon. The C2 will respond with a session_id that the Agent should keep track of, and send with all future call backs.<br>
* **config** - This is a dictionary that represents the agent's initial configuration.
* **facts** - A dictionary containing facts about the target system. The only required fact is "interfaces", which should be provided in the format shown above, however it is recommended that you collect at least the "min" subset on initial beacon (Which can be found under the target section of database.md Documentation). It is also likely that the "hostname" fact will be used for target auto-naming, so it is highly recommended that you collect this fact as well.<br>

### Standard Response
The following is sent in response to an Agent's beacon. The same response format is used for both initial and standard beacons.
```json
{
  "session_id": "Your Session ID",
  "actions": [
    {
      "action_id": "some action ID to track",
      "command": "echo",
      "args": ["hi dad"],
      "action_type": 0
    }, 
    {
      "action_id": "Configuration update action id",
      "action_type": 6,
      "config": {
        "interval": 10,
        "servers": ["10.10.10.10", "1.2.3.4"]
      }
    }
  ]
}
```
* **session_id** - The unique identifier of the session.<br>
* **actions** - An array of Action dictionaries.
  * **action_id** - The unique identifier of the Action. Use this when generating a Response dictionary for the Action.<br>
  * **action_type** - The integer identifier of the type of action being performed. See the above table, or the Action section in database.md for more information.<br>
  * **command** - This is a parameter for several action types, and may not always be included. Please see the Action section in database.md for more information on how Action types should be handled.<br>
  * **args** - This is a parameter for several action types, and may not always be included. Please see the Action section in database.md for more information on how Action types should be handled.<br>
  * **config** - Any key / value pairs in this dictionary should override the Agent's existing configuration settings. It is the Agent's responsibility to validate that these configuration options are valid. Please see the Action section in database.md for more information on how Action types should be handled.<br>

### Standard Beacon
After the session has been initialized, it should respond with the format below:
```json
{
  "session_id": "Your assigned SessionID",
  "responses": [ 
    {
      "action_id": "The action identifier this is in  response to",
      "start_time": 123.2132,
      "end_time": 124.2132,
      "stdout": "bin boot dev etc home lib lib64 mnt opt  proc root run usr var",
      "stderr": "",
      "error": false
    }
  ],
  "facts": {},
  "config": {}
}
```
* **session_id** - Represents the unique session identifier given by the C2.<br>
* **responses** - An array of Response dictionaries. <br>
  * **action_id** - Each Response should correspond to the given action_id.<br>
  * **start_time** - The timestamp on the local system that the action started.<br>
  * **end_time** - The timestamp on the local system that the action completed.<br>
  * **stdout** - The output of the command run. If the action_type does not require a response, just leave this empty.<br>
  * **stderr** - The error output of the command run. If there is no error, or the action_type does not require a response, just leave this empty.
  * **error** - This is a boolean that represents whether the action sucessfully completed or not.<br>
* **facts** - Any key / value pairs in this dictionary will override existing key / value pairs associated with the target. This should be returned whenever a change occurs, or in response to the "gather" action_type.<br>
* **config** - This should only be included when a change has been made to the Agent's configuration, and will be used to verify that the Agent has the correct configuration. It is never required that this field be sent.<br>
