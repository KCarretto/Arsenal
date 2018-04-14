# User Guide
This guide will demonstrate proper usage of the Arsenal framework.

## Terminology
### Overview
When attacking with Arsenal, it's important to have a solid understanding of some of the terminology used by the framework. The first thing to note is that systems you're aiming to compromise are refered to as _targets_. A target will contain information about the underlying machine that your bots / agents are running on.

An _agent_ refers to a payload that is deployed on the target system, and is integrated with Arsenal. A running instance of an agent is refered to as a _session_. Think of it as if an agent were the executable, and a session were the running process. Each session may contain it's own configuration options, and you can closely examine session information using the `GetSession` API method and specifying the `session_id` of the session you wish to learn more about. If you're not sure what `session_id` to specify, you can perform a filtered search using `ListSessions`.

Arsenal makes attacking easy with _groups_, which are simply collections of targets. Groups can be dynamically constructed from target information using "Automember Rules", which are managed by the `AddGroupRule` and `RemoveGroupRule` API methods. Groups allow interacting with multiple targets easy, and you will read more about the `CreateGroupAction` API method below.

## Commanding Agents
### Overview
Interacting with target systems is primarily done using the `CreateAction` and `CreateGroupAction` API methods.

#### Creating Simple Actions
Each time `CreateAction` is run, an action will be queued for the target system, and will be retrieved by the first session to check in from that target. You may specify the `quick` parameter, which will force the action to be bound to the session with the lowest interval on the target. After creating an action, you will be provided with an `action_id` that can be used to track your action. This is a unique identifier for the action. You may specify a custom `action_id` for easier reference, however keep in mind that it still must be unique. You may easily view action information and output using the `GetAction` API method, and specifying the correct `action_id`.

#### Creating Group Actions
The `CreateGroupAction` API method will automatically create an action for each target in a group. It will then track the status of each action for you, and will have a it's own status to describe the current state of the tracked actions. By using the `GetGroupAction` API method, you can easily see the status of each created action, as well as retrieve `action_id` information. The `action_id` of each action may be passed to `GetAction` as normal in order to see action output.

#### Slack Integration
By default, Arsenal comes equipped with a slack integration that can be configured to send notifications to slack when events occur. One such event is the `action_complete` event, which can notify you when actions are completed.

### Action Syntax
A table of action types and their required parameters can be found in the `agent_guide.md` documentation file. The goal of this documentation is to simply show you how to use each action.

#### Config Actions
Config actions allow you to update a session's configuration. Usually this means that you will want to specify a `bound_session_id` when creating an action, such that you can control which session performs the action.


##### Syntax
```
syntax: config [options]
                -i, --interval: Set the session's interval
                -d, --delta: Set the session's interval delta
                -s, --servers: Set a list of the sessions servers
                -c, --config: Set the configuration dictionary
```

##### Example Usage
`config -i 20` will update the session's interval to 20 seconds.
`config -s http://redteam-arsenal.com http://notgoogle.com` will update the agent's servers.

#### Exec Actions
Exec actions allow you to run a command on target systems. You will receive the `stderr` and `stdout` of these actions. You may also force actions to be run at a specific time, or cause them to spawn in separate processes.

##### Syntax
```
syntax: exec [options] <command> [args]
                -t, --time: Set a timestamp for the command to execute
                -s, --spawn: Cause the action to fork and spawn a process.
                             WARN: In many cases, you may not receive command output.
```

##### Example Usage
`exec cmd.exe /c calc.exe` Run calc.exe on the target system.
`exec -t 1523598706 ls -al /etc/ssh` List directory contents at the given time. Note: This must be _before_ the rest of the command, otherwise it will be passed to the command instead (i.e. "ls").

#### File Transfer Actions
Are not currently implemented, but will be available in the next stable release.

#### Gather Action
The `gather` action allows you to instruct a session to gather information (facts) about a target system. This information is then stored in the target's object, and is visible through the `GetTarget` API method (`GetTarget --show-facts` in the python client). 

##### Syntax
```
syntax: gather [options]
                -s, --subset: Specify a subset of facts to gather.
```

##### Example Usage
`gather` Gather all facts on the target system.

#### Reset Action
The `reset` action forces a Session to reinitialize with the teamserver. This is most useful when the teamserver loses data, and no longer recognizes the session's `session_id`. Good C2 servers will automatically send this action to agents if the agent's provided `session_id` does not exist on the teamserver.

## FAQ
### What is the best way to see what groups a target is in?
`GetTarget` will show you this information.

### How do I see the output of an Action?
Use the `GetAction` API method, and specify the proper `action_id`

### What is an action "owner"
The owner of the action is simply the user that created it. This is done automatically based on your login credentials, so no need to worry! 

### It takes too long for actions to come back, I just want to ssh
Why not just spawn a new version of the agent using the `exec` action, and then use the `--quick` option to ensure your actions return as fast as possible. You will have most of the speed of an ssh session, however you will also be significantly stealthier than logging into the target system. Please keep in mind that this is more noisy, and so you may wish to point the low interval session at a different c2 in case of detection.

### What can I do if I don't remember an `action_id`
Use the `ListActions` API method to view actions. To speed things up, you may also filter by various properties (i.e. specify your username to only see your actions). Check out the `api.md` documentation for more information. You could also use the `GetTarget` API call to see recently queued actions for a given target.

### What do these statuses mean?
Please see the `objects.md` documentation for more information on statuses.

### Do I need to manually add each target to a group?
Nope! Check out the `AddGroupRule` API method.
