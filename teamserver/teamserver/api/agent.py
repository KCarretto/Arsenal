"""
    This module contains all 'Agent' API functions.
"""
from ..utils import success_response, handle_exceptions
from ..models import Agent

@handle_exceptions
def register_agent(params):
    """
    This API function registers an agent version with the teamserver. This is used to denote
    what action types an agent supports, to avoid unsupported action types from being sent to
    an agent. If an unregistered agent calls back, there will be no restrictions on what action
    types it receives. If an agent_version already exists, it will be overwritten by the new
    registration.


    agent_version (required, unique): The agent version string to update capabilities for. <str>
    supported_actions (required): A list of supported action types. i.e. [0, 1, 3]. <list>
    """
    agent_version = params['agent_version']
    supported_actions = params['supported_actions']

    agent = Agent(
        agent_version=agent_version,
        supported_actions=supported_actions,
    )
    agent.save()

    return success_response()

@handle_exceptions
def get_agent(params):
    """
    This function retrieves an Agent from the database.

    agent_version (required): The agent version string to search for. <str>
    """
    agent = Agent.get_by_version(params['agent_version'])
    return success_response(agent=agent.document)

@handle_exceptions
def list_agents(params): #pylint: disable=unused-argument
    """
    This function returns a list of agent documents.
    """
    return success_response(agents=[agent.document for agent in Agent.list_agents()])

@handle_exceptions
def unregister_agent(params):
    """
    This function deletes an Agent from the database.

    agent_version (required): The agent version string to search for. <str>
    """
    agent = Agent.get_by_version(params['agent_version'])
    agent.remove()
