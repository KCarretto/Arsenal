"""
    This runs the teamserver using a Flask webserver (not recommended for production use).
"""

from teamserver import create_app

if __name__ == '__main__':
    teamapp = create_app()
    teamapp.run(debug=False)

