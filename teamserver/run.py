"""
    This runs the teamserver using a Flask webserver (not recommended for production use).
"""
from teamserver import create_app
from tools import create_sample_data

def main():
    """
    Run the application in debug mode.
    """
    print("Running Arsenal Teamserver in DEBUG mode!")
    teamserver_app = create_app(
        TESTING=True,
        DISABLE_AUTH=True,
        DISABLE_EVENTS=True,
        MONGODB_SETTINGS=
        {
            'db': 'arsenal_testing',
            'host': 'mongomock://localhost',
            'is_mock': True
        })
    create_sample_data()
    teamserver_app.run(debug=True)

if __name__ == '__main__':
    main()
else:
    TEAMSERVER = create_app()
