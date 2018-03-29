---
layout: default
title: Rick
description: A plant operator at ACME water
categories: persona
image:
  teaser: Rick_teaser.gif
---

{% include toc.html %}

# Rick

![fig:RickPortrait]({{ site.baseurl }}/images/Rick_portrait.jpg "Rick")

[Image source](https://www.flickr.com/photos/savidgefamily/6962111611)

## Narrative


#### Activities

Rick is a clean-water plant operator, responsible for ensuring that
water processed through the plant is in line with specified set-points.
Rick's area of responsibility extends outside of the confines of the
plant to include checking on pumping stations, which feed water into the
plant's nearby reservoir.

During his working shifts (he works a 5 + 1 continental shift), Rick
frequently checks readings on his SCADA workstation, takes water samples
at various locations around the plant, and responds to alarms raised by
the SCADA system; if necessary this involves investigating problems,
and -- if no remedial tasks are possible -- calling someone out to
investigate further.

At the start of every shift, Rick checks AJS to see what work he is
scheduled to carry out. He usually updates AJS based on the work he
carried out before the end of his shift. Rick also maintains a paperwork diary, which is updated after carrying out specific work or
responding to problems. This, together with the status whiteboard, is
also useful for explaining any on-going issues when handing over to the
next shift.

#### Attitudes

Rick isn't particularly concerned about people trying to hack into the
SCADA system he uses. "The only way the SCADA will get infected", Rick
says, "is by an instrument tech plugging a virus infected laptop into
it".

Rick is aware of Information Security communiques on InfoPortal but
doesn't see how this is relevant to him. "We don't have laptops", says
Rick, "and we don't leave the site, so we don't leave anything in cars".
Rick is, however, aware of Information Security controls. Rick knows
that logout policies keep intruders from getting access to his
workstation (although he thinks the logout period is too short given his
environment), and he knows he can only access certain pumping sites via
the telemetry system.

Although Rick can call an instrument tech for many problems, experience
has taught him not to expect much from the ACME ICT support during a
night shift. "What's the point of calling up to say you can't login at
night if all you get is a reference number", Rick complains, "that won't
help me start my pumps now!" Although Rick knows he can call out an
instrument tech to help, he is also conscious that they are out most
evenings, and might not appreciate a call-out for a corporate ICT
problem.

#### Aptitudes

Rick has been a plant operator for over 10 years. Although the exact
procedures need to run his plant are documented in a works manual, he
doesn't need to refer to it. "I haven't read the works manual in years",
Rick says.

This experience does not stay in Rick's head. When problems have
occurred, he raises these during team meetings, and any lessons learned
sometimes find their way into the SCADA system as new functionality.
Rick is aware of the new EnterpriseSCADA developments and possible
improvements to the HMI and start-up procedure. Although not fully in
the loop about what is going on, he hopes that, like the current system,
there will be productivity improvements without an adverse impact.

Rick uses the SCADA's trend monitoring facilities as an indication of
possible problems. "If the trends freeze or flat-line", Rick says, "I
need to go out and take a look at what's wrong". Because problems occur
daily, and he is often on his own, Rick can still control the plant
using panel PCs at remote locations around the plant.

#### Motivations

Because the water quality can change over a matter of minutes, Rick's
ethos is that you need to be ready for anything. Because of this,
checking certain parameters and pieces of kit is an important
discipline, as is logging important events in the works diary and on the
status board; these aid communication to other shift members, and the
eventual piecing together of the elements of an event.

Although information security doesn't phase Rick too much, personal
security does. Potentially facing off a scrap metal thief is a big worry
for Rick. "The police don't respond to intruder alarms at a nearby
pumping station anymore due to false alarms", says Rick. "Because of
this, we've been told not to go out to these places on our own. We have
a lone-worker system when people call us when we get to a particular
station, but what happens if we get problems on the way?"

#### Skills

Rick has a basic operating knowledge of Windows; enough to carry out his
day-to-day routines, check his email and navigate the main sections of
InfoPortal.

Rick isn't a power-user; he acknowledges that younger "whizz kids" are
much more adept at using PCs than he is. Consequently, he only uses a
subset of the desktop icons currently on his desktop. "I don't know
what these other applications do", Rick says,"I've tried clicking on one
and it just gives me a Data Protection Warning. I guess this means I'm
not authorised to use it."

## Argumentation Models

#### Activities

![fig:RickActivities]({{ site.baseurl }}/images/RickActivitiesModel.pdf)

#### Attitudes

![fig:RickAttitudes]({{ site.baseurl }}/images/RickAttitudesModel.pdf)

#### Aptitudes

![fig:RickAptitudes]({{ site.baseurl }}/images/RickAptitudesModel.pdf)

#### Motivations

![fig:RickMotivations]({{ site.baseurl }}/images/RickMotivationsModel.pdf)

#### Skills

![fig:RickSkills]({{ site.baseurl }}/images/RickSkillsModel.pdf)

#### Document References

## References

#### Document References

|----------|---------|----------|
| Reference     |  Document     |     Excerpt |
| ----------------|---------------|--------------|
|  Alarms designed around past experience         |                            Site knowledge GT concept     |         Software people asked to set up alarms based on past problems forgetting about alarms.|
|  Anything could happen                           |                           Process impact GT concept    |          Anything could happen: pumps could fail; water quality can change within 10 minutes|
|  Bespoke systems harder to understand and support.       |                   Limited support knowledge GT concept  | Bespoke systems have problems that it takes a while to understand how it has been programmed.|
|  Callouts occur for anything other than a basic trip.            |           Alarm handling GT concept         |     Basic trips can be manually reset but anything more complicated warrants a call-out.|
|  Carries out tasks and records set-point readings             |              Work routine GT concept        |        Looks at tasks needed to be achieved in a day and set-points to be collected and recorded.|
|  Checking certain things is a discipline              |                      Site knowledge GT concept      |        Checking certain things e.g. coagulant levels is a discipline.|
|  Checks take place at certain times of the day                |              Trend monitoring GT concept  |          Checks are monitored throughout the works at certain times during the day.|
|  Copper theft                       |                                        Site threats GT concept     |           Sites have been broken into to steal earth connections and put through mains to get at copper.|
|  Corporate wifi insecurity                  |                                InfoSec indifference GT concept   |     The corporate wifi is not perceived to be secure as the access code is written down on a wall.|
|  Drifting trends indicate problems                |                          Trend monitoring GT concept     |       Trends drifting off are an indication that something has gone out of sync.|
|  Environmental Agency carry out river monitoring            |                External agencies GT concept      |     The Environmental Agency carry out their own river monitoring.|
|  Everything is logged              |                                         Business compliance GT concept     |    Everything that happens is logged.|
|  Experience contributes to asset management decisions.          |            Site knowledge GT concept       |       Experience about what goes wrong contributes to asset purchase decisions via AJS.|
|  Extreme scenarios                          |                                Unlikely threats GT concept    |        Scenarios of corrupt or missing files taking out a workstation are a bit extreme.|
|  Failures often occur when seasons change.          |                        Hazards GT concept            |         Failures often occur when seasons change.|
|  Familiarity with colour scheme standards.          |                        Site knowledge GT concept       |       People coming in from different plant are familiar with colour schemes.|
|  Few SCADA to EnterpriseSCADA process changes              |                 Process impact GT concept       |       Few process changes expected when old SCADA systems replaced with EnterpriseSCADA.|
|  Hacker aware           |                                                    InfoSec communication GT concept   |    Has read warning about people trying to hack machine on InfoPortal.|
|  Hacking indifference                  |                                     InfoSec indifference GT concept  |      Not worried about people trying to hack the SCADA systems.|
|  HMI usability improvements       |                                          Process Innovation GT concept     |     The new SCADA system is an improvement because there are only slight differences to the MMI.|
|  Infection only from engineers            |                                  Island mindset GT concept       |       A system only gets infected if an engineer connects their own infected laptop into it.|
|  InfoSec communiques irrelevant                    |                         InfoSec indifference GT concept       | Messages about leaving things and laptops in a car are not a problem; [we] do not go off site.|
|  Lack of night ICT support              |                                    ICT non-support GT concept      |       Why have night support if all you get is a logged reference number; you cannot hand the problem over to someone else.|
|  Line manager site authorisation          |                                  Authorisation restriction GT concept  | Can only access sites they have been authorised to; permission for authorisation changes need to be sought from the line manager.|
|  Lone worker vulnerability             |                                     Personal Security GT concept      |     Lone Working system is based on calling up someone when they get to a station; it does not help if you get problems on the way.|
|  Many desktop short-cuts do not get used.        |                           Unexplained feature GT concept     |    Most short-cuts and applications on the desktop have been around a while and do not get used.|
|  Massive and uncontrollable water input       |                              Hazards GT concept        |             It is not like a factory: it is a massive system with tonnes of debris that hits you all in one go.|
|  Migration pending resources         |                                       Interim Systems GT concept     |        Old PC applications will be migrated to SCADA when time and money is available.|
|  MS activities during start of day shift.            |                       Business compliance GT concept       |  Management System activities are carried out during the first hours of a day shift.|
|  MS workaround for intruder alarms.               |                          Business compliance GT concept    |     Lack of police response to intruder alarms led to two-man requirement for alarm response.|
|  Night shift tasks differ slightly from day.          |                      Work routine GT concept      |          Night shift tasks may be similar but slight different due to SAS sampling|
|  No alone out-of-hours visits           |                                    Personal Security GT concept    |       Never go alone when visiting a nearby site out-of-hours|
|  Non-authorised applications cannot be run            |                      Unexplained feature GT concept    |     Not being able to run applications means not authorised to use it.|
|  Notes are easier to read and hand-over              |                       Works diary GT concept         |        Easier to write things on notes. Also easier for person handed over to to just read the logs.|
|  Only general work and failures are logged       |                           Works diary GT concept     |            Supposed to write down everything but not enough pages; any general work carried out is logged - together with failures.|
|  Operators know what they need to do.             |                          Work routine GT concept     |           Operators come in and know what work they need to do.|
|  Out-of-spec alarms precipitate TIS call-outs                |               External agencies GT concept      |     Out of spec alarms are picked up Telemetry Information System; these lead to a technician call out; independent sampling; log checking.|
|  Periodic national security alerts              |                            big security worry GT concept       |   Regular emails are received about things like the Iraqi Wars and terrorism; it then goes quite for a while until the next event.|
|  Personal threats                |                                           Personal Security GT concept     |      Personal experience of being threatened when called out late at night and challenging intruders.|
|  Physical and login security                |                                InfoSec indifference GT concept   |     Once you are through the gate then security is the operator login.|
|  Plant can be operated away from the control room if necessary.      |       One-man site GT concept          |      Can run things from the other side of the plant; this is necessary when you are on your own.|
|  Process problems occur daily.                |                              Process impact GT concept       |       Process problems occur daily.|
|  Processes checked against spec                       |                      Scope of responsibility GT concept   |  Check the process and quality of final effluent meets critical parameters with EA specs.|
|  Pumping decisions rain based                      |                         Hazards GT concept          |           Decisions to pump are based on the rain forecast.|
|  Quick and automatic startup                    |                            Process Innovation GT concept     |     The workstation has been setup so as soon as Windows starts then so does EnterpriseSCADA (as a service); no user interaction is needed.|
|  Readings are taken from SCADA screens.                       |              Hardware checks GT concept         |    SCADA screens are checked to take readings about chemical dosing; iron levels; pH etc.|
|  Records piece things together                 |                             Site knowledge GT concept       |       Records are kept to help piece things together when things go wrong.|
|  Role restrictions                   |                                       Authorisation restriction GT concept  | Depending on what you are authorised to do - certain buttons for things like starting and stopping pumps will be greyed out.|
|  Room for improvement                         |                              Process Innovation GT concept   |       There is always scope to improve and automate as we go along.|
|  Shift based logouts                               |                         Logout policy GT concept            |   People want a shift based auto-logout feature.|
|  Short auto logout                             |                             Logout policy GT concept   |            Automatic logout occurs after a minute or two of inactivity.|
|  Site kept running at optimum efficiency                     |               Scope of responsibility GT concept  |   Keep site running at optimum efficiency|
|  Some plant operations are cheaper at night.        |                       Operational contexts GT concept    |    Pumps are run from some districts at night because the electricity is cheaper.|
|  Specific jobs are day shift related              |                          Work routine GT concept     |           Specific jobs are assigned to the day shift e.g. ordering chemicals|
|  Stand-alone SCADA                      |                                    Island mindset GT concept    |          Systems are stand-alone because they are not connected a network.|
|  Standards evolved over years                    |                           Local standards GT concept    |         Standards have been setup over the years.|
|  Status board communicates problems                |                         Site knowledge GT concept     |         Status board is used to communicate problems with bits of kit.|
|  Tasks entered into AJS are captured by WMS                |                 Corporate interface GT concept     |    Tasks are entered into Asset Job System are captured by Work Management System.|
|  The works diary is a controlled document.          |                        Business compliance GT concept    |     The works diary is a controlled document.|
|  Thieves steal anything                 |                                    Site threats GT concept      |          Thieves will steal anything.|
|  Trends identify plant problems            |                                 Trend monitoring GT concept      |      Trends are used to identify plant problems.|
|  Trouble-shooting driven by known task problems.            |                Site knowledge GT concept     |         Knowledge about coagulant problems leads to particular tasks being carried out e.g. flushing lines; to get everything back to normal.|
|  Uncertainty about EnterpriseSCADA ability to support general operations. |  Limited support knowledge GT concept |  Uncertainty about EnterpriseSCADA capabilities towards supporting general operations.|
|  Untimely logout annoyance            |                                      ICT non-support GT concept    |         It is annoying to nip downstairs and have to log back in when you come back.|
|  Vandalism assessed and mitigated             |                              Site threats GT concept      |          Vandalism has already been assessed and mitigated.|
|  Water entering plant checked against spec                  |                Scope of responsibility GT concept  |   Make sure water is in-spec coming into the plant.|
|  Water is sampled throughout the works              |                        Sample collection GT concept     |      All aspects of the water down in the works is sampled.|
|  Water scheme is geographically big                      |                   Water GT concept      |                 The scheme covers where water is sourced 40 miles away; it has a long way to get to the works.|
|  Works manual is internalised                 |                              Site knowledge GT concept      |        Works manual has been internalised.|

#### External Documents


|  Document                                 |  Version  | Authors                   |    Date|
|  ------------------------------------------| --------- |----------------------------- |------------|
|  Alarm handling GT concept       |       1       |  Shamal Faily  | August 2010|
|  Authorisation restriction GT concept |  1    |     Shamal Faily |  August 2010|
|  big security worry GT concept     |     1    |     Shamal Faily |  August 2010|
|  Business compliance GT concept     |    1    |     Shamal Faily |  August 2010|
|  Corporate interface GT concept     |    1    |     Shamal Faily |  August 2010|
|  External agencies GT concept       |    1    |     Shamal Faily |  August 2010|
|  Hardware checks GT concept         |    1    |     Shamal Faily |  August 2010|
|  Hazards GT concept                 |    1    |     Shamal Faily |  August 2010|
|  ICT non-support GT concept         |    1    |     Shamal Faily |  August 2010|
|  InfoSec communication GT concept   |    1    |     Shamal Faily |  August 2010|
|  InfoSec indifference GT concept    |    1    |     Shamal Faily |  August 2010|
|  Interim Systems GT concept         |    1    |     Shamal Faily |  August 2010|
|  Island mindset GT concept         |     1    |     Shamal Faily |  August 2010|
|  Limited support knowledge GT concept |  1    |     Shamal Faily |  August 2010|
|  Local standards GT concept        |     1    |     Shamal Faily |  August 2010|
|  Logout policy GT concept        |       1    |     Shamal Faily |  August 2010|
|  One-man site GT concept          |      1    |     Shamal Faily |  August 2010|
|  Operational contexts GT concept   |     1    |     Shamal Faily |  August 2010|
|  Personal Security GT concept      |     1    |     Shamal Faily |  August 2010|
|  Process impact GT concept        |      1    |     Shamal Faily |  August 2010|
|  Process Innovation GT concept     |     1    |     Shamal Faily |  August 2010|
|  Sample collection GT concept      |     1    |     Shamal Faily |  August 2010|
|  Scope of responsibility GT concept |    1    |     Shamal Faily |  August 2010|
|  Site knowledge GT concept      |        1    |     Shamal Faily |  August 2010|
|  Site threats GT concept         |       1    |     Shamal Faily |  August 2010|
|  Trend monitoring GT concept      |      1    |     Shamal Faily |  August 2010|
|  Unexplained feature GT concept   |      1    |     Shamal Faily |  August 2010|
|  Unlikely threats GT concept      |      1    |     Shamal Faily |  August 2010|
|  Water GT concept                 |      1    |     Shamal Faily |  August 2010|
|  Work routine GT concept          |      1    |     Shamal Faily |  August 2010|
|  Works diary GT concept           |      1    |     Shamal Faily |  August 2010|

## Further details

[CAIRIS model](https://github.com/failys/cairis/blob/master/examples/personas/Rick/Rick.xml)
