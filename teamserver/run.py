"""
    This runs the teamserver using a Flask webserver (not recommended for production use).
"""
import sys
print (sys.path)

from teamserver import create_app

TEAMSERVER = create_app()

if __name__ == '__main__':
    TEAMSERVER.run(debug=False)

