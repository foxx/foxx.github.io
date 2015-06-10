---
layout: post
title:  Code review of AutobahnJS / crossbar.io
date:   2014-12-30 00:00:00
categories: general
coverimage: /img/covers/repairguy.jpg
type: small
weight: 19
keywords: crossbar, crossbar.io, js, websockets, wamp, javascript
desc: Code review of crossbar.io
---


### Summary

There has already been a comprehensive review of what [crossbar.io](http://crossbar.io/) has to offer [here](http://tavendo.com/blog/post/is-crossbar-the-future-of-python-web-apps/), which is worth reading before making any decision.

In short, crossbar.io aims to provide an end-to-end framework which takes advantages of websockets to implement [WAMP](http://wamp.ws/), allowing you to handle/trigger events without polling. It works on top of Web Sockets implemented by Autobahn.

Firstly, this is a fantastic concept, and I must applaud the authors for thier work. Much like my review of SwampDragon, anything which helps raise awareness about why [SPAs](http://en.wikipedia.org/wiki/Single-page_application) are awesome is a good thing, and the autobahn test suite has proved very useful to the community.

However this is where the positives stop, and upon reviewing their code I have serious concerns. My limit for this review is two hours, sadly this was not enough to address every concern, but it was enough to make a comprehensive decision to say no.

I would urge all readers to review the code/specifications, and come to your own conclusion. There was also a [discussion](https://groups.google.com/forum/#!msg/autobahnws/EMKF4a0aXKI/uy7cg9DvqLYJ) with the authors regarding this article, prior to its release.

### Crossbar demo

There is a fancy colorpicker [demo](https://demo.crossbar.io/demo/colorpicker/index.html) which syncronises the selected color upon change. However the [example code](https://github.com/crossbario/crossbardemo/blob/master/crossbardemo/crossbardemo/web/demo/colorpicker/js/colorpicker.js) isn't very clean and doesn't appear to implement any proper [JS design patterns](http://addyosmani.com/resources/essentialjsdesignpatterns/book/).

The performance was snappy with quite a high FPS, but it resulted in a 45% CPU utilization on my 3ghz i7 with light usage and 60% if I dragged around furiously, which is unacceptably high and would only become worse with additional DOM manipulation.

### Python server code

The underlying WAMP implementation is done using [autobahn](http://autobahn.ws/), also made by the same authors, and uses websockets for communication. Based on their Python [examples](http://autobahn.ws/python/), which can be used with both Twisted and asyncio.

Initial docs inspection worries me, their [getting started](http://crossbar.io/docs/Getting-started-with-Python/) docs appears to show a blob of JSON which is presumably used to configure the application, though I don't see any documentation on what each attribute does. There is also a section on "hacking code" just underneath, which doesn't give any explanation on what it does and why it would be necessary.

Code inspection gets even worse, their repo is immediately untidy from the outset with an older version of the code rotting away in a folder called [v1](httfps://github.com/crossbario/crossbar/tree/master/v1). Makefile seems to contain several commands with no explanation on what each one does, and some rather strange attribute names such as `cbdir`. In some cases, paths have been hard coded to a developers local setup [Makefile#L70](https://github.com/crossbario/crossbar/tree/v0.9.12/crossbar/Makefile#L70). Most files have the same license text [unnecessarily](http://stackoverflow.com/questions/845895/putting-license-in-each-code-file) repeated at the top, in some cases this is the only text in the file [postgres/__init__.py](https://github.com/crossbario/crossbar/tree/v0.9.12/crossbar/crossbar/adapter/postgres/__init__.py).

Some parts of the code have a good amount of class documentation [publisher.py#L39](https://github.com/crossbario/crossbar/tree/v0.9.12/crossbar/crossbar/adapter/postgres/publisher.py#L39), but the majority does not [guest.py#L123](https://github.com/crossbario/crossbar/blob/master/crossbar/crossbar/controller/guest.py#L123). Many sections have nested conditionals which look particularly ugly [publisher.py#L93](https://github.com/crossbario/crossbar/blob/master/crossbar/crossbar/adapter/postgres/publisher.py#L93), and this seems to be repeated throughout the code [broker.py#L170](https://github.com/crossbario/crossbar/blob/v0.9.12/crossbar/crossbar/router/broker.py#L170).

Many of the PEP8 guidelines have not been followed, such as line length [broker.py#L214](https://github.com/crossbario/crossbar/blob/v0.9.12/crossbar/crossbar/router/broker.py#L214), and there doesn't appear to be any lint checks. There is a lot of unnecessary whitespace [broker.py#L201](https://github.com/crossbario/crossbar/blob/v0.9.12/crossbar/crossbar/router/broker.py#L201), as well as inconsistent and unpythonic naming convention [broker.py#L220](https://github.com/crossbario/crossbar/blob/v0.9.12/crossbar/crossbar/router/broker.py#L220) and [broker.py#L292](https://github.com/crossbario/crossbar/blob/v0.9.12/crossbar/crossbar/router/broker.py#L292).

### JS client code

WAMP is implemented using [AutobahnJS](https://github.com/tavendo/AutobahnJS). This uses [when.js](https://github.com/cujojs/when) to implement Promises/A+, and taken design inspiration from [ws](https://github.com/einaros/ws), [cujoJS](http://cujojs.com/) and [Reactive Manifesto](http://www.reactivemanifesto.org/). The JS client is compiled using [Browserify](http://browserify.org/), and seems to follow a [RequireJS](http://requirejs.org/) style.

Code review paints an ugly picture. The source is a whopping 244kB after compile, in some places there good amounts of inline commenting [connection.js#L112](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/connection.js#L112) and in others it is completely lacking [connection.js#L163](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/connection.js#L163). Constant arrays also don't have any documentation [session.js#L150](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L150). Inline comments follow a strange style which includes an empty `//` after each comment, and this style is repeated through most of the code [session.js#L28](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L28).

Logging doesn't appear to be implemented properly, rather it looks for a global variable then sends it all to console.log [log.js#L17](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/log.js#L17). Throughout the code there is consistent global namespace abuse [session.js#L898](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L898).

Fallback browser hacks have been added in at random points throughout the code, rather than kept in a single place, for example `Date.now` [session.js#L24](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L24).

Object member names do not seem to follow a consistent naming convention. For example, an underscore would [typically](http://stackoverflow.com/questions/4484424/underscore-prefix-for-property-and-method-names-in-javascript) denote whether a member is part of public API, however the same common member name `id` can be seen both without on `Subscription.id` [session.js#L108](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L108) and with on `Session._id` [session.js#L194](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L194). There is also mixed uppercase and underscore seperators [session.js#L243](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L243), in this example this is because the original event name is in upper case, but a simple `lower()` could have made this much prettier.

Object instances are created manually [session.js#L262](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L262), there does not appear to be any sort of object factory. These objects are also created using positional arguments, rather than passing in another object to emulate named arguments [session.js#L262](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L262). Some places appear to have factories, but the approach used is by no means good. For example, in [connection.js#L162](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/connection.js#L162) object instanciation exceptions being caught and logged to console, but no event triggered or exception raised.

Max line lengths have not been adhered to [session.js#L417](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L417), and messages are hard coded rather than using a locales table [session.js#L827](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L827). There is quite a bit of unnecessary whitespace [session.js#L788](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L788) and superfluous crlf [session.js#L888](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L888).

Their logic approach and object construction is also a bit strange, for example `Session` socket errors by handled by calling `self._protocol_violation`, which in turn executes `self._socket.close()` rather than returning a response object. [session.js#L234](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L234)

Object documentation does not seem to follow [jsdoc](https://github.com/jsdoc3/jsdoc) or [yuidoc](http://yui.github.io/yuidoc/) specifications [session.js#L673](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L673), and would almost certainly not work in a doc generator. String formatting has been implemented using operators rather than [sprintf](https://www.npmjs.com/package/sprintf-js), and in some cases, mixing operators without any parenthasis [session.js#L980](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L980).

Some sections have good assertion checks [session.js#L1004](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L1004), but the majority does not [session.js#L182](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L182). 
At some points it's quite difficult to understand what code is being used for [session.js#L1343](https://github.com/tavendo/AutobahnJS/blob/v0.9.5/package/lib/session.js#L1343).

### WAMP specification

[WAMP](http://wamp.ws/) aims to be a sub-protocol that sits on top of WS, and provides a unified protocol for RPC and Pub/Sub.

After reading through [WAMP v2](https://github.com/tavendo/WAMP/blob/master/spec/advanced.md), which admittedly is still in beta, I'm left with the impression that it is an over-engineered solution to a very simple problem, which when coupled with lacking maturity and stability, makes it a dangerous candidate for production.

The specification makes for difficult reading, in some ways it reminds me of RFC 3261 (SIP). Some places have nested JSON encoded as a string (wtf?), and throughout the spec there is type hinting appended to message definition keys (|string, |bool etc). There has also been minimal external input and peer review, the majority of the spec has been written by one person and less than a handful of people had any deep involvement on the group mailing list throughout its conception.

Furthermore, WAMP is a trademark which belongs to the company who has sponsored its development, and many of the Autobahn WAMP family use differing licenses, Apache/MIT etc.

### Conclusion

Both AutobahnJS and crossbar.io are let down by poor architectural design, bad code quality, excessive [SLOC](http://en.wikipedia.org/wiki/Source_lines_of_code) and unclear documentation. They are both written in ES5, rather than the far superior ES6, and have clearly not followed TDD.

Autobahn Python is a better story, it now has asyncio support and the WS implementation seems mostly clean, despite not being PEP8 compliant or passing lint checks. However as it's a pure-python implementation there will have performance limitations, and it is tightly bound with WAMP.

On the grounds of poor code and architectual design quality, I would choose not to use crossbar.io, Autobahn or the WAMP specification for any of my work. Admittedly the Autobahn WAMP family has wide cross language support and would allow for rapid prototyping, but the WAMP specification as a whole feels unviable. This doesn't mean *you* shouldn't use it, but you should at least be aware of the dragons.
