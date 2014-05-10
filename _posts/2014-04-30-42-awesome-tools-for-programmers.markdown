---
layout: post
title:  42 awesome tools for programmers
date:   2014-05-01 00:00:00
categories: general
coverimage: /img/covers/requires-professional.jpg
type: small
weight: 18
---

Over the years I've tweaked and perfected my workflow to be [KISS](http://en.wikipedia.org/wiki/KISS_principle) and [DRY](http://en.wikipedia.org/wiki/Don't_repeat_yourself). Here is a collection of tools that you may not even know exist, and could help improve your workflow. (in no particular order)

### 1. uWSGI

[http://uwsgi-docs.readthedocs.org/en/latest/](http://uwsgi-docs.readthedocs.org/en/latest/)

Application server that works with Python and a multitude of other languages. Roberto really has done a fantastic job with this software.


### 2. virtualenvwrapper

[http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/)

Handy tools for managing your python virtualenv's, makes life a lot easier.

### 3. NodeENV

[https://github.com/ekalinin/nodeenv](https://github.com/ekalinin/nodeenv)

Virtual environments for Node JS which work alongside virtualenvwrapper

### 4. New Relic APM

[http://newrelic.com/](http://newrelic.com/application-monitoring)

Code level application monitoring for web applications. This is an invaluable tool for getting insight and profiling into applications running in production.

### 5. SASS

[http://sass-lang.com/guide](http://sass-lang.com/guide)

SASS makes writing CSS fun! Stop writing CSS by hand, seriously.

### 6. Bourbon Neat

[http://neat.bourbon.io/](http://neat.bourbon.io/)

Looking for a bit more control over your CSS structure and styling? Put down [Bootstrap](http://getbootstrap.com/css/), and give Neat a try!

### 7. Get Sentry

[https://getsentry.com/](https://getsentry.com/)

Need an easy way to collect errors from your production deployment? Sentry offers both hosted and non-hosted application logging for many different frameworks and languages. It's better than New Relic's error collector.

### 8. Trello

[http://trello.com](http://trello.com)

Tired of using complex ticketing systems for your projects? Fed up with the usability overhead of JIRA etc? Trello is a great card based alternative for managing your tasks, and comes with full markdown support.

### 9. Github

[https://github.com](https://github.com)

Github allows for better collaboration, code review, and code management for open source and private projects. This service has really made a difference to the world of open source.

### 10. Runscope Traffic Inspector

[https://www.runscope.com/docs/inspector](https://www.runscope.com/docs/inspector)

Capture and inspect your API requests easily and efficiently, this tool has saved my ass a few times!

### 11. PagerDuty

[https://www.pagerduty.com/](https://www.pagerduty.com/)

Receives alarms from almost any source, and sends you a text or a phone call with the alarm details.

### 12. Zapier

[https://zapier.com/](https://zapier.com/)

Connects APIs from 100s of cloud services, and allows you to create triggers between them. For example, if New Relic sends an event, you can trigger a message on Hipchat. This is great for integrating services that don't have direct integration available.

### 13. Hipchat

[https://www.hipchat.com/](https://www.hipchat.com/)

HipChat is a nice corporate chat application with some cool features such as media previewing in the desktop application. However it's slowly getting worse, and would strongly consider moving back to IRC.

### 14. Travis CI 

[https://travis-ci.org/](https://travis-ci.org/)

Hosted CI (Continuous Integration) service for automated testing of your projects.

### 15. Stripe

[https://stripe.com/](https://stripe.com/)

If you have a business model that requires low risk payments, then Stripe is the one for you. Start accepting credit card payments for minimal fees and without PCI DSS (thanks to their brilliant Stripe JS library).

### 15. Percona MySQL

[http://www.percona.com/](http://www.percona.com/)

Percona are dragging MySQL by its feet, kicking and screaming, into the 21st century (quoted from a colleague). Although the future of MySQL is looking bleak, Percona is a must for anyone that hasn't switched to [MariaDB](http://vimeo.com/56639635) yet.

Also have a look at the [PTK (Percona Toolkit)](http://www.percona.com/software/percona-toolkit), some scary but very handy DBA tools.

### 16. Redis

[http://redis.io/](http://redis.io/)

Redis is an advanced, multi-purpose key-value store. It even has pub/sub support, and is a great alternative to [dead rabbit](https://www.rabbitmq.com/). Redis stays fresh and alive thanks to the amazing work from [Salvatore (antirez)](http://antirez.com/latest/0).

### 17. Salt Stack

[http://www.saltstack.com/](http://www.saltstack.com/)

Lets face it, Chef and Puppet really suck. Salt is a great alternative for those who want hassle free devops automation.

### 18. Zencoder

[http://zencoder.com/](http://zencoder.com/)

Cloud service for video rendering, clean documentation and almost faultless service. It's a bit pricey but still beats doing it yourself.

### 19. django-pipeline

[https://github.com/cyberdelia/django-pipeline](https://github.com/cyberdelia/django-pipeline)

Asset pipeline for Django, compiles CSS/SASS/JS etc.

### 20. python-requests

[http://docs.python-requests.org/en/latest/](http://docs.python-requests.org/en/latest/)

Beautiful and simple library for performing HTTP requests. If you're still using `urllib`, take a look at [this comparison](https://gist.github.com/kennethreitz/973705).

### 21. django-devserver

[https://github.com/dcramer/django-devserver](https://github.com/dcramer/django-devserver)

Drop in replacement for Django's built-in runserver command.

### 22. eventlet

[http://eventlet.net/](http://eventlet.net/)

Green threading library for Python

### 23. PYQuery

[https://pypi.python.org/pypi/pyquery](https://pypi.python.org/pypi/pyquery)

jQuery style HTML/XML scraping, much nicer than BeautifulSoup

### 24. Boxcryptor

[https://www.boxcryptor.com/](https://www.boxcryptor.com/)

If you're a cloud storage user with any of the big names (Dropbox etc), you really should check this out. Boxcryptor offers architecturally secure cloud encryption for an extra layer of security. Nothing is ever safe, but this is another great deterrent for pretending data theft.

### 25. RegexBuddy

[http://www.regexbuddy.com/](http://www.regexbuddy.com/)

Handy desktop application (Windows only) for testing regex (regular expressions) with zero fuss.

### 26. SourceTree

[http://www.sourcetreeapp.com/](http://www.sourcetreeapp.com/)

Although lacking in some areas, SourceTree is a neat GUI for managing your GIT repo.

### 27. MongoVUE

[http://www.mongovue.com/](http://www.mongovue.com/)

Desktop application (windows only) for MongoDB managemnet

### 28. Navicat

[http://www.navicat.com/](http://www.navicat.com/)

GUI administration and development application for [MySQL](http://www.percona.com/software/percona-server), (MariaDB)[https://mariadb.org/] and several others.

### 29. VMware Workstation

[http://www.vmware.com/uk/products/workstation](http://www.vmware.com/uk/products/workstation)

Are you still running your code on your local host machine? Stop that! Workstation might be a bit expensive, but it beats [VirtualBox](https://www.virtualbox.org/) hands down.

### 30. KeePass

[http://keepass.info/](http://keepass.info/)

Password management tool for almost every platform. Not perfect if you're looking for complete integration, but it suits my needs perfectly.

### 31. 99U

[http://99u.com/](http://99u.com/)

One of the less spammy newsletters out there, with a weekly update of interesting topics.

### 32. Khan Academy

[https://www.khanacademy.org/cs](https://www.khanacademy.org/cs)

Absolutely insane amount of quality learning material available completely free for anyone.

### 33. TED

[https://www.ted.com/](https://www.ted.com/)

TED offers a collection of insightful and inspiring talks from some of the worlds brightest people.


### 34. HATEOAS

Are you designing an API? You should really keep HATEOAS principle in mind.

* [http://spring.io/understanding/HATEOAS](http://spring.io/understanding/HATEOAS)
* [http://en.wikipedia.org/wiki/HATEOAS](http://en.wikipedia.org/wiki/HATEOAS)
* [http://www.slideshare.net/trilancer/why-hateoas-1547275](http://www.slideshare.net/trilancer/why-hateoas-1547275)
* [http://www.slideshare.net/XEmacs/representational-state-transfer-rest-and-hateoas](http://www.slideshare.net/XEmacs/representational-state-transfer-rest-and-hateoas)
* [http://stackoverflow.com/questions/20335967](http://stackoverflow.com/questions/20335967)
* [http://programmers.stackexchange.com/questions/235872](http://programmers.stackexchange.com/questions/235872)

### 35. Deferred and promises

Deferred [constructs](http://en.wikipedia.org/wiki/Futures_and_promises) are a beautiful design approach for concurrent programming.

There are several language specific implementations of promises and deferred, such as [AS3 Promises](https://github.com/CodeCatalyst/promise-as3/) and [JQuery Deferred](http://api.jquery.com/category/deferred-object/). There's also a great article by [Chris Webb](http://blog.mediumequalsmessage.com/promise-deferred-objects-in-javascript-pt2-practical-use).



### 36. Sandboxie

[http://www.sandboxie.com/](http://www.sandboxie.com/)

Although it doesn't give the same protections of a full hypervisor, Sandboxie helps prevent every day nasties from doing too much damage. It also runs suprisingly seemlessly with little to no conflict, and lets you do things like allowing Chrome bookmarks to persist, but everything else to be sandboxed. Plugins can run inside or outside the sandbox, such as download managers. Quite a neat little tool, not just for security, but for OS hygiene too!

### 37. Sublime Text 2 with SpaceFunk/FutureFunk

[http://www.sublimetext.com/2](http://www.sublimetext.com/2)

This text editor changed my life, seriously. And it looks beautiful with [SpaceFunk Grey Tuesday](https://github.com/Twiebie/ST-Spacefunk) theme and [Future Funk](https://github.com/Twiebie/ST-FutureFunk) color scheme.
