"""
    This file describes the various configuration options available for tweaking.
"""

# DATABASE CONNECTION SETTINGS
DB_NAME = 'arsenal_sample'
DB_HOST = 'localhost'
DB_PORT = 27017
DB_USER = None
DB_PASS = None

# DATABASE DOCUMENT SETTINGS
MAX_STR_LEN = 100
MAX_BIGSTR_LEN = 10000

# DATABASE COLLECTION SETTINGS
COLLECTION_ACTIONS = "actions"
COLLECTION_GROUPS = "groups"
COLLECTION_SESSIONS = "sessions"
COLLECTION_SESSION_HISTORIES = "session_histories"
COLLECTION_TARGETS = "targets"

# SESSION SETTINGS
SESSION_CHECK_THRESHOLD = 5
SESSION_CHECK_MODIFIER = 1.5
SESSION_STATUSES = {
    'active': 'active',
    'missing': 'missing',
    'inactive': 'inactive'
}

# ACTION SETTINGS
ACTION_STALE_THRESHOLD = 900
ACTION_STATUSES = {
    'queued': 'queued',
    'sent': 'sent',
    'failing': 'failing',
    'failed': 'failed',
    'error': 'error',
    'complete': 'complete',
    'stale': 'stale'
}
