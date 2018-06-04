---
layout: page
title: ACME Water
description: A fictitious water company
info: A ficitious water company
categories: exemplar
image:
  teaser: ACME_teaser.gif
---

{% include toc.html %}

# ACME Water

<h2>Background</h2>

The security of the environment around Control Systems, operational personnel, sites, assets, activities, information, technological resources, and services has taken on increased importance at ACME Water for the following reasons:

* The disappearing network boundary: a highly mobile workforce works on assets and systems deployed over a diverse and challenging geographic terrain.  Information Technology enables this but, in doing so, needs to provide controlled access to core applications, allowing multiple protocols access through the perimeter, reducing perimeter controls, allowing partners to deliver contractual obligations on time and to cost.
* The business climate is highly regulated, and delivery of Wastewater and Cleanwater services are critical to our customers.  It is imperative ACME employees are made aware of the importance of protecting our assets, information, and reputation to meet this end.
* Law requires companies to institute reasonable, effective and consistent controls designed to prevent the disclosure and falsification of information, the safety of personnel, sites, and the protection of technological resources.
* Rapid changes face ACME in the use and dependence of computers and network technologies.  It is necessary and reasonable to expect everyone to apply the proper methods of handling and safeguarding information, and managing computer and network resources.

<h2>Goal</h2>

To provide a secure operating environment for SCADA, Telemetry and Control Systems associated with assets owned and operated by ACME.

<h2>Scope</h2>

All ICT infrastructure in support of Enterprise SCADA, Telemetry and Control Systems indicated in the rich picture.

<p><img src="/images/acmeContext.jpg" style="width:100%;height:100%;" alt="fig:ACMEContext" title="Context diagram" /></p>

<h2>Environments</h2>

| Name | Description |
| ---- | ----------- |
| Day  | Day-time plant operations |
| Night | Night-time plant operations |

<h2>Assets</h2>

* Corporate Network
* Enterprise SCADA Network
* EnterpriseSCADA Server
* Firewall
* ICT Application
* ICT cabinet
* ICT credentials
* ICT PC
* InfoPortal
* Intrusion Detection System
* Laptop
* Modem
* Router
* SCADA Workstation
* STCS Application
* STCS credentials
* Telemetry Network
* Works Network

<h2>Roles fulfilled by users or attackers</h2>

* Cracker
* Facilities Management
* ICT Partner
* Information Security Manager
* Instrument Technician
* Integrator
* Petty Criminal
* Plant Operator
* Service Desk
* Vendor

<h2>People</h2>

| Name | Type | Role | Synopsis |
| Barry | Persona | Instrument Technician | A roving instrument technician |
| Gareth | Attacker | Petty Criminal | A raw metal thief |
| Martin | Attacker | Cracker | An industrial control systems penetration tester |
| Rick | Persona | Plant Operator | A cleanwater plant operator |
| Unintentional Rick | Attacker | Plant Operator | A cleanwater plant operator |
| Victor | Attacker | Vendor | A disgruntled expert in ACME's SCADA software |

<h2>Designed Tasks</h2>

* Broken instrument alarm
* Modify SCADA HMI software
* Modify PLC software
* Resolve reservoir alarm
* Take chemicals delivery

<h2>Vulnerabilities</h2>

* Exposed cabinets
* Incomplete firewall rules
* Incomplete Intrusion Detection rules
* Incompatible security controls
* Redundant hardware
* Ubiquitous identity and knowledge
* Unchanged vendor passwords
* Unknown applications

<h2>Threats</h2>

* Enumeration
* False sensor readings
* Footprinting
* Logic bomb
* Kit theft
* Password Enumeration
* Sniffing Kerberos Authentication
* Unauthorised USB usage
* War-dialing

<h2>Further details</h2>

[CAIRIS model](https://github.com/failys/cairis/blob/master/examples/exemplars/ACME_Water/ACME_Water.xml)
