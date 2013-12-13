---
layout: post
title:  Pretty fonts in Debian. Give up now. Seriously.
date:   2013-12-12 00:00:01
categories: general
coverimage: /img/covers/rage.png
---

Just spent 4 hours trying to get pretty fonts working in Debian, so they look like they do in Ubuntu. After reading through endless threads/discussions, and wasting 4 hours with font config, it turns out that Ubuntu have patched a few libraries (at least libcario, libxlt) to make their font rendering look pretty, patches which sadly are not included in Debian at this stage.

### Ubuntu
[![access-virus-3.png](/img/postcontent/fonts2.png)](/img/postcontent/fonts2.png)

### Debian
[![access-virus-3.png](/img/postcontent/fonts1.png)](/img/postcontent/fonts1.png)

Someone released a [custom repo][1] with the patches included, but this has since gone offline. This can now only be achieved by doing a custom package compile of the various patched libraries, not a small task.

If you want a good Linux desktop with pretty fonts then stick with Ubuntu.

Here are some other threads discussing this;

* http://www.techytalk.info/font-smoothing-in-debian-6-0-squeeze-like-in-ubuntu/
* [http://forums.debian.net/viewtopic.php?f=10&t=78662](http://forums.debian.net/viewtopic.php?f=10&t=78662)
* [http://forums.debian.net/viewtopic.php?f=6&t=81177](http://forums.debian.net/viewtopic.php?f=6&t=81177)
* [http://forums.debian.net/viewtopic.php?f=6&t=71333](http://forums.debian.net/viewtopic.php?f=6&t=71333)
* [http://forums.debian.net/viewtopic.php?f=6&t=46550](http://forums.debian.net/viewtopic.php?f=6&t=46550)
* [http://forums.debian.net/viewtopic.php?f=6&t=77868](http://forums.debian.net/viewtopic.php?f=6&t=77868)
* [http://forums.debian.net/viewtopic.php?f=6&t=50742](http://forums.debian.net/viewtopic.php?f=6&t=50742)
* [http://forums.debian.net/viewtopic.php?f=6&t=96808](http://forums.debian.net/viewtopic.php?f=6&t=96808)
* [http://forums.debian.net/viewtopic.php?f=6&t=58173](http://forums.debian.net/viewtopic.php?f=6&t=58173)
* [http://forums.debian.net/viewtopic.php?f=10&t=59728](http://forums.debian.net/viewtopic.php?f=10&t=59728)
* [http://forums.debian.net/viewtopic.php?f=3&t=55536](http://forums.debian.net/viewtopic.php?f=3&t=55536)
* [http://forums.debian.net/viewtopic.php?f=6&t=52610](http://forums.debian.net/viewtopic.php?f=6&t=52610)
* [http://forums.debian.net/viewtopic.php?f=6&t=103175](http://forums.debian.net/viewtopic.php?f=6&t=103175)

 [1]: http://www.techytalk.info/font-smoothing-in-debian-6-0-squeeze-like-in-ubuntu/
