Quick Start
===========

Live Demo
---------

A live demo of CAIRIS is available to use on https://demo.cairis.org.  

The demo has a test account (user: *test@test.com*, password: test) with two example databases you can explore: `NeuroGrid <https://cairis.readthedocs.io/en/latest/examples.html#neurogrid>`_ , `ACME Water <https://cairis.readthedocs.io/en/latest/examples.html#acme-water>`_.
You are also free to create your account to explore CAIRIS' capabilities on your own.

The live demo is rebuilt every night based on the latest updates to CAIRIS, so please feel free to add, update, or remove elements in the example models.
The test account is dropped and re-created each night with the sample models.  Other accounts created on the server are dropped on Sunday morning each week.

Video tutorials
---------------

The `CAIRIS YouTube channel <https://m.youtube.com/channel/UC21MvLyGwF9S0f9XlMLBA9Q>`_ has several short video primers.  These include an overview of the UI, and guidance on using CAIRIS for different design activities.


Example models
--------------


Define your contexts of use
---------------------------

How you use CAIRIS depends on how you approach the early stages of your design.  You will, however, need to work with  :doc:`environments </environments>` to represent your contexts of use.  Each model comes with a *Default* environment, but you may wish to add more later as you learn more about different contexts.

Save early and often
----------------------

You should :doc:`save </io>` your working model early and often.  Saving a model in CAIRIS entails exporting it.  CAIRIS models are XML, so easy to edit using other tools and easy to version control. 

Supporting UX
-------------

CAIRIS supports the creation and management of :doc:`personas </roles_personas>` to represent archetypical users, and :doc:`tasks </tasks>` to describe how these interact with the system being designed.  You need to define :doc:`roles </roles_personas>` that the personas fulfil before creating personas, and personas before creating tasks.  As your design evolves `task models <http://cairis.readthedocs.io/en/latest/tasks.html#visualising-tasks>`_ and `risk analysis models <http://cairis.readthedocs.io/en/latest/risks.html#risk-analysis-model>`_ will summarise the impact that security and usability are having on each other.

Asset-driven security design
----------------------------

Once you've specified at least one environments, you can start modelling :doc:`assets </assets>` : the things that are important to you.  You should model relationships between them to help you make sense of your growing design, and identify new assets you need to protect.  As asset models gives you ideas about possible system weaknesses, record these as :doc:`vulnerabilities </vulnerabilities>`.  As you think of new threats, note who you think the :doc:`attacker </attackers>` might be, and what :doc:`threats </threat>` they might carry out.  Armed with these insights, you can then create :doc:`risks </risks>` that bring everything together.  Based on these risks, you can decide how to :doc:`respond </responses>` and add :doc:`countermeasures </countermeasures>` to mitigate them.

Threat-driven security design
-----------------------------

You don't have to start your design by thinking about assets.  CAIRIS encourages the early creation of `threat models </https://cairis.readthedocs.io/en/latest/threats_tm.html>`_, which can be useful if you're still trying to make sense of what the system is and how attackers might exploit it.  This can help you better understand what your assets are, and even help you understand what the usability implications of certain threats might be.

Working with requirements
-------------------------

The earlier you start finding :doc:`requirements </gro>`, the easier it will be to spot other issues in your design.  CAIRIS lets you model requirements as goals, requirements, and use cases.

Thinking about architecture
---------------------------

Requirements aren't always easy to find, and sometimes thinking about possible architectures can help you work backwards.  You can use :doc:`architectural patterns </architecturalpatterns>` as building blocks and introduce these into environments to see risks they might be exposed to, or how they might impact personas and tasks.  You can also use :doc:`security patterns </patterns>` to see what their consequences of different pieces of *best practice* might have on your design.

Generating documentation
------------------------

Your stakeholders may not want to work directly with CAIRIS, so you can :doc:`generate documentation </gendoc>` to share your design documentation with others.
