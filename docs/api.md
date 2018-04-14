# API Documentation

Read here about how to interact with the teamserver's API.

## Table of Contents
- [AddGroupMember](#addgroupmember)
- [AddGroupRule](#addgrouprule)
- [AddRoleMember](#addrolemember)
- [BlacklistGroupMember](#blacklistgroupmember)
- [CancelAction](#cancelaction)
- [CancelGroupAction](#cancelgroupaction)
- [CreateAction](#createaction)
- [CreateAPIKey](#createapikey)
- [CreateGroup](#creategroup)
- [CreateGroupAction](#creategroupaction)
- [CreateLog](#createlog)
- [CreateRole](#createrole)
- [CreateSession](#createsession)
- [CreateTarget](#createtarget)
- [CreateUser](#createuser)
- [DeleteGroup](#deletegroup)
- [DeleteRole](#deleterole)
- [DeleteUser](#deleteuser)
- [DuplicateAction](#duplicateaction)
- [GetAction](#getaction)
- [GetAgent](#getagent)
- [GetCurrentContext](#getcurrentcontext)
- [GetGroup](#getgroup)
- [GetGroupAction](#getgroupaction)
- [GetRole](#getrole)
- [GetSession](#getsession)
- [GetTarget](#gettarget)
- [GetUser](#getuser)
- [ListActions](#listactions)
- [ListAgents](#listagents)
- [ListAPIKeys](#listapikeys)
- [ListGroupActions](#listgroupactions)
- [ListGroups](#listgroups)
- [ListLogs](#listlogs)
- [ListRoles](#listroles)
- [ListSessions](#listsessions)
- [ListTargets](#listtargets)
- [ListUsers](#listusers)
- [ListWebhooks](#listwebhooks)
- [MigrateTarget](#migratetarget)
- [RebuildGroupMembers](#rebuildgroupmembers)
- [RegisterAgent](#registeragent)
- [RegisterWebhook](#registerwebhook)
- [RemoveGroupMember](#removegroupmember)
- [RemoveGroupRule](#removegrouprule)
- [RemoveRoleMember](#removerolemember)
- [RenameTarget](#renametarget)
- [RevokeAPIKey](#revokeapikey)
- [SessionCheckIn](#sessioncheckin)
- [SetTargetFacts](#settargetfacts)
- [UnblacklistGroupMember](#unblacklistgroupmember)
- [UnregisterAgent](#unregisteragent)
- [UnregisterWebhook](#unregisterwebhook)
- [UpdateRolePermissions](#updaterolepermissions)
- [UpdateSessionConfig](#updatesessionconfig)
- [UpdateUserPassword](#updateuserpassword)

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

## API Method Documentation
## AddGroupMember

### Overview
    This whitelists a member into a group. This means that
    regardless of properties, the member will be a part of the
    group.

### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to add. <str>




## AddGroupRule

### Overview
    Add a membership rule for the group.

### Parameters
    name:       The name of the group to modify. <str>
    attribute:  The attribute to build membership based on. You may access fields using
                    the '.' operator, for example: 'facts.interfaces'. Each attribute is
                    converted into a str for regex matching. <str>
    regex:      The inclusion regex, targets with matching attributes are included as
                    group members. <str>
    rule_id:    Optionally specify a unique name for the rule. <str>




## AddRoleMember

### Overview
    Add a user to a role.

### Parameters
    role_name:  The name of the role to modify. <str>
    username:   The name of the user to add. <str>




## BlacklistGroupMember

### Overview
    Blacklist a target from ever being a member of a group.

### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>




## CancelAction

### Overview
    Cancels an action if it has not yet been sent.
    This will prevent sessions from retrieving it.

### Parameters
    action_id: The action_id of the action to cancel. <str>




## CancelGroupAction

### Overview
    Cancels all actions associated with a group action (only if status is queued).

### Parameters
    group_action_id:    The unique identifier associated with the group action. <str>




## CreateAction

### Overview
    This API function creates a new action object in the database.

### Parameters
    target_name (unique):           The name of the target to perform the action on. <str>
    action_string:                  The action string that will be parsed into an action. <str>
    bound_session_id (optional):    This will restrict the action to only be retrieved
                                        by a specific session. <str>
    action_id (optional, unique):   Specify a human readable action_id. <str>
    quick (optional):               Only send to the target's fastest session. <bool>
                                        Default: False. This overrides bound_session_id




## CreateAPIKey

### Overview
    Create an API key for a user. Only administrators may create api keys for other users.

### Parameters
    allowed_api_calls (optional): A list of API calls that the API token can perform. If left
                                  empty, all of the user's permissions will be granted to the
                                  token. This may not specify any API call that the user does not
                                  currently have access to. <list>
    user_context (optional, requires administrator) <str>




## CreateGroup

### Overview
    This function creates a group object in the database.

### Parameters
    name (unique):  A unique and human readable identifier for the group. <str>




## CreateGroupAction

### Overview
    Creates an action and assigns it to a group of targets. Each target
    will complete the action, and the statuses of each action will be
    easily accessible through the created group action document.

### Parameters
    group_name:                         The name of the group to create an action for. <str>
    action_string:                      The action to perform on the targets. <str>
    group_action_id (optional, unique): Specify a human readable group_action_id. <str>
    quick (optional):                   Only send to the target's fastest session.
                                            Default: False. <bool>




## CreateLog

### Overview
    Log an entry (if current log level deems necessary)

### Parameters
    application:    The application that is requesting to log a message. <str>
    level:          The log level that the message is at (LOG_LEVELS in config.py). <str>
    message:        The message to log. <str>




## CreateRole

### Overview
    Create a role.

    name (unique):      The name of the role.
    allowed_api_calls:  The list of API methods that users with this role may invoke.
    users (optional):   Specify a list of users to add to the role.




## CreateSession

### Overview
    This API function creates a new session object in the database.

### Parameters
    target_uuid:                The unique identifier of the target. <str>
    servers (optional):         Which servers the agent will initially be configured with.
                                    <list[str]>
    interval (optional):        The interval the agent will initially be configured with. <float>
    interval_delta (optional):  The interval delta the agent will initially be
                                    configured with. <float>
    config_dict (optional):     Any other configuration options that the agent is initially
                                    configured with. <dict>
    facts (optional):           An optional facts dictionary to update the target with. <dict>
    agent_version (optional):   The agent_version to register. <str>




## CreateTarget

### Overview
    This API function creates a new target object in the database.

### Parameters
    name (unique):      The name given to the target. <str>
    uuid (unique):      The unique identifier of the target. <str>
    facts (optional):   A dictionary of key,value pairs to store for the target. <dict>




## CreateUser

### Overview
    Create a user.

### Parameters
    username (unique):  The username of the user. <str>
    password:           The desired password for the user. <str>




## DeleteGroup

### Overview
    Delete a group from the database.

### Parameters
    name:   The unique identifier for the group to delete. <str>




## DeleteRole

### Overview
    Delete a role.

### Parameters
    role_name:  The name of the role to delete. <str>




## DeleteUser

### Overview
    Delete a user.

### Parameters
    username:   The name of the user to delete. <str>




## DuplicateAction

### Overview
    This API function is used to queue an identical action to the given action_id.

### Parameters
    action_id: The unique identifier of the action to clone. <str>




## GetAction

### Overview
    Retrieves an action from the database based on action_id.

### Parameters
    action_id: The action_id of the action to query for. <str>




## GetAgent

### Overview
    This function retrieves an Agent from the database.

### Parameters
    agent_version: The agent version string to search for. <str>




## GetCurrentContext

### Overview
    Return the currently authenticated username.




## GetGroup

### Overview
    Retrieves a group from the database based on name.

### Parameters
    name:   The name of the group to query for. <str>




## GetGroupAction

### Overview
    Retrieves a group action from the database based on the group_action_id.

### Parameters
    group_action_id:    The group action identifier to query for. <str>




## GetRole

### Overview
    Retrieve a role object.

### Parameters
    role_name: The name of the role to fetch. <str>




## GetSession

### Overview
    This API function queries and returns a session object with the given session_id.

### Parameters
    session_id: The session_id to search for. <str>




## GetTarget

### Overview
    This API function queries and returns a target object with the given name.

### Parameters
    name:                           The name of the target to search for. <str>
    include_status (optional):      Should status be included, default: True. <bool>
    include_facts (optional):       Should facts be included, default: False. <bool>
    include_sessions (optional):    Should sessions be included, default: False. <bool>
    include_credentials (optional): Should credentials be included, default: False. <bool>
    include_actions (optional):     Should actions be included, default: False. <bool>
    include_groups (optional):      Should groups be included, default: False. <bool>




## GetUser

### Overview
    Retrieve a user object.

### Parameters
    username:                       The name of the user object to fetch. <str>
    include_roles (optional):       Optionally include roles. default: False. <bool>
    include_api_calls (optional):   Display the set of permitted API calls for the user.
                                        default: True. <bool>




## ListActions

### Overview
    This API function will return a list of action documents.
    Filters are available for added efficiency.

### Parameters
    owner (optional):       Only display actions owned by this user. <str>
    target_name (optional): Only display actions for given target. <str>
    limit (optional):       Optionally limit how many values may be returned. <int>
    offset (optional):      The position to start listing from. <int>




## ListAgents

### Overview
    This function returns a list of agent documents.




## ListAPIKeys

### Overview
    Lists the permissions of API keys that you own. This will not return the API key itself.

### Parameters
    user_context (optional, requires administrator)




## ListGroupActions

### Overview
    This API function will return a list of group action documents.
    It is highly recommended to avoid using this function, as it
    can be very expensive.




## ListGroups

### Overview
    List all groups that currently exist.
    WARNING: This will be quite an expensive operation.




## ListLogs

### Overview
    Show filtered log entries

### Parameters
    application (optional):         The application to filter for. <str>
    since (optional):               The timestamp that logs must be newer than. <float>
    include_archived (optional):    Should archived messages be included. Default: False. <bool>
    levels (optional):              The level to filter for. <list[str]>




## ListRoles

### Overview
    Return a list of roles.




## ListSessions

### Overview
    This API function will return a list of session documents.
    It is highly recommended to avoid using this function, as it
    can be very expensive.




## ListTargets

    This API function will return a list of target documents.

    include_status (optional):      Should status be included, Default: True. <bool>
    include_facts (optional):       Should facts be included, Default: False. <bool>
    include_sessions (optional):    Should sessions be included, Default: False. <bool>
    include_credentials (optional): Should credentials be included, Default: False. <bool>
    include_actions (optional):     Should actions be included, Default: False. <bool>
    include_groups (optional):      Should groups be included, Default: False. <bool>




## ListUsers

### Overview
    Return a list of users.

### Parameters
    include_roles (optional):       Optionally include roles. Default: False. <bool>
    include_api_calls (optional):   Display the set of permitted API calls for the user.
                                        default: True. <bool>




## ListWebhooks

### Overview
    This API function will return a list of a user's webhooks.

### Parameters
    user_context (optional, requires administrator) <str>




## MigrateTarget

### Overview
    This API function will move all sessions from one target, to another. It will then delete the
    old target and rename the new target after the old one.

### Parameters
    old_target: The name of the outdated target. <str>
    new_target: The name of the new target to migrate to. <str>




## RebuildGroupMembers

### Overview
    Recalculate group members.

### Parameters
    name (optional):    Optionally specify a single group to rebuild membership for. <str>




## RegisterAgent

### Overview
    This API function registers an agent version with the teamserver. This is used to denote
    what action types an agent supports, to avoid unsupported action types from being sent to
    an agent. If an unregistered agent calls back, there will be no restrictions on what action
    types it receives. If an agent_version already exists, it will be overwritten by the new
    registration.

### Parameters
    agent_version (unique): The agent version string to update capabilities for. <str>
    supported_actions:      A list of supported action types. i.e. [0, 1, 3]. <list>




## RegisterWebhook

### Overview
    This API function will register a new webhook.

### Parameters
    post_url (required):        The url that the data should be sent via JSON in a POST request.
                                    <str>
    event_triggers (required):  A list of events to subscribe to. <str>




## RemoveGroupMember

### Overview
    Removes a target from a group's membership whitelist.

### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>




## RemoveGroupRule

### Overview
    Remove an automembership rule for the group.

### Parameters
    name:       The name of the group to modify. <str>
    rule_id:    The unique identifier of the rule to remove. <str>




## RemoveRoleMember

### Overview
    Remove a user from a role.

### Parameters
    role_name:  The name of the role to modify. <str>
    username:   The name of the user to remove. <str>




## RenameTarget

### Overview
    This API function will rename a target.

### Parameters
    name:       The name of the target to search for. <str>
    new_name:   The new name to assign the target. <str>




## RevokeAPIKey

### Overview
    Revoke a user's API key.

### Parameters
    api_key:    The API key to revoke. <str>
    user_context (optional, requires administrator)




## SessionCheckIn

### Overview
    This API function checks in a session, updating timestamps and history, submitting
    action responses, and will return new actions for the session to complete.

### Parameters
    session_id:             The session_id of the session to check in. <str>
    responses (optional):   Any responses to actions that the session is submitting. <list[dict]>
    facts (optional):       Any updates to the Target's fact collection. <dict>
    config (optional):      Any updates to the Session's config. <dict>




## SetTargetFacts

    This API function updates the facts dictionary for a target.
    It will overwrite any currently existing keys, but will not remove
    existing keys that are not specified in the 'facts' parameter.

    name: The name of the target to update. <str>
    facts: The dictionary of facts to use. <dict>




## UnblacklistGroupMember

### Overview
    Remove a target from the blacklist of a group.

### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>




## UnregisterAgent

### Overview
    This function deletes an Agent from the database.

### Parameters
    agent_version: The agent version string to search for. <str>




## UnregisterWebhook

### Overview
    This API function will unregister a webhook.

### Parameters
    hook_id (required): The identifier of the hook to unregister.




## UpdateRolePermissions

### Overview
    Update the permission set of a role.

### Parameters
    role_name:          The name of the role to update. <str>
    allowed_api_calls:  The new list of allowed api methods. <list[str]>




## UpdateSessionConfig

### Overview
    This API function updates the config dictionary for a session.
    It will overwrite any currently existing keys, but will not remove
    existing keys that are not specified in the 'config' parameter.

    NOTE: This should only be called when a session's config HAS been updated.
          to update a session's config, queue an action of type 'config'.

### Parameters
    session_id:                 The session_id of the session to update. <str>
    config_dict (optional):     The config dictionary to use. <dict>
    servers (optional):         The session's new servers. <list[str]>
    interval (optional):        The session's new interval. <float>
    interval_delta (optional):  The session's new interval_delta. <float>




## UpdateUserPassword

### Overview
    Changes a users password. Requires the user's current password.

### Parameters
    current_password:   The user's current password. <str>
    new_password:       The user's new password. <str>
    user_context (optional, requires administrator)
