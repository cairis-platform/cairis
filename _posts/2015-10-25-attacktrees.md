---
layout: post
title:  "Incorporating attack trees into CAIRIS"
date:   2015-10-25 14:00:00
categories: CAIRIS
description: Attack trees are great for ideation, but how do you integrate them into a larger system's design with the minimum of effort?
author: Shamal Faily
image:
  teaser: attacktree_teaser.gif
---

Although CAIRIS was designed as a security requirements management tool, it's a big tool which does much more than just manage requirements.  This is the first of a series of postings that describes just some of the things you can do with CAIRIS.

In this posting, we look at how attack trees can be incorporated into CAIRIS.  Attack trees are a formal, methodical way of describing the security of systems ([Schneier, 1999](https://www.schneier.com/paper-attacktrees-ddj-ft.html)).  They are a lightweight approach for modelling attacks; this is a good thing as they are simple enough that people can quickly create and contribute to them.  Once the trees are created, it would be useful if these could be incorporated into a larger system's design with the minimum of effort.

Attack trees have been used in conjunction with CAIRIS during the design of [webinos](http://webinos.org), but CAIRIS was only used to support the [creation and management of attacker personas](http://www.shamalfaily.com/wp-content/papercite-data/pdf/atfa11.pdf).  Once the insights had been drawn from the attack trees and incorporated into the other design models, they were largely forgotten.  However, it might be useful to have these attack trees around in some form, in case people want to see how resulting threats or vulnerabilities arose.

CAIRIS doesn't support attack trees, but it does support KAOS obstacle models.  Obstacles are conditions representing undesired behaviour that prevent an associated goal from being achieved ([van Lamsweerde and Letier, 2000](https://www.info.ucl.ac.be/~avl/files/TSE-Obstacles.pdf)), where the *associated goal* is some form of requirement the system needs to satisfy.  The obstacle model is represented using the same top-down approach notation as attack tree, so they seem a good candidate for representing the attacks and the sort of things that need to hold for an attack to be successful.

To illustrate how we can incorporate attack trees into CAIRIS using obstacle models, let's look at a simple example.

We teach attack trees to our second-year ethical hacking students at [BU](https://www1.bournemouth.ac.uk), and we encourage them to use low fidelity approaches for modelling their trees; this ensures technology doesn't get in the way of ideation.  Our students are taught how to identify and exploit vulnerabilities using tools like [nmap](http://nmap.org) and [metasploit](http://metasploit.com), and attack trees allow them to visualise what they have done, so they can explain their attacks to others.

Here is an example of a partially complete attack tree that arose when discussing how a vsftpd backdoor in Metasploitable might be exploited.

![attackTreeSketch]({{ site.baseurl }}/images/Exploit_vsftpd_backdoor_sketch.pdf)

We can quickly render this tree into something machine readable using [graphviz](http://www.graphviz.org).  Here is the attack tree rendered in graphviz's [Dot language](http://www.graphviz.org/content/dot-language) (downloadable from [here]({{ site.baseurl }}/images/Exploit_vsftpd_backdoor_graphviz.dot)).

```
digraph AT {
  "Backdoor to host" [shape=box,style=rounded];
  "or_1" [shape=triangle,label="or"];
  "Exploit vsftpd backdoor" [shape=box,style=rounded];
  "and_1" [shape=triangle,label="and"];
  "Telnet to vulnerable host" [shape=box,style=rounded];
  "Append smiley to credentials" [shape=box,style=rounded];
  "Run vsftpd as daemon" [shape=box,style=rounded];
  "or_2" [shape=triangle,label="or"];
  "and_2" [shape=triangle,label="and"];
  "Disable telnet" [shape=box];
  "Install exploited vsftpd package" [shape=box,style=rounded];
  "Build exploited vsftpd software" [shape=box,style=rounded];
  "Download exploited vsftpd source" [shape=box,style=rounded];
  "Compile exploited vsftpd source" [shape=box,style=rounded];
  "Configure inetd for vsftpd" [shape=box,style=rounded];
  "Disable vsftpd in inetd" [shape=box];

  "Backdoor to host" -> "or_1" [dir=none];
  "or_1" -> "Exploit vsftpd backdoor" [dir=none];
  "Exploit vsftpd backdoor" -> "and_1" [dir=none];
  "and_1" -> "Telnet to vulnerable host" [dir=none];
  "Telnet to vulnerable host" -> "Disable telnet" [dir=none];
  "and_1" -> "Append smiley to credentials" [dir=none];
  "and_1" -> "Run vsftpd as daemon" [dir=none];
  "Run vsftpd as daemon" -> "or_2" [dir=none];
  "or_2" -> "Install exploited vsftpd package" [dir=none];
  "or_2" -> "Build exploited vsftpd software" [dir=none];
  "Build exploited vsftpd software" -> "and_2" [dir=none];
  "and_2" -> "Download exploited vsftpd source" [dir=none];
  "and_2" -> "Compile exploited vsftpd source" [dir=none];
  "and_2" -> "Configure inetd for vsftpd" [dir=none];
  "Configure inetd for vsftpd" -> "Disable vsftpd in inetd" [dir=none];
}
```

This is the model generated by graphviz based on the Dot file.

![attackTreeRendered]({{ site.baseurl }}/images/Exploit_vsftpd_backdoor_png.png)

CAIRIS can import an attack tree rendered in Dot and convert this to an obstacle model, but two pieces of information need to be provided first:

* The context of analysis.  Environments are a first class object in CAIRIS, and an attack tree that might be effective in one context might not be in another.  It is, therefore, necessary to provide an indication of the context the attack tree should be situated in.

* The model contributors.  CAIRIS is concerned about the people that contribute to the model, so we should provide some details about how created the model so the contributors can be contacted should any queries arise resulting from the attack tree.

Armed with this information, we can import the attack tree into CAIRIS, but selecting the System / Import Model, selecting 'Attack Tree (Dot)' from the combo box, and providing the above information.

With the model now imported into CAIRIS, it's possible to visualise the model and start integrating insights from the model into the rest of a system's design.

 ![atObsModel]({{ site.baseurl }}/images/Exploit_vsftpd_backdoor_obstacleModel.png)
