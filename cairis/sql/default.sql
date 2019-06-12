/* 
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
*/

insert into environment(id,name,description,short_code) values(0,'Default','Default environment','DEF');
insert into vulnerability_type(id,name,description) values(0,'Design','A vulnerability inherent in the design or specification of hardware or software whereby even a perfect implementation will result in a vulnerability.');
insert into vulnerability_type(id,name,description) values(1,'Implementation','A vulnerability resulting from an error made in implementing software or hardware of a satisfactory design.');
insert into vulnerability_type(id,name,description) values(2,'Configuration','A vulnerability resulting from an error in the configuration and administration of a system or component.');
insert into threat_type(id,name,description) values(0,'Physical','Physical Security');
insert into threat_type(id,name,description) values(1,'Natural','Environment / Acts of Nature');
insert into threat_type(id,name,description) values(2,'Insider/Manipulation','Sometimes deliberate attempts are made to acquire information or access by manipulating staff by using a range of influencing techniques.  This is sometimes described as social engineering, creating situations in which someone will willingly provide access to information, sites or systems to someone unauthorised to receive it.  Customer facing personnel who have been trained to be helpful and informative can be particularly vulnerable to such attacks.');
insert into threat_type(id,name,description) values(3,'Insider/Sabotage','Saborage is often committed by a former employee seeking revenge on their employer because of a personal grudge caused by a negative work related event such as dismissal.  Although it is sometimes planned well in advance, it can also be the result of an opportunistic moment.');
insert into threat_type(id,name,description) values(4,'Electronic/Malware','Malware is any program or file that is harmful to a computer, the term covers viruses, worms, Trojan horses, and spyware.  Malware is becoming increasingly sophisticated and can be used to compromise computers to install DOS zombie programs or other malicious programs.');
insert into threat_type(id,name,description) values(5,'Electronic/Hacking','Hackers want to get into your computer system and use them for their own purposes.  There are many hacking tools available on the internet as well as online communities actively discussing hacking techniques enabling even unskilled hackers to break into unprotected systems.  Hackers have a range of motives; from showing off their technical prowess, to theft of money, credentials or information, to cause damage.');
insert into threat_type(id,name,description) values(6,'Electronic/DoS and DDoS','A Denial-of-Service (DoS) attack involves a malicious attempt to disrupt the operation of a computer system or network that is connected to the Internet.  A Distributed Denial-of-Service (DDoS) attack is a more dangerous evolution of a DoS attack because it utilises a network of compromised zombie computers to mount the attack, so there is no identifiable single source.');
insert into threat_type(id,name,description) values(7,'Electronic/Keystoke logging','Keystroke loggers work by recording the sequence of key-strokes that a user types in.  The more sophisticated versions use filtering mechanisms to only record highly prized information such as email addresses, passwords and credit card number sequences.');
insert into threat_type(id,name,description) values(8,'Electronic/Phishing and Spoofing',"Phishing describes a social engineering process designed to trick an organisation's customers into imparting confidential information such as passwords, personal data or banking and financial details.  Most commonly these are criminal attacks but the same techniques could be used by others to get sensitive information.");
insert into asset_value(id,name,description,environment_id) values(0,'None','To be defined',0);
insert into asset_value(id,name,description,environment_id) values(1,'Low','To be defined',0);
insert into asset_value(id,name,description,environment_id) values(2,'Medium','To be defined',0);
insert into asset_value(id,name,description,environment_id) values(3,'High','To be defined',0);
