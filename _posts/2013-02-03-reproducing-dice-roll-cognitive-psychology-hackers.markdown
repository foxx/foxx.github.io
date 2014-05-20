---
layout: post
title:  Reproducing 'dice roll' from [27C3] Cognitive Psychology for Hackers
date:   2013-02-03 00:00:00
categories: general
coverimage: /img/covers/reproducing-dice-roll.png
weight: 15
---


On a lazy Sunday afternoon, I was watching a presentation by [Sai Zai][1] on [Cognitive Psychology for Hackers from 27C3][2]. At around 13 minutes in, he showed an example of betting against a dice roll on the following slide (as seen in the article picture above).Immediately, the most obvious choice to me was B, but was quickly told I was wrong. Despite this being explained I still didn't understand why this was happening, and found it difficult to believe. So I wrote a little Python script to reproduce this, which proved me wrong :)

Edit 10/05/2013: Sai Zai was kind enough to reach out to me after discovering my blog post, and explain in more detail about why this happens;

{% highlight text %}
FWIW, you needn't've done a monte carlo simulator on this one. It's
very basic probability theory; you can compute the answer pretty
straightforwardly by just multiplying the individual probabilities.
Unless you doubt *that*, in which case yeah, a monte carlo sim is the
right way to go. ;-)

It's not 2^5 *equal* choices. It's 1/3 blue per roll, 2/3 green.
They're independent rolls, and those aren't equally weighted dice.

So e.g. BG (exactly, not BG + GB) = (1/3)*(2/3). (Same for GB. Add BB
& GG, and you get 1.)

Thus BGB = 2/27, etc; BGBBB = 2/(3^5). Adding another G on the front
is that * (2/3). ;-)

BTW, https://www.youtube.com/watch?v=N_AzEzxJW5E&list=PL67D7801116B579E9&index=2
is a more recent iteration of the same talk. Has a few more examples added.
{% endhighlight %}

Here were the results;

{% highlight python %}

$ python test2.py

####################################################
#
# Reproducing 'dice roll' from the video
# Cognitive Psychology for Hackers
# See http://www.youtube.com/watch?v=uJAuAuGboOM (14:00m)
#
# cal.leeming [at] simplicitymedialtd.co.uk
# 03/02/2013
#
####################################################

- Choices: ['G', 'G', 'G', 'G', 'B', 'B']
- Answers: ['BGBBB', 'GBGBBB', 'GBBBBB']
- Attempts: 2000

Place your bets..


Our winner is: BGBBB
Answer     Found      Total chance    Compared chance
BGBBB      1005       0.824%          50.250%
GBGBBB     646        0.529%          32.300%
GBBBBB     349        0.286%          17.450%
{% endhighlight %}

And here is the code I used as a proof of concept, I was supposed to be working when doing this, so apologies for the mess. Enjoy!

<script src="https://gist.github.com/foxx/b36138811f61305ffc66.js"></script>

 [1]: http://s.ai/
 [2]: http://www.youtube.com/watch?v=uJAuAuGboOM