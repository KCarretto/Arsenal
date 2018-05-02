"""
This script adds sample data to the database.
"""
import time

try:
    from teamserver.models import Target, Session, SessionConfig
except: # pylint: disable=bare-except
    import sys
    from os.path import dirname, abspath
    sys.path.insert(0, abspath(dirname(abspath(dirname(__file__)))))
    from teamserver.models import Target, Session, SessionConfig

def create_sample_data():
    """
    Add sample objects to the database.
    """
    targets = [
        Target(
            name="System A",
            uuid="AA:BB:CC:DD:EE:FF",
        ),
        Target(
            name="System B",
            uuid="AA:AA:AA:AA:AA:AA",
        ),
        Target(
            name="System C",
            uuid="BB:BB:BB:BB:BB:BB",
        ),
    ]
    sessions = [
        Session(
            session_id="Session 1",
            target_name="System A",
            timestamp=time.time(),
            agent_version="arsenal-default",
            config=SessionConfig(
                interval=10,
                delta=5,
                servers=[
                    "http://c2.redteam-arsenal.com",
                ]
            ),
        )
    ]

    for item in targets+sessions:
        item.save()

if __name__ == '__main__':
    create_sample_data()
