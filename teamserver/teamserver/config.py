"""
    This file describes the various configuration options available for tweaking.
"""
import os

# CELERY SETTINGS
CELERY_MAIN_NAME = 'arsenal'
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost:5672')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_BROKER_TRANSPORT = {
    'region': 'us-west-2'
}

# DATABASE CONNECTION SETTINGS
DB_NAME = os.environ.get('DB_NAME', 'arsenal_sample')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 27017))
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# DATABASE DOCUMENT SETTINGS
MAX_STR_LEN = 500
MAX_BIGSTR_LEN = 10000
MAX_RESULTS = 500

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
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
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
SESSION_ARCHIVE_MODIFIER = 2
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
    'stale': 'stale',
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
API_KEY_SALT = os.environ.get('API_KEY_SALT', "ROBO4PRESIDENT")
HASH_TIME_PARAM = 16
HASH_MEMORY_PARAM = 10
HASH_PARALLELIZATION_PARAM = 2

# WEBHOOK SETTINGS
CONNECT_TIMEOUT = 10.0
READ_TIMEOUT = 30.0



# INTEGRATION SETTINGS
def read_api_key(api_key_file):
    """
    Reads an API key file.
    """
    api_key = None
    if api_key_file and os.path.exists(api_key_file):
        with open(api_key_file, 'r') as keyfile:
            api_key = keyfile.readlines()[0].strip().strip('\n')

    return api_key

INTEGRATIONS = {
    'SLACK_CONFIG': {
        'enabled': os.environ.get('SLACK_ENABLED', False),
        'API_TOKEN': os.environ.get('SLACK_API_TOKEN', read_api_key('.slack_api')),
        'TIMEOUT': int(os.environ.get('SLACK_TIMEOUT', 10)),

        'ERROR_CHANNEL': os.environ.get('SLACK_ERROR_CHANNEL', 'notifications'),
        'ACTION_CHANNEL': os.environ.get('SLACK_ACTION_CHANNEL', 'notifications'),
    },
    'PWNBOARD_CONFIG': {
        'enabled': os.environ.get('PWNBOARD_ENABLED', False),
        'URL': os.environ.get('PWNBOARD_URL', 'https://pwnboard.local/generic')
    }
}
