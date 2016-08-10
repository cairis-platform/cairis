---
layout: post
title:  "Introducing the CAIRIS web app"
date:   2016-08-10 23:00:00
categories: CAIRIS
description: Next steps in the evolution of CAIRIS
image:
  teaser: cairisweb_teaser.gif
---

## Introducing the CAIRIS web app ##

We're pleased to announce the first alpha release of the CAIRIS web app.

The web app first started life as a project by [Robin Quetin](https://github.com/RobinQuetin) and [Raf Vandelaer](http://www.rafvandelaer.be/) when they both visited BU last year.  Development on the app then lay dormant for several months while the rest of the code base was refactored.  Fortunately, with the help of [Waldemar Woch](https://github.com/invalidtoken) and [Rachel Larcombe](https://github.com/RachelLar) in recent months, the web app has been integrated into the CAIRIS code base and the web app is starting to become more and more functional.


In producing a web app of CAIRIS, we had three goals.

### 1. Opening CAIRIS for all platforms ###

People seem excited about CAIRIS, but less excited about using a GUI that runs on Linux/Gnome desktop, with people preferring to use something that runs on Windows or a Mac.  With this in mind, a CAIRIS web app provides the convenience of using the tool on the OS of one's choice without the overhead of porting all the front-end code to a specific native platform.  As the screenshots below illustrate, much of the analytical processing and visual model generation still takes place on the back-end, so the look and feel of the tool is largely unchanged.

![fig:riskmodel]({{ site.baseurl }}/images/NGRiskModel.jpg "Risk model")

![fig:riskmodel]({{ site.baseurl }}/images/NGReqs.jpg "Requirements management")

### 2. Opening CAIRIS for other apps and services ###

We wanted to develop an API that people could use for leveraging CAIRIS' analytical capabilities without using the GUI.  When CAIRIS was used on the [webinos project](http://webinos.org), many of the requirements and architectural design models were created and generated without using the GUI at all, and [scripts were used to import data into CAIRIS for processing, and export data from CAIRIS into various formats](https://github.com/webinos/webinos-design-data).  By interacting with the CAIRIS database exclusively through the web services, the CAIRIS web app has become a design tool that uses the CAIRIS API.  

### 3. Evolving CAIRIS into multiple apps ###

 We wish to evolve CAIRIS into multiple apps.  CAIRIS was initially designed as a requirements management tool which also managed security and UX design data.  In recent years, CAIRIS has evolved so much that it may be better served by multiple apps, with each using different subsets of the CAIRIS API.  For example, a *CAIRIS risk* app might focus on the functionality related to asset modelling and risk analysis, while a *CAIRIS UX* app might help UX designers co-located with security engineers by capturing data and creating models such as personas, use cases, requirements, and scenarios.

### Next steps ###

This initial version of the CAIRIS web app currently supports everything needed to manage risks and related artifacts, personas, and several of the visual models.  We are currently hard at work implementing the functionality that will make the web app functionally equivalent to the desktop app.  We're also developing a prototype *CAIRIS risk* app to explore the different forms that security design tools might take.

### We want your feedback ###

Although the web app is still in its early stages and unstable in places, we would love to get feedback on what people think about the tool.  We would particularly welcome [issues](https://github.com/failys/cairis/issues) if anything breaks, or ideas about features that people would like to see.
