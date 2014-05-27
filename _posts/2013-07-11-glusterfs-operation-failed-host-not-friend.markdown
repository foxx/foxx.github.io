---
layout: post
title:  GlusterFS operation failed, host not a friend
date:   2013-07-11 00:00:00
categories: general
coverimage: /img/covers/lol-seahorse.jpg
weight: 12
keywords: glusterfs, ubuntu
desc: GlusterFS operation failed, this is how to fix it
---

GlusterFS is a lovely piece of technology, but it is bitchy as hell. If you stumbled across this thread, it's because GlusterFS is giving you problems, no one seems to explain why and the CLI is about as useful as a third leg. Please note, this post relates to GlusterFS 3.2.7, and most of these problems are fixed in 3.3.

### Hostname problems

You must make sure your local hostname is pointing towards 127.0.0.1, otherwise you will end up with. You must also make sure each glusterfs hostname is aliased in /etc/hosts.

If you don't do this, you'll end up with;

{% highlight text %}
root@test1$ gluster volume create gv1 replica 2 transport tcp test1:/glusterfs/brick test2:/glusterfs/brick
Host test1 not a friend
{% endhighlight %}

### Gluster volume create hangs

If you get;

{% highlight text %}
root@test1$ gluster volume create gv1 replica 2 transport tcp test1:/glusterfs/brick test2:/glusterfs/brick
--- timeouts after 5 minutes ----
root@test1$ gluster volume create gv1 replica 2 transport tcp test1:/glusterfs/brick test2:/glusterfs/brick
Another operation is in progress, please retry after some time
{% endhighlight %}

You MUST not "gluster peer probe" the local machine.. if this happens you cannot remove it, and glusterfs will hang on creation. To fix this, you can either;

Purge all peers, then re-probe;

{% highlight text %}
$ rm -f /etc/glusterd/peers/*
{% endhighlight %}

Or find the specific peer you want, then remove;

{% highlight text %}
$ gluster peer status
$ rm -f /etc/glusterd/peers/ID-HERE
{% endhighlight %}

### Pre-existing volumes (or failed volume creation)

If you get;

{% highlight text %}
root@test1$ gluster volume create gv1 replica 2 transport tcp test1:/glusterfs/brick test2:/glusterfs/brick
Operation failed on test2
{% endhighlight %}

If a volume creation fails, you might hit [this problem.][1]. To fix it, all you need to do is;

{% highlight text %}
setfattr -x trusted.glusterfs.volume-id $brick_path
setfattr -x trusted.gfid $brick_path
rm -rf $brick_path/.glusterfs
{% endhighlight %}

 [1]: http://joejulian.name/blog/glusterfs-path-or-a-prefix-of-it-is-already-part-of-a-volume/