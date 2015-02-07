---
layout: post
title:  Lets review.. Docker (again)
date:   2015-01-17 00:00:00
categories: general
coverimage: /img/covers/pewdiepie1.jpg
type: small
weight: 20
keywords: docker, namespaces, containers, linux, lxc
desc: Many reasons why you should stop using Docker
---

### Summary

It's been just over a year since my last [review][55] of Docker, heavily criticising it's flawed architectural design and poor user experience. The project has since matured into [1.0][1] and gained some [notoriety][4] from Amazon, but has suffered growing user frustration, [hype][3] accusations and even breakout [exploits][1] leading to host contamination. However the introduction of private repos in [Docker Hub][5], which eliminated the need to run your own registry for hosted deployments, coupled with webhooks and tight Github build [integrations][6], looked to be a promising start.

So I decided to give Docker another chance and put it into production for 6 months. The result was an absolute shit show of abysmal performance, hacky workarounds and rage inducing user experience which left me wanting to smash my face into the desk. Indeed performance was so bad, that disabling caching features actually resulted in faster build times. 

If you expect anything positive from Docker, or its maintainers, then you're shit outta luck.


### Dockerfile

Dockerfile has numerous problems, it's ugly, restrictive, contradictory and fundamentally flawed. Lets say you want to build multiple images of a single repo, for example a second image which contains debugging tools, but both using the same base requirements. Docker does not support this (per [#9198][8]), there is no ability to extend a Dockerfile (per [#735][7]), using sub directories will break build context and prevent you using ADD/COPY (per [#2224][9]), as would piping (per [#2112][10]), and you cannot use env vars at build time to conditionally change instructions (per [#2637][11]).

Our hacky [workaround][53] was to create a base image, two environment specific images and some Makefile automation which involved renaming and sed replacement. There are also some unexpected "[features][54]" which lead to env `$HOME` disappearing, resulting in unhelpful error messages. Absolutely disgusting.


### Docker cache/layers

Docker has the ability to [cache][12] Dockerfile instructions by using COW (copy-on-write) filesystems, similar to that of LVM [snapshots][50], and until recently only supported AuFS, which has numerous problems. Then in release [0.7][13] different COW implementations were introduced to improve stability and performance, which you can read about in detail [here][14].

However this caching system is unintelligent, resulting in some surprising [side effects][15] with no ability to prevent a single instruction from caching (per [#1996][16]). It's also painfully slow, to the point that builds will be faster if you disable caching and avoid using layers. This is exacerbated by slow download performance in Docker Hub, detailed further down, causing images to be uploaded/downloaded very slowly. 

These problems are caused by the poor architectural design of Docker as a whole, enforcing linear instruction execution even in situations where it is entirely inappropriate (per [#2439][17]). As a workaround for slow builds, you can use a third party tool which supports asynchronous execution, such as [Salt Stack][18], [Puppet][19] or even [bash][20], completely defeating the purpose of layers and making them useless.


### Docker Hub

Docker encourages social collaboration via Docker Hub which allows Dockerfiles to be published, both public and private, which can later be extended and used by other users via [FROM][24] instruction, rather than copy/pasting. However this is flawed for several reasons. Dockerfile does not support multiple FROM instructions (per [#3378][21], [#5714][22] and [#5726][23]), meaning you can only inherit from a single image. It also has no version enforcement, for example the author of `dockerfile/ubuntu:14.04` could replace the contents of that tag, which is the equivalent of using a package manager without enforcing versions. And as mentioned later in the article, it has frustratingly slow speed restrictions.

Docker Hub also has an automated build system which detects new commits in your repository and triggers a container build. It is also completely useless for many reasons. Build configuration is restrictive with little to no ability for customisation, missing even the basics of pre/post script hooks. It enforces a specific project structure, expecting a single Dockerfile in the project root, which breaks our previously mentioned build workarounds, and build times were horribly slow.

Our workaround was to use [CircleCI][25], an exceptional hosted CI platform, which triggered Docker builds from Makefile and pushed up to Docker Hub. This did not solve the problem of slow speeds, but the only alternative was to use our own Docker Registry, which is ridiculously [complex][26].


### Security

Docker originally used LXC as their default execution environment, but now use their libcontainer by default as of [0.9][35]. This introduced the ability to [tweak][27] namespace capabilities, privileges and, use customised LXC [configs][28] when using the appropriate exec-driver.

It requires a root daemon be running at all times on the host, and there have been [numerous][30] security vulnerabilities in Docker, for example [CVE-2014-6407][31] and [CVE-2014-6408][32] which, quite frankly, should not have existed in the first place. Even Gartner, with their [track record][33] for poor assessments, expressed [concern][34] over the immaturity of Docker and the security implications.

Docker, by design, puts ultimate trust in namespace [capabilities][29] which expose a much larger attack surface than a typical hypervisor, with Xen having [129][36] CVEs in comparison with the [1279][37] in Linux. This can be acceptable in some situations, for example public builds in Travis CI, but are dangerous in private, multi user environments.


### Containers are not VMs

Namespaces and cgroups are beautifully [powerful][49], allowing a process and its children to have a private view of shared kernel resources, such as the network stack and process table. This fine-grain control and segregation, coupled with chroot jailing and [grsec][39], can provide an excellent layer of protection. Some applications, for example [uWSGI][38], take direct advantage of these features without Docker, and applications which don't support namespaces directly can be sandboxed using [firejail][48].

Containerisation projects, such as LXC and Docker, take advantage of these features to effectively run multiple distros inside the same kernel space. In [comparison][46] with hypervisors, this can sometimes have the [advantage][45] of lower memory usage and faster startup times, but at the cost of reduced security, stability and compatibility. One horrible [edge case][42] relates to [Linux Kernel Interfaces][41], running incompatible or untested combinations of glibc versions in kernel and userspace, resulting in unexpected behavior.

Back in 2008 when LXC was conceived, hardware assisted virtualisation had only been around for a couple of years, many hypervisors has performance and stability issues, as such virtualisation was not a widely used technology and these were acceptable tradeoffs to keep costs low and reduce physical footprint. However we have now reached the point where hypervisor performance is almost as fast as bare metal and, interesting, faster in some [cases][43]. Hosted on-demand VMs are also becoming faster and cheaper, with [DigitalOcean][44] massively [outperforming][51] EC2 in both performance and cost, making it financially viable to have a 1:1 mapping of applications to VMs.

There are some specific use cases in which containerisation is the correct approach, but unless you can explain precisely why in your use case, then you should probably be using a hypervisor instead. Even if you're using virtualisation you should still be taking advantage of namespaces, and tools such as [firejail][47] can help when your application lacks native support for these features.

### Docker is unnecessary

Docker adds an intrusive layer of complexity which makes development, troubleshooting and debugging frustratingly difficult, often creating more problems than it solves. It doesn't have any benefits over deployment, because you still need to utilise snapshots to achieve responsive auto scaling. Even worse, if you're not using snapshots then your production environment scaling is dependant on the stability of Docker Hub. 

It is already being abused by projects such as [baseimage-docker](https://github.com/phusion/baseimage-docker), an image which intends to make inspection, debugging and compatibility easier by running init.d as its entry point and even giving you an optional SSH server, effectively treating the container like a VM, although the authors reject this notion with a poor [argument][52].

### Conclusion

If you're development workflow is sane, then you will already understand that Docker is unnecessary. All of the features which it claims to be helpful are either useless or poorly implemented, and it's primary benefits can be easily achieved using namespaces directly. Docker would have been a cute idea 8 years ago, but it's pretty much useless today.


* Credits to [CYPHERDEN][56] for the cover image, taken from [PewDiePie][57]

[1]: http://blog.docker.com/2014/06/docker-container-breakout-proof-of-concept-exploit/
[2]: http://www.theregister.co.uk/2014/06/09/docker_milestone_release/
[3]: http://www.krisbuytaert.be/blog/docker-vs-reality-0-1
[4]: http://www.theregister.co.uk/2014/11/15/amazon_ec2_container_service_deep_dive/
[5]: https://docs.docker.com/userguide/dockerhub/
[6]: http://docs.docker.com/docker-hub/builds/
[7]: https://github.com/docker/docker/issues/735
[8]: https://github.com/docker/docker/issues/9198
[9]: https://github.com/docker/docker/issues/2224
[10]: https://github.com/docker/docker/issues/2112
[11]: https://github.com/docker/docker/issues/2637
[12]: http://thenewstack.io/understanding-the-docker-cache-for-faster-builds/
[13]: http://blog.docker.com/2013/11/docker-0-7-docker-now-runs-on-any-linux-distribution/
[14]: http://developerblog.redhat.com/2014/09/30/overview-storage-scalability-docker/
[15]: http://kimh.github.io/blog/en/docker/gotchas-in-writing-dockerfile-en/#build_caching_what_invalids_cache_and_not
[16]: https://github.com/docker/docker/issues/1996
[17]: https://github.com/docker/docker/issues/2439
[18]: http://blog.xebia.com/2014/06/14/combining-salt-with-docker/
[19]: http://puppetlabs.com/blog/building-puppet-based-applications-inside-docker
[20]: https://github.com/fideloper/Vaprobash
[21]: https://github.com/docker/docker/issues/3378
[22]: https://github.com/docker/docker/issues/5714
[23]: https://github.com/docker/docker/issues/5726
[24]: https://docs.docker.com/reference/builder/#from
[25]: https://circleci.com/
[26]: https://github.com/docker/docker-registry
[27]: https://docs.docker.com/reference/run/#runtime-privilege-linux-capabilities-and-lxc-configuration
[28]: https://www.stgraber.org/2014/01/17/lxc-1-0-unprivileged-containers/
[29]: https://docs.docker.com/articles/security/
[30]: http://www.theregister.co.uk/2014/11/25/docker_vulnerabilities/
[31]: http://www.securityfocus.com/bid/71315
[32]: http://www.securityfocus.com/bid/71518
[33]: http://www.zdnet.com/article/why-does-the-it-industry-continue-to-listen-to-gartner/
[34]: http://www.theregister.co.uk/2015/01/12/docker_security_immature_but_not_scary_says_gartner/
[35]: http://www.infoq.com/news/2014/03/docker_0_9
[36]: http://www.cvedetails.com/vendor/6276/XEN.html
[37]: http://www.cvedetails.com/vendor/33/Linux.html
[38]: http://uwsgi-docs.readthedocs.org/en/latest/Namespaces.html
[39]: https://grsecurity.net/
[40]: https://linuxcontainers.org/
[41]: http://en.wikipedia.org/wiki/Linux_kernel_interfaces
[42]: http://stackoverflow.com/questions/27171485/various-glibc-and-linux-kernel-versions-compatibility
[43]: https://major.io/2014/06/22/performance-benchmarks-kvm-vs-xen/
[44]: https://www.digitalocean.com/pricing/
[45]: http://www.theregister.co.uk/2014/05/02/docker_hadoop/
[46]: http://marceloneves.org/papers/pdp2013-containers.pdf
[47]: https://l3net.wordpress.com/projects/firejail/
[48]: http://man7.org/linux/man-pages/man7/capabilities.7.html
[49]: http://www.toptal.com/linux/separation-anxiety-isolating-your-system-with-linux-namespaces
[50]: http://serverfault.com/questions/41020/is-this-how-lvm-snapshots-work
[51]: http://uncrunched.com/2013/08/07/digital-ocean-v-aws-10x-performance-for-13-cost/
[52]: https://github.com/phusion/baseimage-docker#fat_containers
[53]: https://gist.github.com/foxx/0305f9f7ebe65b246c6c
[54]: https://gist.github.com/foxx/0c4f02de6e3906fa1c98
[55]: http://iops.io/blog/lxc-application-containers-docker-initial-thoughts/
[56]: https://www.youtube.com/channel/UCOwxx9VnEnlFKt5EB70KTzQ
[57]: https://www.youtube.com/watch?v=LWCUMLEbQ00