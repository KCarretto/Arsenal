"""
    This module contains methods used to directly access the database.
    This is useful in cases where relying on API functions may be unreliable.
"""
from uuid import uuid4

import sys
import time

try:
    from teamserver.models import Action, Response, GroupAction, Log
    from teamserver.models import Session, SessionHistory, Target, Group
    from teamserver.config import SESSION_CHECK_THRESHOLD
except ModuleNotFoundError:
    from os.path import abspath, dirname
    # Configure path to start at teamserver module
    sys.path.append(abspath(dirname(dirname(dirname(abspath(__file__))))))
    from teamserver.models import Action, Response, GroupAction, Log
    from teamserver.models import Session, SessionHistory, Target, Group
    from teamserver.config import SESSION_CHECK_THRESHOLD

class Database(object):
    """
    This object just contains methods used to insert objects directly into the database.
    These methods do not invoke the API to create any objects.
    """
    #####################################
    #           Create Methods          #
    #####################################
    @staticmethod
    def create_action(
            target_name=None,
            action_string=None,
            action_type=None,
            response=None,
            bound_session_id=None):
        """
        Create an action object in the database.
        """
        if target_name is None:
            target = Database.create_target()
            target_name = target.name

        action_string = action_string if action_string is not None else 'exec echo test'

        action = Action(
            action_id=str(uuid4()),
            action_string=action_string,
            action_type=action_type if action_type is not None else 1,
            target_name=target_name,
            bound_session_id=bound_session_id if bound_session_id is not None else '',
            queue_time=time.time(),
            response=response
        )
        parsed_action = Action.parse_action_string(action_string)
        action.update_fields(parsed_action)
        action.save(force_insert=True)
        return action

    @staticmethod
    def create_group_action(
            group_name=None,
            action_string=None):
        """
        Create a group action object in the database.
        """
        action_string = action_string if action_string is not None else 'exec ls -al /bin'

        if group_name is None:
            targets = [
                Database.create_target().name,
                Database.create_target().name,
                Database.create_target().name,
                Database.create_target().name,
            ]
            group_name = Database.create_group(None, targets).name

        group = Database.get_group(group_name)
        actions = [
            Database.create_action(target, action_string).action_id
            for target in group.member_names
        ]

        action_string = action_string if action_string is not None else 'exec echo test'

        group_action = GroupAction(
            group_action_id=str(uuid4()),
            action_string=action_string,
            action_ids=actions
        )
        group_action.save(force_insert=True)
        return group_action

    @staticmethod
    def create_response(
            stdout=None,
            stderr=None,
            error=False,
            start_time=None,
            end_time=None):
        """
        Create a response object in the database.
        """
        response = Response(
            stdout=stdout if stdout is not None else 'test',
            stderr=stderr if stderr is not None else '',
            error=error,
            start_time=start_time if start_time is not None else (time.time()-5),
            end_time=end_time if end_time is not None else time.time()
        )
        return response

    @staticmethod
    def create_group(
            name=None,
            whitelist_members=None,
            blacklist_members=None):
        """
        Create an group object in the database.
        """
        group = Group(
            name=name if name is not None else str(uuid4()),
            whitelist_members=whitelist_members,
            blacklist_members=blacklist_members
        )
        group.save(force_insert=True)

        return group

    @staticmethod
    def create_session( # pylint: disable=too-many-arguments
            target_name=None,
            timestamp=None,
            interval=20,
            interval_delta=5,
            servers=None,
            config_dict=None,
            create_history=True):
        """
        Create an session object in the database.
        """
        if target_name is None:
            target = Database.create_target()
            target_name = target.name

        session_id = str(uuid4())
        timestamp = timestamp if timestamp is not None else time.time()

        if create_history:
            Database.create_session_history(session_id, [timestamp])

        session = Session(
            session_id=session_id,
            target_name=target_name,
            servers=servers if servers is not None else ['8.8.8.8'],
            interval=interval,
            interval_delta=interval_delta,
            config_dict=config_dict,
            timestamp=timestamp
        )
        session.save(force_insert=True)

        return session

    @staticmethod
    def create_session_history(session_id=None, checkin_timestamps=None):
        """
        Create an session history object in the database.
        """
        session_history = SessionHistory(
            session_id=session_id if session_id is not None else str(uuid4()),
            checkin_timestamps=checkin_timestamps if checkin_timestamps else [time.time()]
        )
        session_history.save(force_insert=True)

        return session_history

    @staticmethod
    def create_target(
            name=None,
            mac_addrs=None,
            facts=None,
            credentials=None):
        """
        Create an target object in the database.
        """
        target = Target(
            name=name if name is not None else str(uuid4()),
            facts=facts if facts is not None else {
                'hostname': uuid4(),
                'interfaces': [
                    {
                        'name': 'lo',
                        'mac_addr': str(uuid4),
                        'ip_addrs': ['127.0.0.1', '::1']
                    },
                    {
                        'name': 'eth0',
                        'mac_addr': str(uuid4),
                        'ip_addrs': ['192.168.0.1']
                    }
                ]
            },
            mac_addrs=mac_addrs if mac_addrs is not None else [
                'AA:BB:CC:DD:EE:FF',
                str(uuid4())[0:17]
                ],
            credentials=credentials
        )
        target.save(force_insert=True)
        return target

    @staticmethod
    def create_log(timestamp, application, level, message):
        """
        Creates a log in the database.
        """
        entry = Log(
            application=application,
            timestamp=timestamp,
            level=level,
            message=message
        )
        entry.save(force_insert=True)
        return entry

    #####################################
    #           Get Methods             #
    #####################################
    @staticmethod
    def get_action(action_id):
        """
        Get an action object from the database.
        """
        return Action.get_by_id(action_id)
    @staticmethod
    def get_group_action(group_action_id):
        """
        Get a group action object from the database.
        """
        return GroupAction.get_by_id(group_action_id)

    @staticmethod
    def get_group(name):
        """
        Get a group object from the database.
        """
        return Group.get_by_name(name)

    @staticmethod
    def get_session(session_id):
        """
        Get a session object from the database.
        """
        return Session.get_by_id(session_id)

    @staticmethod
    def get_session_history(session_id):
        """
        Get a session history object from the database.
        """
        return SessionHistory.get_by_session_id(session_id)

    @staticmethod
    def get_target(name):
        """
        Get a target object from the database.
        """
        return Target.get_by_name(name)

    @staticmethod
    def list_logs(application=None):
        """
        List logs for an application.
        """
        return Log.list(False, application)

    #####################################
    #           Utility Methods         #
    #####################################
    @staticmethod
    def parse_action_string(action_string):
        """
        Parses an action string.
        """
        return Action.parse_action_string(action_string)

    @staticmethod
    def missing_session(session):
        """
        This function updates a session's timestamp to force it's status
        to become missing.
        """
        missing_timer = session.interval + session.interval_delta + SESSION_CHECK_THRESHOLD + 1
        session.timestamp = time.time() - missing_timer
        session.save()
