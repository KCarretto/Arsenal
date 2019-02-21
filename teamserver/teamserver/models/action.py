"""
    This module defines a python object model for the Action document
    in the backend MongoDB database.
"""
import time
import shlex
import argparse

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine.fields import StringField, IntField, FloatField
from mongoengine.fields import BooleanField, EmbeddedDocumentField

from .session import Session

from ..exceptions import CannotCancelAction, CannotAssignAction
from ..exceptions import ActionSyntaxError, ActionUnboundSession
from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, ACTION_STATUSES, SESSION_STATUSES
from ..config import COLLECTION_ACTIONS, ACTION_STALE_THRESHOLD
from ..config import ACTION_TYPES, DEFAULT_SUBSET, MAX_RESULTS


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

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried action.
        """
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
        }


class Action(DynamicDocument):
    """
    This class represents an action, which is assigned to a target
    and then sent to a session. It's status is based on the status of
    the session it was sent to, as well as if the session has sent or
    responded to the action yet.
    """

    meta = {
        "collection": COLLECTION_ACTIONS,
        "indexes": [
            {"fields": ["action_id"], "unique": True},
            {"fields": ["target_name"]},
            {"fields": ["session_id"]},
            {"fields": ["target_name", "session_id", "cancelled", "bound_session_id"]},
            {"fields": ["target_name", "owner"]},
        ],
    }
    action_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    action_string = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN)
    action_type = IntField(required=True, null=False)
    target_name = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    session_id = StringField(max_length=MAX_STR_LEN)
    bound_session_id = StringField(null=False, default="", max_length=MAX_STR_LEN)

    queue_time = FloatField(required=True, null=False)
    cancel_time = FloatField()
    sent_time = FloatField()
    complete_time = FloatField()

    response = EmbeddedDocumentField(Response)
    cancelled = BooleanField(default=False)

    owner = StringField(max_length=MAX_STR_LEN)

    @staticmethod
    def get_by_id(action_id):
        """
        This method queries for the action object matching the id provided.
        """
        return Action.objects.get(action_id=action_id)  # pylint: disable=no-member

    @staticmethod
    def get_target_actions(target_name):
        """
        This method returns a list of actions for the given target name.
        """
        return Action.objects(target_name=target_name)  # pylint: disable=no-member

    @staticmethod
    def get_target_unassigned_actions(target_name, session_id=None):
        """
        This method returns a list of unassigned actions for the given target name.
        Provide a session_id to include actions that are bound to that session_id.
        """
        actions = Action.objects.filter(  # pylint: disable=no-member
            target_name=target_name,
            session_id=None,
            cancelled=False,
            bound_session_id__in=[None, session_id, ""],
        )
        return actions

    @staticmethod
    def list_actions(**kwargs):
        """
        This method queries for all action objects.
        """
        target_name = kwargs.get("target_name")
        owner = kwargs.get("owner")
        limit = kwargs.get("limit", MAX_RESULTS)
        offset = kwargs.get("offset", 0)
        if owner and target_name:
            return Action.objects(  # pylint: disable=no-member
                owner=owner, target_name=target_name
            )[offset:limit]
        elif owner:
            return Action.objects(owner=owner)[offset:limit]  # pylint: disable=no-member
        elif target_name:
            return Action.objects(target_name=target_name)[  # pylint: disable=no-member
                offset:limit
            ]
        return Action.objects[offset:limit]  # pylint: disable=no-member

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
            This action tells a session to update it's config with the provided json.

            syntax: config [options]
                -i, --interval: Set the session's interval
                -d, --delta: Set the session's interval delta
                -s, --servers: Set a list of the sessions servers
                -c, --config: Set the configuration dictionary
            """
            parser = argparse.ArgumentParser("config_action_parser")
            parser.add_argument("-i", "--interval", type=float)
            parser.add_argument("-d", "--delta", type=float)
            parser.add_argument("-c", "--config", nargs=2, action="append")
            parser.add_argument("-s", "--servers", nargs="+", type=list)
            args = parser.parse_args(tokens)
            config = {}
            if args.config and isinstance(args.config, list):
                for arg in args.config:
                    if isinstance(arg, list) and len(arg) > 1:
                        try:
                            config[arg[0]] = int(arg[1])
                        except ValueError:
                            config[arg[0]] = arg[1]

            if args.servers:
                config["servers"] = ["".join(server) for server in args.servers]
            if args.interval:
                config["interval"] = args.interval
            if args.delta:
                config["interval_delta"] = args.delta

            return {"action_type": ACTION_TYPES.get("config", 0), "config": config}

        def parse_exec(tokens):
            """
            This parses the exec action category.

            syntax: exec [options] <command> [args]
                -t, --time: Set a timestamp for the command to execute
                -s, --spawn: Cause the action to fork and spawn a process.
                             WARN: In many cases, you may not receive command output.
            """
            parser = argparse.ArgumentParser("exec_action_parser")
            parser.add_argument("-t", "--time", type=float)
            parser.add_argument("-s", "--spawn", action="store_true", default=False)
            parser.add_argument("command", nargs=argparse.REMAINDER, type=str)

            args = parser.parse_args(tokens)
            command_tokens = args.command

            action_type = ACTION_TYPES.get("exec", 1)

            if args.time and args.spawn:
                action_type = ACTION_TYPES.get("timed_spawn", 4)
            elif args.spawn:
                action_type = ACTION_TYPES.get("spawn", 2)
            elif args.time:
                action_type = ACTION_TYPES.get("timed_exec", 3)

            command_args = []
            if len(command_tokens) > 1:
                command_args = command_tokens[1:]

            resp = {"action_type": action_type, "command": command_tokens[0], "args": command_args}

            if args.time:
                resp["start_time"] = args.time

            return resp

        def parse_upload(tokens):
            """
            This parses the upload action category.

            syntax: upload <teamserver_path> <remote_path>
            """
            parser = argparse.ArgumentParser("upload_action_parser")
            parser.add_argument("teamserver_path", type=str)
            parser.add_argument("remote_path", type=str)
            args = parser.parse_args(tokens)

            return {
                "action_type": ACTION_TYPES.get("upload", 5),
                "teamserver_path": args.teamserver_path,
                "remote_path": args.remote_path,
            }

        def parse_download(tokens):
            """
            This parses the download action category.

            syntax: download <remote_path> <teamserver_path>
            """
            parser = argparse.ArgumentParser("download_action_parser")
            parser.add_argument("remote_path", type=str)
            parser.add_argument("teamserver_path", type=str)
            args = parser.parse_args(tokens)

            return {
                "action_type": ACTION_TYPES.get("download", 6),
                "remote_path": args.remote_path,
                "teamserver_path": args.teamserver_path,
            }

        def parse_gather(tokens):
            """
            This parses the gather action category.
            You may specify a subset, however the default is DEFAULT_SUBSET ('all' by default)/
            syntax: gather
                -s, --subset: Specify a subset of facts to gather.
            """
            parser = argparse.ArgumentParser("download_action_parser")
            parser.add_argument("-s", "--subset", type=str)
            args = parser.parse_args(tokens)

            return {
                "action_type": ACTION_TYPES.get("gather", 7),
                "subset": args.subset if args.subset else DEFAULT_SUBSET,
            }

        def parse_reset(tokens):  # pylint: disable=unused-argument
            """
            This parses the reset action category.

            syntax: reset
            """
            return {"action_type": ACTION_TYPES.get("reset", 999)}

        cmds = {
            "config": parse_config,
            "exec": parse_exec,
            "upload": parse_upload,
            "download": parse_download,
            "gather": parse_gather,
            "reset": parse_reset,
        }
        method = cmds.get(cmd[0].lower())
        if method is None or not callable(method):
            raise ActionSyntaxError("Invalid action type.")

        parsed = None
        try:
            parsed = method(cmd[1:])
        except IndexError:
            raise ActionSyntaxError("Invalid number of arguments.")

        return parsed

    @property
    def session(self):
        """
        This property queries for the associated session object.
        """
        return Session.objects.get(session_id=self.session_id)  # pylint: disable=no-member

    @property
    def status(self):  # pylint: disable=too-many-return-statements
        """
        This property returns the current status of the action based
        on the status of it's assigned session, as well as if it has
        been retrieved or contains a response.
        """
        # Return cancelled if the action was cancelled
        if self.cancelled:
            return ACTION_STATUSES.get("cancelled", "cancelled")

        # Return queued if no session has been assigned
        if self.session_id is None:
            if time.time() > self.queue_time + ACTION_STALE_THRESHOLD:
                return ACTION_STATUSES.get("stale", "stale")
            return ACTION_STATUSES.get("queued", "queued")
        # Return complete if we have received a response
        elif self.response is not None:
            if self.response.error:
                return ACTION_STATUSES.get("error", "error")
            return ACTION_STATUSES.get("complete", "complete")

        session = self.session
        if not session:
            self.session_id = None
            self.save()
            raise ActionUnboundSession(
                "Action is assigned to session that no longer exists. It has been unbound."
            )

        session_status = session.status

        if session_status == SESSION_STATUSES.get("active", "active"):
            return ACTION_STATUSES.get("sent", "sent")

        if session_status == SESSION_STATUSES.get("missing", "missing"):
            return ACTION_STATUSES.get("failing", "failing")

        return ACTION_STATUSES.get("failed", "failed")

    @property
    def agent_document(self):
        """
        This property filters and returns the JSON information that will be sent
        to an agent.
        """

        def config_document():
            """
            Returns an action document for the config action type.
            """
            return {
                "action_id": self.action_id,
                "action_type": self.action_type,
                "config": self.config,  # pylint: disable=no-member
            }

        def exec_document():
            """
            Returns an action document for the exec action type.
            """
            resp = {
                "action_id": self.action_id,
                "action_type": self.action_type,  # pylint: disable=no-member
                "command": self.command,  # pylint: disable=no-member
                "args": self.args,  # pylint: disable=no-member
            }

            if hasattr(self, "start_time"):  # pylint: disable=no-member
                resp["start_time"] = self.start_time  # pylint: disable=no-member

            return resp

        def upload_document():
            """
            Returns an action document for the upload action type.
            """
            return {
                "action_id": self.action_id,
                "action_type": self.action_type,
                "teamserver_path": self.teamserver_path,  # pylint: disable=no-member
                "remote_path": self.remote_path,  # pylint: disable=no-member
            }

        def download_document():
            """
            Returns an action document for the download action type.
            """
            return {
                "action_id": self.action_id,
                "action_type": self.action_type,
                "remote_path": self.remote_path,  # pylint: disable=no-member
                "teamserver_path": self.teamserver_path,  # pylint: disable=no-member
            }

        def gather_document():
            """
            Returns an action document for the gather action type.
            """
            return {
                "action_id": self.action_id,
                "action_type": self.action_type,
                "subset": self.subset,  # pylint: disable=no-member
            }

        def default_document():
            """
            Returns an action document for any other action type.
            """
            return {"action_id": self.action_id, "action_type": self.action_type}

        action_documents = {
            ACTION_TYPES.get("config", 0): config_document,
            ACTION_TYPES.get("exec", 1): exec_document,
            ACTION_TYPES.get("spawn", 2): exec_document,
            ACTION_TYPES.get("timed_exec", 3): exec_document,
            ACTION_TYPES.get("timed_spawn", 4): exec_document,
            ACTION_TYPES.get("upload", 5): upload_document,
            ACTION_TYPES.get("download", 6): download_document,
            ACTION_TYPES.get("gather", 7): gather_document,
            ACTION_TYPES.get("reset", 999): default_document,
        }

        return action_documents.get(self.action_type, default_document)()

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried action.
        """
        doc = self.agent_document
        doc["target_name"] = self.target_name
        doc["action_string"] = self.action_string
        doc["status"] = self.status
        doc["session_id"] = self.session_id
        doc["bound_session_id"] = self.bound_session_id
        doc["queue_time"] = self.queue_time
        doc["sent_time"] = self.sent_time
        doc["complete_time"] = self.complete_time
        doc["owner"] = self.owner
        if self.response:
            doc["response"] = self.response.document
        return doc

    def assign_to(self, session_id):
        """
        This function will assign the action to the given session_id.
        It does not attempt to lookup the session.
        """
        if self.bound_session_id and session_id != self.bound_session_id:
            raise CannotAssignAction(
                "Action cannot be assigned to session, because it is bound to another"
            )

        self.session_id = session_id
        self.sent_time = time.time()
        self.save()

    def submit_response(self, response):
        """
        This function will update the action object with a response object,
        and set appropriate timestamps.
        """
        self.response = response
        self.complete_time = time.time()
        self.save()

    def cancel(self):
        """
        This function will cancel an action if possible (only if status is queued).
        It will return True or False with the success of this operation.
        """
        if self.status == ACTION_STATUSES.get("queued", "queued"):
            self.cancelled = True
            self.cancel_time = time.time()
            self.save()
        else:
            raise CannotCancelAction("Action status is not queued.")

    def update_fields(self, parsed_action):
        """
        Sets fields on this action document based on a parsed action dictionary.
        """
        for key, value in parsed_action.items():
            if key not in [
                "action_id",
                "target_name",
                "action_string",
                "bound_session_id",
                "queue_time",
                "sent_time",
                "complete_time",
                "response",
            ]:
                self.__setattr__(key, value)

