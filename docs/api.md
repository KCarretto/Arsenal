# API Documentation

Read here about how to interact with the teamserver's API.

## Table of Contents

- [Web Hooks](#web-hooks)
  * [RegisterWebhook](#registerwebhook)
    + [Overview](#overview)
    + [Parameters](#parameters)
    + [Example Request](#example-request)
    + [Example Response](#example-response)
  * [RemoveWebhook](#removewebhook)
    + [Overview](#overview-1)
    + [Parameters](#parameters-1)
    + [Example Request](#example-request-1)
    + [Example Response](#example-response-1)
  * [ListWebhooks](#listwebhooks)
    + [Overview](#overview-2)
    + [Parameters](#parameters-2)
    + [Example Request](#example-request-2)
    + [Example Response](#example-response-2)
- [API Tokens](#api-tokens)
  * [CreateAPIToken](#createapitoken)
    + [Overview](#overview-3)
    + [Parameters](#parameters-3)
    + [Example Request](#example-request-3)
    + [Example Response](#example-response-3)
  * [DeleteAPIToken](#deleteapitoken)
    + [Overview](#overview-4)
    + [Parameters](#parameters-4)
    + [Example Request](#example-request-4)
    + [Example Response](#example-response-4)
- [Targets](#targets)
  * [CreateTarget](#createtarget)
    + [Overview](#overview-5)
    + [Parameters](#parameters-5)
    + [Example Request](#example-request-5)
    + [Example Response](#example-response-5)
  * [GetTarget](#gettarget)
    + [Overview](#overview-6)
    + [Parameters](#parameters-6)
    + [Example Request](#example-request-6)
    + [Example Response](#example-response-6)
  * [SetTargetFacts](#settargetfacts)
    + [Overview](#overview-7)
    + [Parameters](#parameters-7)
    + [Example Request](#example-request-7)
    + [Example Response](#example-response-7)
  * [ArchiveTarget](#archivetarget)
    + [Overview](#overview-8)
    + [Parameters](#parameters-8)
    + [Example Request](#example-request-8)
    + [Example Response](#example-response-8)
  * [ListTargets](#listtargets)
    + [Overview](#overview-9)
    + [Parameters](#parameters-9)
    + [Example Request](#example-request-9)
    + [Example Response](#example-response-9)
- [Sessions](#sessions)
  * [CreateSession](#createsession)
    + [Overview](#overview-10)
    + [Parameters](#parameters-10)
    + [Example Request](#example-request-10)
    + [Example Response](#example-response-10)
  * [GetSession](#getsession)
    + [Overview](#overview-11)
    + [Parameters](#parameters-11)
    + [Example Request](#example-request-11)
    + [Example Response](#example-response-11)
  * [SessionCheckin](#sessioncheckin)
    + [Overview](#overview-12)
    + [Parameters](#parameters-12)
    + [Example Request](#example-request-12)
    + [Example Response](#example-response-12)
  * [ListSessions](#listsessions)
    + [Overview](#overview-13)
    + [Parameters](#parameters-13)
    + [Example Request](#example-request-13)
    + [Example Response](#example-response-13)
- [Actions](#actions)
  * [CreateAction](#createaction)
    + [Overview](#overview-14)
    + [Parameters](#parameters-14)
    + [Example Request](#example-request-14)
    + [Example Response](#example-response-14)
  * [CreateGroupAction](#creategroupaction)
    + [Overview](#overview-15)
    + [Parameters](#parameters-15)
    + [Example Request](#example-request-15)
    + [Example Response](#example-response-15)
  * [GetAction](#getaction)
    + [Overview](#overview-16)
    + [Parameters](#parameters-16)
    + [Example Request](#example-request-16)
    + [Example Response](#example-response-16)
  * [CancelAction](#cancelaction)
    + [Overview](#overview-17)
    + [Parameters](#parameters-17)
    + [Example Request](#example-request-17)
    + [Example Response](#example-response-17)
  * [CancelGroupAction](#cancelgroupaction)
    + [Overview](#overview-18)
    + [Parameters](#parameters-18)
    + [Example Request](#example-request-18)
    + [Example Response](#example-response-18)
  * [ListActions](#listactions)
    + [Overview](#overview-19)
    + [Parameters](#parameters-19)
    + [Example Request](#example-request-19)
    + [Example Response](#example-response-19)
- [Groups](#groups)
  * [CreateGroup](#creategroup)
    + [Overview](#overview-20)
    + [Parameters](#parameters-20)
    + [Example Request](#example-request-20)
    + [Example Response](#example-response-20)
  * [GetGroup](#getgroup)
    + [Overview](#overview-21)
    + [Parameters](#parameters-21)
    + [Example Request](#example-request-21)
    + [Example Response](#example-response-21)
  * [AddGroupMembers](#addgroupmembers)
    + [Overview](#overview-22)
    + [Parameters](#parameters-22)
    + [Example Request](#example-request-22)
    + [Example Response](#example-response-22)
  * [RemoveGroupMembers](#removegroupmembers)
    + [Overview](#overview-23)
    + [Parameters](#parameters-23)
    + [Example Request](#example-request-23)
    + [Example Response](#example-response-23)
  * [ListGroups](#listgroups)
    + [Overview](#overview-24)
    + [Parameters](#parameters-24)
    + [Example Request](#example-request-24)
    + [Example Response](#example-response-24)
  * [DeleteGroup](#deletegroup)
    + [Overview](#overview-25)
    + [Parameters](#parameters-25)
    + [Example Request](#example-request-25)
    + [Example Response](#example-response-25)
- [Credentials](#credentials)
  * [CreateCredentials](#createcredentials)
    + [Overview](#overview-26)
    + [Parameters](#parameters-26)
    + [Example Request](#example-request-26)
    + [Example Response](#example-response-26)
  * [GetValidCredentials](#getvalidcredentials)
    + [Overview](#overview-27)
    + [Parameters](#parameters-27)
    + [Example Request](#example-request-27)
    + [Example Response](#example-response-27)
  * [InvalidateCredentials](#invalidatecredentials)
    + [Overview](#overview-28)
    + [Parameters](#parameters-28)
    + [Example Request](#example-request-28)
    + [Example Response](#example-response-28)
  * [ListCredentials](#listcredentials)
    + [Overview](#overview-29)
    + [Parameters](#parameters-29)
    + [Example Request](#example-request-29)
    + [Example Response](#example-response-29)
- [Logs](#logs)
  * [CreateLog](#createlog)
    + [Overview](#overview-30)
    + [Parameters](#parameters-30)
    + [Example Request](#example-request-30)
    + [Example Response](#example-response-30)
  * [ListLogs](#listlogs)
    + [Overview](#overview-31)
    + [Parameters](#parameters-31)
    + [Example Request](#example-request-31)
    + [Example Response](#example-response-31)

## Web Hooks
### RegisterWebhook
#### Overview
#### Parameters
#### Example Request
#### Example Response
### RemoveWebhook 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListWebhooks
#### Overview
#### Parameters
#### Example Request
#### Example Response

## API Tokens
### CreateAPIToken
#### Overview
#### Parameters
#### Example Request
#### Example Response
### DeleteAPIToken
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Targets
### CreateTarget 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetTarget
#### Overview
#### Parameters
#### Example Request
#### Example Response
### SetTargetFacts
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ArchiveTarget 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListTargets
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Sessions
### CreateSession 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetSession 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### SessionCheckin
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListSessions
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Actions
### CreateAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CreateGroupAction 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CancelAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### CancelGroupAction
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListActions
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Groups
### CreateGroup 
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetGroup
#### Overview
#### Parameters
#### Example Request
#### Example Response
### AddGroupMembers
#### Overview
#### Parameters
#### Example Request
#### Example Response
### RemoveGroupMembers
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListGroups
#### Overview
#### Parameters
#### Example Request
#### Example Response
### DeleteGroup
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Credentials
### CreateCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### GetValidCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### InvalidateCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListCredentials
#### Overview
#### Parameters
#### Example Request
#### Example Response

## Logs
### CreateLog
#### Overview
#### Parameters
#### Example Request
#### Example Response
### ListLogs
#### Overview
#### Parameters
#### Example Request
#### Example Response


