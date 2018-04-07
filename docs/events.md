# Events
This documentation file describes the events that are triggered within the teamserver, and the data that will be sent to subscribers via a Webhook.

# API Call
Each API method call generates the `api_call` event, with the following data:
```
{
'event': 'api_call',
'method': 'The method being called. i.e. ListTargets',
'user': 'The user calling the method',
}
```

# Session Check In
Each time a session checks in with the teamserver, the `session_checkin` event is triggered with the following data:
```
{
'event': 'session_checkin',
'session': <Session Object>,
'target': <Target Object (with only facts and defaults)
}
```

# Action Complete
Each time a response is submitted to an action, the `action_complete` event is triggered with the following data:
```
{
'event': 'action_complete',
'action': <Action Object>
}

