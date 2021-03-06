---
layout: post
title:  LXC containers are awesome, but Docker.io sucks
date:   2013-11-05 00:00:00
categories: general
coverimage: /img/covers/sun-disappoint-pony.jpg
weight: 17
keywords: docker, docker.io, lxc, aufs, containers, ubuntu
desc: Docker is not the right answer
---

I have been using LXCs since early 2009 and have long argued this application containers should be adopted. Separating application run time is critical not just for security, but for sanity as well. Under most conditions, excluding any event which results in host contamination, for example kernel exploits, you can assume the host machine will still be clean even after running a guest container. 

Resource limiting also means you can access the box during periods of saturated IO/CPU without having to reboot, this is crucial for live on-the-fly debugging and memory capture. It also prevents mistakes in package configuration from destroying the host machine, for example an apt dependency on a package which then breaks libc6 for ssh. It also means you can test close to the environment running in production, though you cannot avoid differences in your host hardware, kernel or distro.

[Docker][8] sells itself as a tool allowing creation of lightweight, portable, self-sufficient application containers. The concept is fundamentally correct, but has sadly been poorly implemented in Docker.

Alex Hudson wrote an [interesting article][4] and appears to have come to similar conclusions about Docker, they took the correct design decision to use LXCs, but everything else is lacking.

Here are my initial thoughts;

* AuFS is not a good choice of FS. It requires [kernel patches][1] and it still suffers from [problems][2]. Although I'm not a huge fan of [stacked file systems][3], OverlayFS might have been a better choice.
* CLI/API abstraction is non intuitive.
* Documentation quality is poor.
* Network redirection implementation is not clear, the docs say that [iptables is used][6], but commit log [suggests otherwise][7]
* Lack of maturity. Docker has only been here for [less than a year][5]
* Written in Go, which in itself lacks maturity, and reduces the number of volunteers able to contribute
* Suffers with some quite nasty bugs in [initscript][9], [upstart][10] and [apt-get][11].
* It monkey patches `/sbin/init`, this is particularly evil and [causes problems][11]
* Private image storage is [unnecessarily complex][12]

For some of you, Docker might be the best step forward especially if you do not have the in-house skills to create your own application container stack. But for those who have the time/skill set, I would highly recommend rolling your own instead. It could be argued that rolling your own stack would have even less maturity, but I think the benefits outweight that if you can afford it.

For those choosing Docker because of their hosted PAAS platform - think again. PAAS pricing inflation is ridiculously high at the moment, running 5 instances with 1GB will cost you nearly $1000/month, so a unique skill set is still required to build and maintain these container systems even if you roll your own or not.

To summerize, Docker is no where near production ready and even when it is, I still won't be using it. However I have to give credit to them for raising awareness about LXCs. The concept of containers are awesome, it's just a shame Docker implemented it in a poor way.

 [1]: http://docs.docker.io/en/latest/installation/kernel/#id2
 [2]: http://bkhome.org/blog/?viewDetailed=01449
 [3]: http://www.thegeekstuff.com/2013/05/linux-aufs/
 [4]: http://www.alexhudson.com/2013/05/28/a-first-look-at-docker-io/
 [5]: http://en.wikipedia.org/wiki/Docker_(Linux_container_engine)
 [6]: http://blog.docker.io/2013/03/docker-containers-can-haz-networking-now/
 [7]: https://github.com/dotcloud/docker/commit/fac0d87d00ada08309ea3b82cae69beeef637c89
 [8]: http://docker.io/
 [9]: https://github.com/dotcloud/docker/issues/1024
 [10]: https://github.com/dotcloud/docker/issues/2276
 [11]: https://github.com/dotcloud/docker/issues/1724
 [12]: http://docs.docker.io/en/latest/use/workingwithrepository/
