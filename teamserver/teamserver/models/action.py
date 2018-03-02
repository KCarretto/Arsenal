"""
    This module defines a python object model for the Action document
    in the backend MongoDB database.
"""
import time
import shlex

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine.fields import StringField, IntField, FloatField
from mongoengine.fields import BooleanField, EmbeddedDocumentField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, ACTION_STATUSES, SESSION_STATUSES
from ..config import COLLECTION_ACTIONS, ACTION_STALE_THRESHOLD
from ..config import ACTION_TYPES, FACT_SUBSETS


class Response(EmbeddedDocument):
    """
    This class represents a response from an action.

        stdout: Any output the action genereated.
        stderr: Any error messages the action generated.
        start_time: The local system time that the action started.
        end_time: The local system time that the action completed.
        error: A boolean representing if the action encountered an error.
    """

    stdout = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    stderr = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    start_time = FloatField(required=True, null=False)
    end_time = FloatField(required=True, null=False)
    error = BooleanField(default=True)

class Action(DynamicDocument):
    """
    This class represents an action, which is assigned to a target
    and then sent to a session. It's status is based on the status of
    the session it was sent to, as well as if the session has sent or
    responded to the action yet.
    """
    meta = {
        'collection': COLLECTION_ACTIONS,
        'indexes': [
            {
                'fields': ['action_id'],
                'unique': True
            },
            {
                'fields': ['target_name']
            },
            {
                'fields': ['session_id']
            },
        ]
    }
    action_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    action_string = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN)
    action_type = IntField(required=True, null=False)
    target_name = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    session_id = StringField(max_length=MAX_STR_LEN)
    bound_session_id = StringField(max_length=MAX_STR_LEN)

    queue_time = FloatField(required=True, null=False)
    sent_time = FloatField()
    complete_time = FloatField()

    response = EmbeddedDocumentField(Response)

    @staticmethod
    def get_by_id(action_id):
        """
        This method queries for the action object matching the id provided.
        """
        return Action.objects.get(action_id=action_id) #pylint: disable=no-member

    @staticmethod
    def get_target_actions(target_name):
        """
        This method returns a list of actions for the given target name.
        """
        return Action.objects(target_name=target_name) #pylint: disable=no-member

    @staticmethod
    def get_target_unassigned_actions(target_name, session_id=None):
        """
        This method returns a list of unassigned actions for the given target name.
        Provide a session_id to include actions that are bound to that session_id.
        """
        return Action.objects( #pylint: disable=no-member
            target_name=target_name,
            session_id=None,
            bound_session_id__in=[session_id, None]
        )

    @staticmethod
    def parse_action_string(action_string):
        """
        This function will parse an action string, and return a dictionary of
        key value pairs to set on an associated Action document. Additionally it
        will return the action type of the action in the 'action_type' field of the
        dictionary.
        """
        cmd = shlex.split(action_string)

        def parse_config(tokens):
            """
            This parses the config action category.

            syntax: config key=value key2=value2
            """
            config = dict(token.split('=') for token in tokens)

            return {
                'action_type': ACTION_TYPES.get('config', 0),
                'config': config
            }

        def parse_exec(tokens):
            """
            This parses the exec action category.

            syntax: exec [--time=<time>, -t=<time> ] [--spawn, -s] '<command>'
            """
            spawn = '--spawn' in tokens or '-s' in tokens
            timed = any(
                [
                    '--time=' in token for token in tokens
                ]) or any(
                    [
                        '-t=' in token for token in tokens
                    ]
                )

            start_time = None
            if timed:
                for token in tokens:
                    if token.startswith('--time=') or token.startswith('-t='):
                        start_time = token.split('=')[1]

            action_type = ACTION_TYPES.get('exec', 1)
            if timed and spawn:
                action_type = ACTION_TYPES.get('timed_spawn', 4)
            elif spawn:
                action_type = ACTION_TYPES.get('spawn', 2)
            elif timed:
                action_type = ACTION_TYPES.get('timed_exec', 3)

            cmd = tokens[-1]
            if any([cmd in token for token in ['--time=', '-t=', '-s', '--spawn']]):
                pass
                # TODO: Raise parsing error

            cmd_tokens = shlex.split(cmd)
            args = []
            if len(cmd_tokens) > 1:
                args = cmd_tokens[1:]

            response = {
                'action_type': action_type,
                'command': cmd_tokens[0],
                'args': args,
            }
            if timed:
                response['start_time'] = start_time

        def parse_upload(tokens):
            """
            This parses the upload action category.

            syntax: upload <teamserver_path> <remote_path>
            """
            return {
                'action_type': ACTION_TYPES.get('upload', 5),
                'teamserver_path': tokens[0],
                'remote_path': tokens[1]
            }

        def parse_download(tokens):
            """
            This parses the download action category.

            syntax: download <remote_path> <name>
            """
            return {
                'action_type': ACTION_TYPES.get('download', 6),
                'remote_path': tokens[0],
                'name': tokens[1]
            }

        def parse_gather(tokens):
            """
            This parses the gather action category.
            You may specify a subset, however the default is all.
            syntax: gather [subset]
            """
            action_type = ACTION_TYPES.get('gather', 7)
            subset = FACT_SUBSETS.get('all', 'all')
            if tokens:
                subset = FACT_SUBSETS.get(tokens[0], 'all')

            return {
                'action_type': action_type,
                'subset': subset
            }

        def parse_reset(tokens): #pylint: disable=unused-argument
            """
            This parses the reset action category.
            """
            return {
                'action_type': ACTION_TYPES.get('reset')
            }

        cmds = {
            'config': parse_config,
            'exec': parse_exec,
            'upload': parse_upload,
            'download': parse_download,
            'gather': parse_gather,
            'reset': parse_reset
        }
        method = cmds.get(cmd[0].lower())
        if method is None or not callable(method):
            # TODO: Raise parsing exception
            pass

        # TODO: Raise parsing exception
        parsed = method(cmd[1:])

        return parsed

    @property
    def session(self):
        """
        This property queries for the associated session object.
        """
        return Session.objects.get(session_id=self.session_id) #pylint: disable=no-member

    @property
    def status(self): #pylint: disable=too-many-return-statements
        """
        This property returns the current status of the action based
        on the status of it's assigned session, as well as if it has
        been retrieved or contains a response.
        """
        # Return queued if no session has been assigned
        if self.session_id is None:
            if time.time() > self.queue_time + ACTION_STALE_THRESHOLD:
                return ACTION_STATUSES.get('stale', 'stale')
            return ACTION_STATUSES.get('queued', 'queued')
        # Return complete if we have received a response
        elif self.response is not None:
            if self.response.error:
                return ACTION_STATUSES.get('error', 'error')
            return ACTION_STATUSES.get('complete', 'complete')

        # TODO: Raise an error if the session does not exist

        session_status = self.session.status

        if session_status == SESSION_STATUSES.get('active', 'active'):
            return ACTION_STATUSES.get('sent', 'sent')

        if session_status == SESSION_STATUSES.get('missing', 'missing'):
            return ACTION_STATUSES.get('failing', 'failing')

        return ACTION_STATUSES.get('failed', 'failed')

    @property
    def agent_document(self):
        """
        This property filters and returns the JSON information that will be sent
        to an agent.
        """
        return {
            'action_id': self.action_id,
            'action_type': self.action_type,
        }
    def assign_to(self, session):
        """
        This function assigns this action to a session. It will update
        the current action object.
        """
        # TODO: Generate Event

        if self.bound_session_id is not None and session.session_id != self.bound_session_id:
            # TODO: Raise error for assigning to non-bound session
            pass

        self.session_id = session.session_id
        self.sent_time = time.time()
        self.save()

    def assign_to_id(self, session_id):
        """
        This function will assign the action to the given session_id.
        It does not attempt to lookup the session.
        """
        # TODO: Generate Event

        if self.bound_session_id is not None and session_id != self.bound_session_id:
            # TODO: Raise error for assigning to non-bound session
            pass

        self.session_id = session_id
        self.sent_time = time.time()
        self.save()

    def submit_response(self, response):
        """
        This function will update the action object with a response object,
        and set appropriate timestamps.
        """
        # TODO: Generate Event
        self.response = response
        self.complete_time = time.time()
        self.save()
