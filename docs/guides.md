# Guides

This documentation file will provide you with any guides necessary in extending / customizing this framework.

## Creating an Agent

### Overview
An Agent is a program that will be run on a target system, and will callback to a C2 that has been integrated with Arsenal. The goal of Arsenal is to allow Red Teamers to create their own Agents and C2 servers, but not need to deal with any of the backend management. This guide will cover how to create an Agent to work with the Arsenal HTTP C2 Server. It is recommended that you review the contents of this guide before attempting to create your own Agent / C2, because the framework does impose some light requirements on the Agent.

### Agent Requirements
#### Target Identification Information
When an Agent calls back to a C2, it is important that the Teamserver is able to identify what machine / target the Agent is running on. IP Addresses alone cannot accurately identify a system, because NAT would cause many systems to appear the same from the C2's perspective. To solve this asset management problem, Arsenal utilizes a combination of the following information:
  - Hostname
  - All MAC Addresses
When a Session calls back with that criteria, identical to an already existing Target, the Session is associated with the already existing Target. If no Target with the given criteria exists, a new Target is created and is given an automatically generated name. Target naming rules may be created to assign Target names in an automated fashion. The order of the array of MAC Addresses does not matter.

#### Session ID Tracking
When an Agent calls back to the C2 for the first time, the C2 must register the newly created Session with the Arsenal Teamserver (If you are unfamiliar, we define a Session as a running instance of an Agent). It uses the Arsenal Teamserver API to do this. Once registered, the C2 is then provided with a Session ID that the Agent must keep track of, and send in every callback request. Without this, the Teamserver will be unable to track which Target a Session belongs to.

#### Action ID Tracking
When a Red Teamer wishes to run a command or perform some other action on the Target system, they queue an Action with the Arsenal Teamserver. Upon creation, that Action is given a unique identifier. Agents should receive this information with every command that they run, and upon completion, ensure that the Response also includes this Action identifier. Without this information, the Arsenal Teamserver cannot associate the given Response with an Action.

#### Action Types
It is required that Agents support the following action types, or return a specified error when an unsupported action type is attempted.

| Name    | Code | Description    | Required Parameters
| :------ | :--- | :------------- | :-------------------
| exec    | 0    | Run a command. | command: 'string'<br>args: ['list', 'of', 'args']
| spawn   | 1    | Run a command and disown child process.<br>Do not wait for output. | command: 'string'<br>args: ['list', 'of', 'args']
| timed_exec | 2 | Run a command at a given time.<br>Based off of the time provided, not the system time.| command: ‘string’<br>args: [‘list’, ‘of’, ‘args’]<br>activate_time: 123123.23<br>current_time: 123122.01
| upload  | 3    | Upload a file to the remote system. | remote_path: '/target/destination/path'<br>file: [byte array of file contents]
| download | 4   | Retrieve a file from the target system. | remote_path: '/target/source/path'
| gather   | 5   | Gather and report updated facts.         | subset: 'all'
| reset    | 999 | Reinitialize session.<br>Agent should perform another initial beacon.<br> C2 will provide a new Session ID. | N/A

