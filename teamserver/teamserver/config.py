"""
    This file describes the various configuration options available for tweaking.
"""

# CELERY SETTINGS
CELERY_MAIN_NAME = 'arsenal'
CELERY_BROKER_URL = 'amqp://localhost:5672'
CELERY_RESULT_BACKEND = 'amqp://localhost:5672'

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
COLLECTION_ACTIONS = 'actions'
COLLECTION_GROUP_ACTIONS = 'group_actions'
COLLECTION_GROUPS = 'groups'
COLLECTION_SESSIONS = 'sessions'
COLLECTION_SESSION_HISTORIES = 'session_histories'
COLLECTION_TARGETS = 'targets'
COLLECTION_LOGS = 'logs'
COLLECTION_AGENTS = 'agents'
COLLECTION_USERS = 'users'
COLLECTION_ROLES = 'roles'
COLLECTION_APIKEYS = 'api_keys'
COLLECTION_WEBHOOKS = 'webhooks'

# LOG SETTINGS
APPLICATION = 'teamserver-internal'
LOG_LEVEL = 'DEBUG'
LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARN': 2,
    'CRIT': 3,
    'FATAL': 4
}

# AGENT SETTINGS
DEFAULT_AGENT_SERVERS = ['http://redteam.com']
DEFAULT_AGENT_INTERVAL = 60
DEFAULT_AGENT_INTERVAL_DELTA = 15
DEFAULT_AGENT_CONFIG_DICT = {}
DEFAULT_SUBSET = 'all'

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
    'cancelled': 'cancelled',
    'queued': 'queued',
    'sent': 'sent',
    'failing': 'failing',
    'failed': 'failed',
    'error': 'error',
    'complete': 'complete',
    'stale': 'stale',
}
GROUP_ACTION_STATUSES = {
    'cancelled': 'cancelled',
    'queued': 'queued',
    'in progress': 'in progress',
    'mixed success': 'mixed success',
    'success': 'success',
    'failed': 'failed',
}

ACTION_TYPES = {
    'config': 0,
    'exec': 1,
    'spawn': 2,
    'timed_exec': 3,
    'timed_spawn': 4,
    'upload': 5,
    'download': 6,
    'gather': 7,
    'reset': 999
}

# AUTH SETTINGS
API_KEY_SALT = 'thebestsaltthebestsalt'

# WEBHOOK SETTINGS
CONNECT_TIMEOUT = 10.0
READ_TIMEOUT = 30.0
