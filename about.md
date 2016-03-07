---
layout: default
title: About CAIRIS
---

{% include toc.html %}

<h2>What is CAIRIS?</h2> 

CAIRIS stands for *Computer Aided Integration of Requirements and Information Security*.  It was designed to be a security requirements management tool, and was built from the ground up to support all the elements necessary for usability, requirements, and risk analysis.  

<h2>Why did you build CAIRIS?</h2>

CAIRIS was developed as part of [Shamal Faily](http://shamalfaily.com)'s [doctoral research](http://ora.ox.ac.uk/objects/uuid:520b939f-b1d9-4a53-9a47-21f0ffcfd68d).  CAIRIS was designed and developed to better understand the form that software tools for secure and usable software design might take.

<h2>Why do I need CAIRIS?</h2>

No-one disagrees that security should be considered as early as possible when designing software, but how do you do this productively, i.e. without security getting in the way of the business of understanding the software's core functional goals?

CAIRIS helps by supporting the usability, security, and requirements engineering activities that one might use at the initial stages of a project.  If you're undertaking these activities then you're collecting data that needs to go somewhere.  By using CAIRIS as a repository for this data, you will benefit from CAIRIS' automatic analysis and visualisation capabilities.

<h2>What does CAIRIS do that other tools do not?</h2> 

Several things.

First, some tools focus on the specification of requirements.  Others focus on modelling requirements together with related concepts.  Still others are centered around managing UX data.  CAIRIS is the only tool that does all of this (and more).

Second, CAIRIS is, to the best of our knowledge, the only security design tool that supports the notion of *environments*.  If you're building a medical data repository that will be used by different communities of users, you will be concerned about the nuances each community has about an asset's security properties.  For example, *clinical data* might have a high confidentiality value to one community, but low confidentiality value in other; this difference in properties may be due to the level of anonymisation this asset might be subjected to in each community.  Similarly, each community might have threats, vulnerabilities, people that look similar but have subtle variations.  CAIRIS can capture these variations, thereby allowing the impact of design changes, or changes in people's characteristics and tasks to be examined for each 'context of use'.

Third, CAIRIS is scaleable.  In most other tools, analysts are required to build models by hand.  However, as models get bigger, this task gets increasingly harder.  CAIRIS addresses this by automatically generating models based on connections between concepts that analysts make.  CAIRIS deals with the messiness associated with visualising this data, so you don't have to.

Fourth, CAIRIS doesn't attempt to be the 'one tool that rules them all'.  CAIRIS works best when used in combination with other 'best of breed' tools.  For example, CAIRIS has been used to import data from sources ranging from wiki pages and spreadsheets, to open source repositories about attack patterns.  Moreover, in addition to generating models and documentation, CAIRIS can generate goal models that can be imported into other tools like [jUCMNav](http://jucmnav.softwareengineering.ca/ucm/bin/view/ProjetSEG/WebHome).  Because of how CAIRIS has been implemented, it's also fairly easy to develop extensions for importing and exporting data.

Finally, although CAIRIS' origins are in specifying requirements, it has been recently extended to support the specification and analysis of software architectures as well.  To date, we believe CAIRIS to be the only tool that supports the specification and analysis of both security requirements and security architectures.

<h2>Is CAIRIS used in the real world?</h2>

CAIRIS has been used in a number of real-world case studies.  You can read about some of these studies [here]({{site.baseurl }}/papers.html).  We're currently working with a number of companies (both large and small) who are looking to adopt CAIRIS.  

We're always interested in hearing from others interested in adopting the tool, so please [get in touch](mailto:sfaily@bournemouth.ac.uk) if you want to use CAIRIS and need help getting started.

<h2>Are there any examples of CAIRIS in action?</h2>

Yes, see the [Examples](http://cairis.org/examples) page.

The [design data](https://github.com/webinos/webinos-design-data) for [webinos](http://webinos.org) is also based on CAIRIS.  

We are currently working on [a project to build specification exemplars for critical infrastructure systems](https://cybersecurity.bournemouth.ac.uk/?page_id=55); these models will be based on CAIRIS.  [ACME Water](http://cairis.org/ACME_Water) is the first of these exemplars.  We are currently building a second exemplar based on a rail company.  Please [get in touch](mailto:sfaily@bournemouth.ac.uk) for more information if these models or this project is of interest.

<h2>Is CAIRIS free?</h2> 

Yes.  CAIRIS has been made freely available under an Apache Software License.  You can find the source code for CAIRIS on [github](https://github.com/failys/CAIRIS).

<h2>Does CAIRIS only work on Linux?</h2> 

CAIRIS will run on any platform that supports its open source dependencies.  Although it works best on Linux (particularly Debian based distributions), it has been known to run on Mac OS X and Windows as well.  Because of its architecture, there is no reason why the server side components can't run on one platform, and the client side components can't run on another.

<h2>Are there plans for a CAIRIS webapp?</h2> 

[Robin Quetin](https://github.com/RobinQuetin) developed a proof-of-concept [CAIRIS web app](https://github.com/RobinQuetin/CAIRIS-web).  This is no longer being actively developed, but we are looking at how to integrate aspects of this work back into the main [CAIRIS repository](https://github.com/failys/CAIRIS).

<h2>I'm not very Linux savvy.  Is there something like a package or install script I can run, or a pre-built VM image I can download?</h2> 

You can download a Linux virtual appliance from [here](https://drive.google.com/open?id=0Bx5c5XNaOMoTM1RsclRjYTVSSGs).

There is no 'officially supported' install script yet, but [Robin Quetin](https://github.com/RobinQuetin) did create an [install script](https://github.com/RobinQuetin/CAIRIS-web/blob/develop/cairis/scripts/install_debian.sh) for his [CAIRIS web app](https://github.com/RobinQuetin/CAIRIS-web) prototype.  Adapting this script is on our 'to do' list, but interested contributors are more than welcome to adapt this or develop an alternative script, and submit to the CAIRIS code base :-)

<h2>Do you still do research around CAIRIS?</h2> 

Very much so.  We have a number of undergraduate and postgraduate research assistants that are currently extending CAIRIS, and exploring some of the ideas that originally motivated its development.  We love to hear from prospective collaborators, so if working with us to improve the state of the art in security design tools is of interest then please [get in touch](mailto:sfaily@bournemouth.ac.uk).

<h2>How can I contribute to CAIRIS?</h2> 

You can contribute in several ways.

* You can use CAIRIS in your own practice.  One of our aims in developing CAIRIS is to transfer knowledge about security design tool best practice, so by using CAIRIS you will be helping us do this.  We welcome problem reports or feature requests; you can contribute these by doing little more than raising [an issue on github](https://github.com/failys/CAIRIS/issues), or [getting in touch](mailto:sfaily@bournemouth.ac.uk) if your requirements are a little more elaborate.
* If you work in higher education, please consider using CAIRIS as a tool for teaching security design.  CAIRIS has already been used in [Oxford](http://www.cs.ox.ac.uk)'s postgraduate [Design of Security](http://www.cs.ox.ac.uk/softeng/subjects/DES.html) course.  At [BU](https://www1.bournemouth.ac.uk), we're also incorporating CAIRIS into our own cybersecurity teaching.  We're happy to share any teaching material we develop, so if you're interested in using CAIRIS as part of your teaching then please [get in touch](mailto:sfaily@bournemouth.ac.uk).
* We're always looking for people to help with general maintenance activities.  The CAIRIS documentation is a little out of date in places, and a number of really interesting features (e.g. the functionality associated with specifying and analysing software architectures) isn't documented as well as it could be.  We would also love to hear from people interested in looking at how CAIRIS can be best packaged, given the various platforms and infrastructures they might wish to use CAIRIS for.

<h2>How can I sponsor CAIRIS?</h2> 

We'd love to hear from companies interested in sponsoring the on-going design and evolution of CAIRIS.  You can sponsor us in lots of different ways.  These include:  

* Providing people to help maintain and grow CAIRIS.  
* Providing [modest] financial support we can use to employ interns to develop CAIRIS.
* Buying consultancy to help you adopt CAIRIS.  Any income from CAIRIS consultancy, will go back into the development of CAIRIS.  
* [Knowledge Transfer Partnerships (KTPs)](https://connect.innovateuk.org/web/ktp).  If you're a UK SME and see CAIRIS as an important tool in growing your business, then a KTP is a great way of getting government funding to support us and your project.

Please [get in touch](mailto:sfaily@bournemouth.ac.uk) if any (or all!) of the above is of interest to you.
