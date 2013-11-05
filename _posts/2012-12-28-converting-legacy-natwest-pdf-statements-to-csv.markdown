---
layout: post
title:  Converting legacy Natwest CC PDF statements to importable CSV
date:   2012-12-28 00:00:00
categories: general
coverimage: /img/covers/legacy-natwest-cc.png
---



This code is alpha as fuck, and you will almost certainly have to either modify or make your own depending on your own circumstances. This article is just to show you how we did it and give some food for thought. My apologies for the heavily obfuscated text, you can view these yourself by logging into your own portal. For those of you that use Natwest credit cards, you are probably all too familiar with the "4 month restriction" on downloading transactions, after which they only provide PDF statements. 

This is not very helpful when you need to import your data into an accountancy package (such as Microsoft Money, Xero, Excel etc). I nearly had to manually input all our statements, but then I realised "oh wait, I'm a programmer!". If there was only a few transactions, I'd have just imported them manually.. but we had hundreds of archived transactions that we needed to import, and I was sure as hell not going to waste my Friday afternoon doing this! 

### How it works 

I downloaded an existing CSV from the Natwest CC portal to find out the expected format, which was; 

{% highlight text %}
Transaction Date, Transaction Description, Transaction Type, Country Code, Transaction Amount, Currency  
26/12/2012,X X X,X X X-X,X,X,X X,GBR,£1.00,United Kingdom, Pounds (GBP)  
26/12/2012,X X,X, X X X X,GBR,£1.00,United Kingdom, Pounds (GBP)  
24/12/2012,X X,X X,GBR,£1.00,United Kingdom, Pounds (GBP)  
24/12/2012,X X X X X,X X (X X X X X),GBR,£2.00,United Kingdom, Pounds (GBP)
{% endhighlight %} 

Annoyingly, the CSV provided by the Natwest CC is actually broken, as it doesn't have quotes around the fields, and uses the field delimiter in those strings... 

*sigh*. So we look at the CSV provided by the Natwest portal (yes, there are two different systems!), which uses the correct format; 

{% highlight text %}
02 Aug 2012,XXX,"'X X X X X",-1.00,,"'A SMITH","'5123456789012345",  
03 Aug 2012,XXX,"'XXX XXX XXX , 1.00 USD",2.00,,"'A SMITH","'5123456789012345",  
12 Aug 2012,XXX,"'X X X X",1.00,,"'A SMITH","'5123456789012345",  
18 Aug 2012,XXX,"'X X CA , 1.00 USD",2.00,,"'A SMITH","'5123456789012345",
{% endhighlight %} 

Now, we download the individual statements from the Natwest CC portal (of which it allows you to download over a years worth), open with Acrobat Reader, then copy and paste manually into notepad.. what we get is; 

{% highlight python %}
13 APR 16 APR 12345678 X X X X X 4.00  
13 APR 16 APR 12345678 X X/X X 4.00  
11 APR 16 APR 12345678 X X X X 1.00  
15 APR 16 APR 12345678 X *X.X X X 1.00  
17 APR 17 APR 12345678 X X X - X X 30.00 -  
18 APR 19 APR 12345678 X*X X-X-X X 1.00  
26.99 USD EXCHANGE RATE 1.553828  
19 APR 20 APR 12345678 X X X X X 1.00  
19 APR 20 APR 12345678 X X/X X 2.00  
20 APR 23 APR 12345678 X X/X X X/X X 7.00  
20 APR 23 APR 12345678 X X 123455677 1.00  
22 APR 23 APR 12345678 X 123455677 NJ 4.00  
65.93 USD EXCHANGE RATE 1.568268
{% endhighlight %} The first date is the trans date, the second is the post date.. the third is some ID that doesn't seem relevant to what we need, the fourth is the description and the last is the amount. As you can see it's not a straight transform, so we need to play with it a bit. 

The final regex we ended up with was, along with an example in RegexBuddy; 

{% highlight text %}
^(?P<trans_date>\d{2}) (?P<trans_month>\w{3}) (?P<post_date>\d{2}) (?P<post_month>\w{3}) (?P<some_id>\w{8}) (?P<desc>.+) (?P<amount_pounds>\d+)\.(?P<amount_pence>\d+)(?: |)(?P<negative>-|)
{% endhighlight %}

[![legacy-natwest-1.png](/img/postcontent/legacy-natwest-1.png)](/img/postcontent/legacy-natwest-1.png)

### Final result

{% highlight python %}

$ python test.py
12 APR 2012,CREDIT,"'X X X X X ",1.47,,"'A SMITH","'5123456789012345",
12 APR 2012,CREDIT,"'X'X X/X X ",4.00,,"'A SMITH","'5123456789012345",
12 APR 2012,CREDIT,"'X X X X ",1.50,,"'A SMITH","'5123456789012345",
13 APR 2012,CREDIT,"'X *X.X X X ",1.99,,"'A SMITH","'5123456789012345",
14 APR 2012,CREDIT,"'X X X - X X ",10.00,,"'A SMITH","'5123456789012345",
11 JUL 2012,CHARGE,"'INTEREST ",1.50,,"'A SMITH","'5123456789012345",
02 AUG 2012,CREDIT,"'FASTER PAYMENT RECEIVED - THANK YOU ",-100.00,,"'A SMITH","'5123456789012345",
{% endhighlight %}


### Proof of concept code

{% highlight python %}

#!/usr/bin/env python
# thanks http://stackoverflow.com/questions/255332/python-re-findall-with-groupdicts

# we have to manually specify the damn year.. this could be auto extracted from the pdf text, but im too lazy
# if you have pdfs spreading over a year end period, then you might want to look into adding this
YEAR="2012"

# put your card number here
# if your card number has changed between statements, then you need to take this into consideration
ACCOUNT_NUMBER="5511222233334444"

# put your account name here
ACCOUNT_NAME="A SMITH"

import datetime
import re
from decimal import Decimal
from pprint import pprint as p

m = re.compile("^(?P<trans_date>\d{2}) (?P<trans_month>\w{3}) (?P<post_date>\d{2}) (?P<post_month>\w{3}) (?P<some_id>\w{8}) (?P<desc>.+) (?P<amount_pounds>\d+)\.(?P<amount_pence>\d+)(?: |)(?P<negative>-|)", re.MULTILINE)
data = open("test.txt", "rb").read()
data = [m.groupdict() for m in m.finditer(data)]
for x in data:
    d = "%s %s %s" % ( x['post_date'], x['post_month'], YEAR)
    dt = datetime.datetime.strptime(d, "%d %b %Y").date()
    amount = Decimal("%s.%s" % ( x['amount_pounds'], x['amount_pence'], ) )
    data = {
             'desc' : x['desc'],
             'day' : x['trans_date'],
             'month' : x['trans_month'],
             'year' : YEAR,
             'amount' : amount,
             'account_number' : ACCOUNT_NUMBER,
             'account_name' : ACCOUNT_NAME,
        }

    # CREDIT ADJ is NOT HANDLED!!!!
    if x['some_id'] == 'INTEREST':
        print '''%(day)s %(month)s %(year)s,CHARGE,"INTEREST ",-%(amount)s,,"%(account_name)s","%(account_number)s",''' % data
    elif x['negative']:
        # PAYMENT and CREDIT are treated as the same thing, this may be very bad!!!!
        print '''%(day)s %(month)s %(year)s,CREDIT,"%(desc)s ",%(amount)s,,"%(account_name)s","%(account_number)s",''' % data
    else:
        print '''%(day)s %(month)s %(year)s,SALE,"%(desc)s ",-%(amount)s,,"%(account_name)s","%(account_number)s",''' % data
{% endhighlight %}
