---
layout: post
title:  "Building personas into design tools: why CAIRIS does it, and how"
date:   2015-11-05 07:00:00
categories: CAIRIS
description: Four guideline for integrating personas into software engineering tools
image:
  teaser: cvertduc_teaser.gif
---

## What are personas? ##

Personas are behavioural specifications that embody the goals and needs of archetypical users.  By *specification*, we usually mean some sort of narrative description, and by *archetypical* we mean typical users that might use some product or service we are building or evaluating.  They were originally introduced to deal with developer biases arising from the word 'user'; these biases might lead developers to bend and stretch assumptions about what 'users' should actually do.

## Why incorporate personas into design tools? ##

Lots of people have talked about how personas might be better integrated into the software toolset of designers and engineers.  However, when we looked at how this might be done, we found very few (if any) examples of how this works in practice.  As UX is largely craft-based, this isn't entirely surprising, but if we are serious about using personas to provide assurance for large scale and/or critical systems then this becomes problematic.  In such systems, personas might be woven into different design models, and different levels of abstraction.  If personas aren't properly specified, validated, or maintained then they might lead to exactly the sort of problems that personas were originally meant to solve.

## How does CAIRIS do it? ##

If you want full details of how CAIRIS acts as an exemplar for integrating personas into software engineering tools (and how this works on a real project) then you should take a look at our [EICS 2013 paper](http://www.shamalfaily.com/wp-content/papercite-data/pdf/faly131.pdf). However, if you're looking for a quick radio edit of the paper then CAIRIS does it by following four guidelines.

### 1. CAIRIS makes persona characteristics explicit ###

The rationale underpinning persona characteristics should be available from the interfaces where persona narratives are displayed.

We have found that people new to personas have problems trusting their fictional narratives. We can start building trust by providing some rationale for their description at the point when this rationale might be needed.  If this rationale is visualised, it also helps spot fallacies that might be underpinning persona characteristics.

In CAIRIS, we use [argumentation models](http://www.shamalfaily.com/wp-content/papercite-data/pdf/fafl108.pdf) to provide this rationale.  Here is an example of the argument underpinning the characteristic 'Contextual variety encourages rather than discourages user-centeredness'.

![fig:argModel]({{ site.baseurl }}/images/cvertduc.pdf "Argumentation model example")

These visualisations are linked to persona narratives in CAIRIS using context-specific menus, so you can quickly compare and contrast the visual rationale with the narrative text.


### 2. CAIRIS integrates qualitative data analysis ###

As useful as argumentation models are for providing assurance about personas, useful insights that might arise when creating personas might be lost once personas are created.  To capture these insights, tools should do more than just maintain persona specifications; they should provide the analytical support necessary to create them as well.

A few years ago, we presented a framework for [persona cases](http://www.shamalfaily.com/wp-content/papercite-data/pdf/fafl111.pdf) at CHI, illustrating how qualitative data analysis approaches can be used to create persona characteristics that stand up to validation.  Because commercial [CAQDAS tools](http://www.surrey.ac.uk/sociology/research/researchcentres/caqdas/) like [atlas.ti](http://atlasti.com) or [NVivo](http://www.qsrinternational.com/product) are out of the reach of many designers, CAIRIS incorporates all the elements necessary to support qualitative analysis needed to build persona cases.  This includes the ability to qualitatively code source data, annotate text with memos, and model relationships between codes.  As the below figure shows, we also added support for showing the role that each code relationship and quotation plays in justifying a particular persona characteristic.

![fig:editImplChar]({{ site.baseurl }}/images/EditCharacteristic.pdf "Edit implied characteristic")

<h3>3. CAIRIS facilitates persona interchange</h3>

Interoperability is important if we want designers using different tools to use personas.  CAIRIS already supports model interchange using XML, so this seemed a reasonable basis upon which personas might be exchanged.

Rather than forcing designers to create CAIRIS models just for interchanging personas and persona related data, we modified the DTD for CAIRIS 'usability' element to make it easier to create individual XML files for a given persona and its underlying data; this is shown in the UML class diagram below.

![fig:usabilityDTD]({{ site.baseurl }}/images/UsabilityDTD.pdf "Class diagram of persona DTD structure")

You can find lots of examples of how these persona XML models look in practice by browsing the [personas in the webinos design data repository on github](https://github.com/webinos/webinos-design-data/tree/master/personas).

### 4. CAIRIS is conducive to persona version control ###

If you're serious about persona interchangeability, you also want to be concerned about how personas are going to evolve in line with other design models as well.  If personas are to be accorded the same consideration as other models by a project team then, if other models are version controlled, personas should be as well.

Building on the previous guideline, this can be implemented quickly by storing personas in individual XML files, and adding them to a suitable version control system like [git](https://git-scm.com).

As we saw [here](https://github.com/webinos/webinos-design-data/tree/master/personas), this solution is trivial to implement if you're using something like [github](https://github.com).  As our webinos-data-data repository also illustrates, we can even incorporate personas into [build scripts](https://github.com/webinos/webinos-design-data/tree/master/scripts), so we can see if and how, from a design perspective, personas might 'break the build'.

<h2>Food for thought?</h2>

In building personas into CAIRIS, we had three goals to get people thinking about tools for personas.

First, we wanted to draw attention to the need for decent-tool support for personas.  We don't see how personas can be seriously integrated into all stages of a product's design and engineering activities without it.

Second, we wanted to provide an actual example of a software tool that 'builds personas in'.  The need for supporting persona interchangeability and version control seems self-evident now, but -- in incorporating personas in CAIRIS -- we have demonstrated how this looks in practice.

Finally, we wanted to raise the broader question 'whither software tools for personas?'.  For example, we have shown how version control for personas might work, but we were also dealing with anonymised data.  Providing these examples may not have worked out so well if we were working with sensitive data where more elaborate access control was a requirement. Still, provisioning CAIRIS for personas did at least raise issues that might have otherwise remained hidden.

Over to you?
