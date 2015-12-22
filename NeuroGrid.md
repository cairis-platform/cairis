---
layout: default
title: NeuroGrid
description: A data grid for neuroscience
categories: exemplar
image:
  teaser: Exemplar_teaser.gif
---

{% include toc.html %}

# NeuroGrid

## Background

NeuroGrid is a project funded by the UK Medical Research Council.  The project's aim is to develop a Grid-based collaborative research environment, in order to enhance collaboration both within and between clinical researchers.

The sensitivity of this clinical data and its distributed nature drives the need to find secure and effective ways of accessing and managing it.

## Goal

The high-level goal which needs to be satisfied is the secure processing of clinical data.  This involves securely uploading clinical data to NeuroGrid, which is then analysed before aggregated results can be downloaded.

## Scope

The scope of this study is restricted to the upload and download of data to and from NeuroGrid.


## Environments

| Name | Description |
| ---- | ----------- |
| Core Technology | NeuroGrid infrastructure operations |
| Psychosis | The exemplar aims to integrate large existing datasets of serial MRI scans and behaviour data coupled to the NeuroGrid image analysis service into a Grid-based database, test image normalisation techniques, and develop a general ontology for a psychosis databas, for use in multi-centre studies.  The exemplar tests capabilities of NeuroGrid to deal with restrospective data, assimilate material into databases, and use of the toolkit for normalisation and analysis.|
| Stroke | This exemplar aims to improve infrastructure for handling imaging in large studies including: efficient interpretation and storage of large image datasets from multicentre randomised controlled trials; very large studies of observer reliability to improve image interpretation; establishing large living archives of images linked to key metadata for diseases which require long term study to understand their true nature history and the effects of treatment; for knowledge transfer. The development of a structure for trial image metadata, based on a careful description of the metadata in the two exemplar trials is a key part of the project. |

## Assets

* Access Control Policy
* Analysis data
* CA certificate
* Client Workstation
* Clinical data
* Data node
* Delegation token
* Guest certificate
* Grid meta-data
* Portal
* Personal certificate
* User certificate
* Web browser
* WebDev folder
* Workflow

## Roles fulfilled by users or attackers

* Certificate Authority
* Data Consumer
* Data Provider
* Developer
* Hacker
* Researcher
* Social Engineer
* Sysadmin

## People

| Name | Type | Role | Synopsis |
| Carol | Attacker | Social Engineer | A freelance journalist |
| Claire | Persona | Researcher | A clinical researcher within the Psychosis exemplar |
| Mallory | Attacker | Hacker | A bot maintainer |
| Matt | Persona | Sysadmin | A system administrator on the infrastructure team |
| Tom | Persona | Developer | An application developer within the Stroke exemplar |
| Trudy | Attacker | Hacker | A script kiddie |
| Yves | Attacker | Data Consumer, Social Engineer | A research fellow within the Stroke exemplar |

## Designed Tasks

* Issue User Certificate
* Upload data
* Download data

## Vulnerabilities

* Certificate ubiquity
* Intermediate data accessibility
* Invisible college
* OTS vulnerability
* Partial anonymisation
* Replay vulnerability
* Workflow channel

## Threats

* Clinical data modification
* Meta-data modification
* Social engineering
* Trojan Horse
* DOS
* Replay attack

## Further details

[Github](https://github.com/failys/CAIRIS/tree/master/cairis/examples/exemplars/NeuroGrid)
