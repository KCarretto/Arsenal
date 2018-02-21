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
COLLECTION_TARGETS = "targets"
COLLECTION_ACTIONS = "actions"

# SESSION SETTINGS
SESSION_CHECK_THRESHOLD = 5
SESSION_CHECK_MODIFIER = 1.5
SESSION_STATUSES = {
    'active': 'active',
    'missing': 'missing',
    'inactive': 'inactive'
}

