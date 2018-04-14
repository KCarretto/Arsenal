# Events Documentation
This documentation file describes the events that are triggered within the teamserver, and the data that will be sent to subscribers via a Webhook.

## Subscribing to Events
The teamserver's API allows you to subscribe to events by registering an outgoing 'Webhook'. You may manage webhooks using the `RegisterWebhook`, `UnregisterWebhook`, and `ListWebhooks` API methods. When registering a webhook, you will provide a `post_url`, which is the URL that the event data will be sent to via an HTTP POST request. You will also specify `event_triggers` which is a list of events to subscribe to. When any of these events are triggered, the information with be sent to the `post_url`.

## Event Details
### API Call
Each API method call generates the `api_call` event, with the following data:
```
{
'event': 'api_call',
'method': 'The method being called. i.e. ListTargets',
'user': 'The user calling the method',
}
```

### Session Check In
Each time a session checks in with the teamserver, the `session_checkin` event is triggered with the following data:
```
{
'event': 'session_checkin',
'session': <Session Object>,
'target': <Target Object (with only facts and defaults)
}
```

### Action Complete
Each time a response is submitted to an action, the `action_complete` event is triggered with the following data:
```
{
'event': 'action_complete',
'action': <Action Object>
}
```
### Logged Error
Each time a log with level CRIT or higher is generated, the `logged_error` event is triggered with the following data:
```
{
'event': 'logged_error',
'log': <Log Object>
}
```
