---
layout: post
title:  "Threat Modelling, Documentation and More"
date:   2017-10-20 14:06:00
categories: CAIRIS
description: Just because we've been quiet doesn't mean we haven't been busy
image:
  teaser: dfd_teaser.gif
---

It's been a while since we last posted a blog update, but just because we've been quiet doesn't mean we haven't been busy.  
The below is just a summary of what has been keeping us busy recently.

### Better support for threat modelling ###

![DFD]({{ site.baseurl }}/images/DFD.jpg)

At [ESPRE 2017](http://espre2017.org), we presented work on [how CAIRIS might be used to better support collaboration between security and usability engineers](http://www.shamalfaily.com/wp-content/papercite-data/pdf/faia17.pdf).  This paper not only described CAIRIS' support for [attack tree modelling](http://cairis.org/cairis/attacktrees/), and [automation for persona creation](http://cairis.org/cairis/trello/), it also showcased new functionality for creating data flow diagrams.   In addition to support for DFDs, we've also created a new 'threat model' view on the CAIRIS home page.  This is analogous to a STRIDE table, and shows how data flow diagram elements in a given environment are exposed to threats specific to different security and privacy properties.

### Deprecating the desktop application ###

Our ESPRE 2017 paper was also a showcase for the CAIRIS web client, which is now the recommended front-end when working with CAIRIS.  The CAIRIS desktop application is still available, but is now considered deprecated.  Almost all of the functionality supported by the desktop application has now been incorporated into the web client, and there is much functionality in the web client which isn't in the desktop app.  Consequently, if you are still using the desktop app, we would encourage you to start using the web client instead.  As you'll see, as well as being easier and more intuitive to use, it's also a lot easier to setup.

### More stability ###

We used the opportunity of migrating from the desktop to the web client to improve the stability and resilience of CAIRIS in general.  We closed a lot of long standing open [issues](https://github.com/failys/cairis/issues), updated the back-end codebase to be compatible with Python 3, and discovered and resolved lots of issues in the web client.  There may still be other issues with the web client, so please don't hesitate raising an issue if, while using CAIRIS, something doesn't feel right.

### Better documentation ###

![RTD]({{ site.baseurl }}/images/rtd.jpg)

We've also started the long-overdue overhaul of CAIRIS' documentation.  Until recently, this was maintained in github pages.  We've now make the documentation part of the codebase, and made the documentation available on the excellent [Read the Docs](http://cairis.readthedocs.io/en/latest/) platform.  The documentation for the desktop application has now been updated to reflect the web client, and we've started to document areas of CAIRIS we never got around to properly documenting first time around, e.g. use cases, traceability, etc.   There is still a lot to update, so if there is something you particularly want to see documented now then please raise an issue and we'll look at prioritising what you need.   We would also welcome pull requests for any typos you find, or general improvements you think might be useful.

### Better demonstrations ###

If you've been following this blog then you will know we trialled a live demo of CAIRIS a few months ago.  The live demo now has a permanent home -- http://demo.cairis.org.  We've made some tweaks to the configuration of the live demo, so -- even though the demo runs in the cloud -- it's performance should be almost as good as if the CAIRIS container was running on your desktop or within a VM.

CAIRIS now has support for multiple databases, which means we can now load both of the CAIRIS exemplar models on the live demo:  NeuroGrid and ACME Water.   Once you login (user: test, password: test), just click on the System / Open Database menu, and select the model you want to play with.  The demo is rebuilt from the latest CAIRIS sources every night, so please feel free to create new models or edit existing ones as you see fit.
