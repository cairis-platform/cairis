---
layout: post
title:  "Easing the process of adopting CAIRIS"
date:   2016-04-23 13:10:00
categories: CAIRIS
description: Test, packages, and more
image:
  teaser: easingadoption_teaser.gif
---

## Easing the process of adopting CAIRIS ##

Although the blog has been quiet in recent months, a lot has been happening with CAIRIS.  As a result of this work, it's now easier than ever for both users and developers to adopt the tool.  Here is a quick summary of these changes.

* The CAIRIS source code on [github](https://github.com/failys/cairis) has been reorganised.  Everything is now properly structured into modules, making it easier for new developers to figure out where everything is, and how different components work together.

* We've introduced several initiatives to improve the code quality and maintainability of CAIRIS.  The repository has now been linked up with [Travis](https://travis-ci.org/failys/cairis) and [Coveralls](https://coveralls.io/github/failys/cairis?branch=master), to provide continuous integration and coverage testing for repository changes.  The repository also has [requires.io](https://requires.io/github/failys/cairis/requirements/?branch=master) integration, to ensure that CAIRIS' dependencies are automatically monitored.  We've added badges to the README file on github, so people can quickly check CAIRIS' stability.

![fig:github_bages]({{ site.baseurl }}/images/github_badges.jpg "Github badges")

* CAIRIS is now available as a package on [PyPI](https://pypi.python.org/pypi/cairis).  As you will see on the [installation page](http://cairis.org/install/), this vastly simplifies the installation process; this now entails little more than installing dependent packages, installing CAIRIS using `pip install`, and running a script to configure the CAIRIS database.  Moreover, we're currently working on a Debian package for CAIRIS so, very soon, it will be possible to install and configure CAIRIS using just a single command.

* We've started the process of integrating [CAIRIS-web](https://github.com/RobinQuetin/CAIRIS-web) into the master CAIRIS repository.  In the first instance, we will be developing web services for frequently used CAIRIS functionality.  However, in time, we plan to re-start work on a CAIRIS web app.

Watch this space for further updates on some of the above initiatives!
