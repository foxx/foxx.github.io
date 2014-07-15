---
layout: post
title:  Python random.random() collisions caused by str() cast
date:   2012-12-04 00:00:00
categories: general
coverimage: /img/covers/piccard1.jpg
weight: 5
keywords: collision, random, python, repr, str, cast
desc: Generating random number collisions in Python due to bad casting
---


Today we were building a queuing system that generated job IDs using an MD5 of random.random(), but noticed we were getting collisions every few seconds. However, after much investigation, this was failing because str() automatically rounds depending on what Python version you are on. 

Total time wasted, 2 hours 14 minutes (not including the time it took to write this thread  This has been discussed in full detail here; <http://bugs.python.org/issue16609> In a nut shell - casting random.random() to an str() ends up with an automatic rounding, where as using repr() leaves the precision as it is. If you cast to an str() in certain versions of Python, you will lose precision, and end up with non random/colliding randomness. 

### Correct

{% highlight python %}
>>> print repr(random.random());
0.33885573194811902
>>> print repr(random.getrandbits(64));
6543444180651906361L
{% endhighlight %}

### Incorrect

{% highlight python %}
>>> print str(random.random());
0.880223937771
{% endhighlight %}

#### Example

{% highlight python %}
>>> import random  
>>> random.random()  
0.33885573194811902  
>>> x = random.random()  
>>> x  
0.88022393777095409  
>>> print x  
0.880223937771  
>>> str(x)  
'0.880223937771'  
>>> print str(x)  
0.880223937771  
>>> repr(x)  
'0.88022393777095409'  
>>> str(repr(x))  
'0.88022393777095409'  
{% endhighlight %}

### Reproducing the problem

{% highlight python %}
#!/usr/bin/env python

import random
import redis
import sys
import time
import pickle
import sys

def md5sum(val):
    return str(val)
    from hashlib import sha1
    o = sha1()
    o.update(str(val))
    return o.hexdigest()

class RandomTest(object):
    def __init__(self, *args, **kwargs):
        pass

    def test(self, method, iterations):
        print "testing %s for %s iterations" % ( method, iterations, )

        h = {}
        start_ts = time.time()

        for i in range(iterations):
            k = "test_%s" % ( method, )
            assert hasattr(self, k), "invalid test method"
            val = getattr(self, k)()
            val = str(val)
            elapsed = time.time() - start_ts
            if h.has_key(val):
                print ""
                print "collision %s - took %ss / iteration %s" % ( val, elapsed, i)
                return

            h[val] = True

            if i % 100000 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()

        print ""
        print "no collision detected"

    def test_random1(self):
        return random.random()

    def test_random2(self):
        return repr(random.random())

    def test_random1md5(self):
        return md5sum(str(random.random()))

    def test_random2md5(self):
        return md5sum(repr(random.random()))

iterations = 5000000
t = RandomTest()
t.test(method='random1', iterations=iterations)
t.test(method='random2', iterations=iterations)
t.test(method='random1md5', iterations=iterations)
t.test(method='random2md5', iterations=iterations)

{% endhighlight %}

{% highlight python %}
$ python hsetnx_send.py  
testing random1 for 5000000 iterations  
...................  
collision 0.336826610526 - took 19.6727981567s / iteration 1879939  

testing random2 for 5000000 iterations
..................................................  
no collision detected  

testing random1md5 for 5000000 iterations  
.............  
collision 0.385472739752 - took 13.8068420887s / iteration 1284184  

testing random2md5 for 5000000 iterations  
..................................................  
no collision detected  
{% endhighlight %}