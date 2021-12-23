---
layout: page
title: About CAIRIS
---

{% include toc.html %}

<h2>What is CAIRIS?</h2>

CAIRIS stands for *Computer Aided Integration of Requirements and Information Security*.  It is a platform for eliciting, specifying, and validating secure and usable systems.  It was built from the ground up to support all the elements necessary for usability, requirements, and risk analysis.  

<h2>Why did you build CAIRIS?</h2>

CAIRIS initially developed over 10 years ago as part of [Shamal Faily](https://rgu-repository.worktribe.com/person/1335432/shamal-faily)'s [doctoral research](http://ora.ox.ac.uk/objects/uuid:520b939f-b1d9-4a53-9a47-21f0ffcfd68d) to better understand what software tool support for security and usability design might take.

<h2>Why do I need CAIRIS?</h2>

No-one disagrees that security should be considered as early as possible when designing software, but how do you do this productively, i.e. without security getting in the way of the business of understanding the software's core functional goals?

CAIRIS helps by supporting the usability, security, and requirements engineering activities that one might use at the initial stages of a project.  If you're undertaking these activities then you're collecting data that needs to go somewhere.  By using CAIRIS as a repository for this data, you will benefit from CAIRIS' automatic analysis and visualisation capabilities.

<h2>What does CAIRIS do that other tools do not?</h2>

Several things.

First, some tools focus on the specification of requirements.  Others focus on modelling requirements together with related concepts.  Still, others are centred around managing UX data.  CAIRIS is the only tool that does all of this (and more).

Second, CAIRIS is, to the best of our knowledge, the only security design tool that supports the notion of *environments*.  If you're building a medical data repository that will be used by different communities of users, you will be concerned about the perceptions stakeholders in each community might have about security, and what this means when determining the value of an asset, or the impact of a risk.  For example, *clinical data* might have a high confidentiality value to one community, but low confidentiality value in other; this difference in properties may be due to the level of anonymisation this asset might be subjected to in each community.  Similarly, each community might have threats, vulnerabilities, people that look similar but have subtle variations.  CAIRIS can capture these variations, thereby allowing the impact of design changes or changes in people's characteristics and tasks to be examined for each 'context of use'.

Third, CAIRIS is scaleable.  In most other tools, analysts are required to build models by hand.  However, as models get bigger, this task gets increasingly harder.  CAIRIS addresses this by automatically generating models based on connections between concepts that analysts make.  CAIRIS deals with the messiness associated with visualising this data, so you don't have to.

Fourth, CAIRIS doesn't attempt to be the 'one tool that rules them all'.  CAIRIS works best when used in combination with other 'best of breed' tools.  For example, CAIRIS has been used to import data from sources ranging from wiki pages and spreadsheets, to open source repositories about attack patterns.  More recently, as illustrated [here](https://cairis.readthedocs.io/en/latest/usergoals.html#working-with-workbooks), we've been looking at how we can create partially populated Excel workbooks that users can complete and re-import back to CAIRIS.  CAIRIS also has an [API](https://app.swaggerhub.com/apis/failys/CAIRIS), which makes it possible to build apps that work with data from CAIRIS and other tools.  Because of how CAIRIS has been implemented, it's also fairly easy to [extend CAIRIS](https://cairis.readthedocs.io/en/latest/extending.html).

Finally, although CAIRIS' origins are in specifying requirements, it can also support the specification and analysis of software architectures as well.  To date, we believe CAIRIS to be the only tool that supports the specification and analysis of both security requirements and security architectures.

<h2>Is CAIRIS used in the real world?</h2>

CAIRIS has been and is currently being used commercially, particularly in critical infrastructure domains such as Defence, Health, Transport, and Water Treatment.  We're always keen to hear from companies (both large and small) interested in using CAIRIS.  Please [get in touch](mailto:s.faily@rgu.ac.uk) if you want to use CAIRIS and need help gettting started.

<h2>Are there any examples of CAIRIS in action?</h2>

Yes, there are several [example models](https://cairis.readthedocs.io/en/latest/examples.html) you can look at and play with.

<h2>Is there is a live demo of CAIRIS that I can play with?</h2>

Yes.  You can get started [here](https://cairis.org/cairis/cloud/).

<h2>Is CAIRIS free?</h2>

Yes.  CAIRIS has been made freely available under an Apache Software License.  You can find the source code for CAIRIS on [github](https://github.com/cairis-platform/cairis).

<h2>Does CAIRIS only work on Linux?</h2>

No, CAIRIS will run on any platform that supports its open source dependencies.  Although it works best on Ubuntu, it has been known to run on Mac OS X and Windows as well.  Because of its architecture, there is no reason why the server side components can't run on one platform, and the client side components can't run on another. CAIRIS has also been distributed as a Docker container, which will run on any platform that supports Docker.

<h2>Do you still do research around CAIRIS?</h2>

Very much so.  We have a number of undergraduate and postgraduate research assistants that are currently extending CAIRIS, and exploring some of the ideas that originally motivated its development.  We love to hear from prospective collaborators, so if working with us to improve the state of the art in security design tools is of interest then please [get in touch](mailto:s.faily@rgu.ac.uk).

<h2>How can I contribute to CAIRIS?</h2>

You can contribute in several ways.

* You can use CAIRIS in your own practice.  One of our aims in developing CAIRIS is to transfer knowledge about security design tool best practice, so by using CAIRIS and sharing your experiencees with us, you will be helping us do this.  
* Report problems or feature requests by raising [an issue on github](https://github.com/cairis-platform/cairis/issues), or [getting in touch](mailto:s.faily@rgu.ac.uk) if your requirements are a little more elaborate.
* If you work in higher education, please consider using CAIRIS as a tool for teaching security design.  CAIRIS has already been used in [Oxford](http://www.cs.ox.ac.uk)'s postgraduate [Design of Security](http://www.cs.ox.ac.uk/softeng/subjects/DES.html) course.  [Bouremouth University](https://www1.bournemouth.ac.uk) and [Robert Gordon University](https://rgu.ac.uk) has also incorporated CAIRIS into its cybersecurity teaching.  We're happy to share any teaching material we develop, so if you're interested in using CAIRIS as part of your teaching then please [get in touch](mailto:s.faily@rgu.ac.uk).
* We're always looking for volunteers to help maintain and evolve CAIRIS - this includes not only the code, but other elements of CAIRIS such as documentation and even this website.

<h2>How can I sponsor CAIRIS?</h2>

We'd love to hear from companies interested in sponsoring the on-going design and evolution of CAIRIS.  You can sponsor us in lots of different ways.  These include:  

* Providing people to help maintain and grow CAIRIS.  
* Providing [modest] financial support we can use to employ interns to develop CAIRIS.
* Buying consultancy to help you adopt CAIRIS.  Any income from CAIRIS consultancy, will go back into the development of CAIRIS.  
* [Knowledge Transfer Partnerships (KTPs)](https://connect.innovateuk.org/web/ktp).  If you're a UK SME and see CAIRIS as an important tool in growing your business, then a KTP is a great way of getting government funding to support us and your project.

Please [get in touch](mailto:s.faily@rgu.ac.uk) if any (or all!) of the above is of interest to you.
