"""
    This runs the teamserver using a Flask webserver (not recommended for production use).
"""
from teamserver import create_app
from teamserver.config import MODE

TEAMSERVER = create_app()

if __name__ == "__main__":
    debug = MODE.upper() == "DEBUG"
    TEAMSERVER.run(debug=debug)
