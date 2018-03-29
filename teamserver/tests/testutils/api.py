"""
    This module is used to invoke API functions.
"""

from flask import json

class APIClient(object): # pylint: disable=too-many-public-methods
    """
    This class contains several functions that allow the user to invoke
    API methods.
    """
    #####################################
    #          Webhook Methods          #
    #####################################
    #@staticmethod
    #def register_webhook(client):
    #    pass

    #@staticmethod
    #def remove_webhook(client):
    #    pass

    #@staticmethod
    #def list_webhooks(client):
    #    pass

    #####################################
    #          API Methods              #
    #####################################
    #@staticmethod
    #def create_api_token(client):
    #    pass

    #@staticmethod
    #def delete_api_token(client):
    #    pass

    #####################################
    #          Target Methods           #
    #####################################
    @staticmethod
    def create_target(
            client,
            name=None,
            mac_addrs=None,
            facts=None):
        """
        Invoke the CreateTarget API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateTarget',
                name=name if name is not None else 'TEST Target',
                mac_addrs=mac_addrs if mac_addrs else ['AA:BB:CC:DD:EE:FF'],
                facts=facts if facts is not None else {}
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)

    @staticmethod
    def get_target(
            client,
            name):
        """
        Invoke the GetTarget API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetTarget',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)


    @staticmethod
    def set_target_facts(
            client,
            name,
            facts):
        """
        Invoke the SetTargetFacts API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='SetTargetFacts',
                name=name,
                facts=facts,
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)

    @staticmethod
    def get_target_groups(
            client,
            name):
        """
        Invoke the GetTargetGroups API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetTargetGroups',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)

    @staticmethod
    def get_target_actions(
            client,
            name):
        """
        Invoke the GetTargetActions API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetTargetActions',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #@staticmethod
    #def archive_target(client):
    #    pass

    @staticmethod
    def list_targets(client):
        """
        Invoke the ListTargets API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListTargets',
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)

    @staticmethod
    def rename_target(client, name, new_name):
        """
        Invoke the RenameTarget API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='RenameTarget',
                name=name,
                new_name=new_name,
            )),
            content_type='application/json',
            follow_redirects=True
            )
        return json.loads(resp.data)

    #####################################
    #          Session Methods          #
    #####################################
    @staticmethod
    def create_session( # pylint: disable=too-many-arguments
            client,
            mac_addrs,
            interval=120,
            interval_delta=20,
            servers=None,
            config_dict=None):
        """
        Invoke the CreateSession API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateSession',
                mac_addrs=mac_addrs,
                servers=servers if servers else ['10.10.10.10', 'https://google.com'],
                interval=interval,
                interval_delta=interval_delta,
                config_dict=config_dict if config_dict else {'TEST_SESSION': 'hello world'},
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def get_session(
            client,
            session_id):
        """
        Invoke the GetSession API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetSession',
                session_id=session_id,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def session_check_in(
            client,
            session_id,
            responses=None):
        """
        Invoke the SessionCheckIn API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='SessionCheckIn',
                session_id=session_id,
                responses=responses if responses else []
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def update_session_config( # pylint: disable=too-many-arguments
            client,
            session_id,
            interval=None,
            interval_delta=None,
            servers=None,
            config_dict=None):
        """
        Invoke the UpdateSessionConfig API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='UpdateSessionConfig',
                session_id=session_id,
                interval=interval,
                interval_delta=interval_delta,
                servers=servers,
                config_dict=config_dict
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #@staticmethod
    #def archive_session(client):
    #    pass

    @staticmethod
    def list_sessions(client):
        """
        Invoke the ListSessions API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListSessions',
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #####################################
    #          Action Methods           #
    #####################################
    @staticmethod
    def create_action(
            client,
            target_name,
            action_string=None):
        """
        Invoke the CreateAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateAction',
                target_name=target_name,
                action_string=action_string if action_string is not None else 'exec echo DEFAULT'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def get_action(
            client,
            action_id):
        """
        Invoke the GetAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetAction',
                action_id=action_id
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def cancel_action(
            client,
            action_id):
        """
        Invoke the CancelAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CancelAction',
                action_id=action_id
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def list_actions(client):
        """
        Invoke the ListActions API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListActions',
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #####################################
    #        Group Action Methods       #
    #####################################
    @staticmethod
    def create_group_action(
            client,
            group_name,
            action_string=None):
        """
        Invoke the CreateGroupAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateGroupAction',
                group_name=group_name,
                action_string=action_string if action_string is not None else 'exec echo DEFAULT'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def get_group_action(
            client,
            group_action_id):
        """
        Invoke the GetGroupAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetGroupAction',
                group_action_id=group_action_id
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def cancel_group_action(
            client,
            group_action_id):
        """
        Invoke the CancelGroupAction API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CancelGroupAction',
                group_action_id=group_action_id
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def list_group_actions(client):
        """
        Invoke the ListGroupActions API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListGroupActions',
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #####################################
    #           Group Methods           #
    #####################################
    @staticmethod
    def create_group(
            client,
            name):
        """
        Invoke the CreateGroup API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateGroup',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def get_group(
            client,
            name):
        """
        Invoke the GetGroup API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='GetGroup',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def add_group_member(
            client,
            group_name,
            target_name):
        """
        Invoke the AddGroupMember API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='AddGroupMember',
                group_name=group_name,
                target_name=target_name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def remove_group_member(
            client,
            group_name,
            target_name):
        """
        Invoke the RemoveGroupMember API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='RemoveGroupMember',
                group_name=group_name,
                target_name=target_name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def blacklist_group_member(
            client,
            group_name,
            target_name):
        """
        Invoke the BlacklistGroupMember API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='BlacklistGroupMember',
                group_name=group_name,
                target_name=target_name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def delete_group(
            client,
            name):
        """
        Invoke the DeleteGroup API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='DeleteGroup',
                name=name,
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def list_groups(client):
        """
        Invoke the ListGroups API function using the provided client.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListGroups',
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    #####################################
    #        Credentials Methods        #
    #####################################
    #@staticmethod
    #def create_credentials(client):
    #    pass
    #
    #@staticmethod
    #def get_valid_credentials(client):
    #    pass
    #
    #@staticmethod
    #def invalidate_credentials(client):
    #    pass
    #
    #@staticmethod
    #def list_credentials(client):
    #   pass
    #
    #####################################
    #             Log Methods           #
    #####################################
    @staticmethod
    def create_log(
            client,
            application,
            level,
            message):
        """
        Invoke the CreateLog API method.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='CreateLog',
                application=application,
                level=level,
                message=message
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

    @staticmethod
    def list_logs(
            client,
            include_archived=False,
            since=0,
            application=None):
        """
        Invoke the ListLogs API method.
        """
        resp = client.post(
            '/api',
            data=json.dumps(dict(
                method='ListLogs',
                application=application,
                include_archived=include_archived,
                since=since
            )),
            content_type='application/json',
            follow_redirects=True
        )
        return json.loads(resp.data)

