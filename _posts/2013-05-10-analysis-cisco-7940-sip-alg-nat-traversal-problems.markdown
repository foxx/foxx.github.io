---
layout: post
title:  Analysis of Cisco 7940, SIP ALG and NAT traversal problems
date:   2013-05-10 00:00:00
categories: general
coverimage: /img/covers/analysis-of-cisco-7940-sip.jpg
---



I'm personally a huge fan of the Cisco phones, ever since I was a little kid I'd always wanted one.. I'd see them on TV shows, they were in the offices at school, and it made me insanely jealous that I couldn't have one. Now I'm all grown up, and about a year ago I purchased my very first [Cisco 7940][1] phone.. It was an exciting day, trying to re-flash a 10 year old phone with nothing but a monochrome LCD with no backlight, and a few buttons. Eventually after 2-3 days of messing around, I managed to get it hooked up to a TFTP, [reflashed with the SIP firmware][2], and connected to my provider.

The phone did not work with my first provider ([Gradwell][3]), and their support blamed this on the fact that it was an "unsupported phone". So I threw up an install of 3cx on a colo, and all was good. Then Virgin Media released a firmware upgrade R37 ([discussed here][4]) which broke my poor Cisco phone again. So I purchased a shiny new [TP-Link WR1043N][5], put my VM router into modem mode, and boom everything was working again. After a few months I needed to get a Dual WAN router (as we had a second ADSL line installed, due to latency issues at peak times on Virgin Media), so we decided to buy another router. Given that the WR1043N worked without problem, we bought a lovely [TP-Link ER6020 Dual WAN Gigabit][6] router.

But then to my horror, the Cisco phone stopped working again! To confuse things even more, although the Cisco phone had stopped functioning, the softphone's on our PCs continued to function without problem. I'd just spent £100 on this lovely new router, and I really didn't want to RMA it. So I decided to actually dig into why this was happening.. I had recently switched into the world of SIP and telecoms about 1 year ago and figured it would be an excellent learning opportunity.

### Test 1 - Cisco 7940 phone

So, let's follow the packet conversation and see where things are breaking. First we fire up [Wireshark][7] on our server and set up the necessary filters, and then we enable some debugging on the Cisco phone to show the SIP messages being sent and receives, we do this via the telnet interface on the Cisco phone by executing the following;

{% highlight text %}
$ telnet 192.168.1.104
Password: *****
Cisco7940# debug sip-messages
Enabling bug logging on this terminal - use 'tty mon 0' to disable
{% endhighlight %}

Cisco phone sends REGISTER packet:

{% highlight text %}
[17:00:53:148185] sipTransportSendMessage: Closed a one-time UDP send channel handle = 3
[17:00:53:148194] sipTransportSendMessage: ccb &lt;7>: config &lt;5.79.5.158>:&lt;5060> - remote &lt;5.79.5.158>:&lt;5060>
[17:00:53:148194] sipTransportSendMessage: Opened a one-time UDP send channel to server &lt;5.79.5.158>:&lt;5060>, handle = 3 local port= 5060
[17:00:53:148195] sipTransportSendMessage:Sent SIP message to &lt;5.79.5.158>:&lt;5060>, handle=&lt;3>, length=&lt;567>, message=

[17:00:53:148195] REGISTER sip:3cx.voiceflare.co.uk SIP/2.0
Via: SIP/2.0/UDP 192.168.1.104:5060;branch=z9hG4bK683a1a40
From: &lt;sip:2006@3cx.voiceflare.co.uk>;tag=000c30a97025005c3fa02d4d-5ce6939d
To: &lt;sip:2006@3cx.voiceflare.co.uk>
Call-ID: 000c30a9-70250003-381e261d-34d10c8e@192.168.1.104
Max-Forwards: 70
Date: Fri, 10 May 2013 16:00:52 GMT
CSeq: 145 REGISTER
User-Agent: Cisco-CP7940G/8.0
Contact: &lt;sip:2006@192.168.1.104:5060;transport=udp>;+sip.instance="&lt;urn:uuid:00000000-0000-0000-0000-000c30a97025>";+u.sip!model.ccm.cisco.com="8"
Content-Length: 0
Expires: 120
{% endhighlight %}

3CX server receives REGISTER packet

{% highlight text %}
Internet Protocol Version 4, Src: 86.5.223.17 (86.5.223.17), Dst: 5.79.5.158 (5.79.5.158)
User Datagram Protocol, Src Port: 23201 (23201), Dst Port: sip (5060)

REGISTER sip:3cx.voiceflare.co.uk SIP/2.0
Via: SIP/2.0/UDP 192.168.1.104:5060;branch=z9hG4bK683a1a40
From: &lt;sip:2006@3cx.voiceflare.co.uk>;tag=000c30a97025005c3fa02d4d-5ce6939d
To: &lt;sip:2006@3cx.voiceflare.co.uk>
Call-ID: 000c30a9-70250003-381e261d-34d10c8e@192.168.1.104
Max-Forwards: 70
Date: Fri, 10 May 2013 16:00:52 GMT
CSeq: 145 REGISTER
User-Agent: Cisco-CP7940G/8.0
Contact: &lt;sip:2006@192.168.1.104:5060;transport=udp>;+sip.instance="&lt;urn:uuid:00000000-0000-0000-0000-000c30a97025>";+u.sip!model.ccm.cisco.com="8"
Content-Length: 0
Expires: 120

{% endhighlight %}

3CX server sends 407 response packet:

{% highlight text %}
Internet Protocol Version 4, Src: 5.79.5.158 (5.79.5.158), Dst: 86.5.223.17 (86.5.223.17)
User Datagram Protocol, Src Port: sip (5060), Dst Port: sip (5060)

SIP/2.0 407 Proxy Authentication Required
Via: SIP/2.0/UDP 192.168.1.104:5060;branch=z9hG4bK683a1a40;received=86.5.223.17
Proxy-Authenticate: Digest nonce="414d535c079daad234:38465ad0db9a18427774f51f1dcb7ab3",algorithm=MD5,realm="3CXPhoneSystem"
To: &lt;sip:2006@3cx.voiceflare.co.uk>;tag=1c7d7042
From: &lt;sip:2006@3cx.voiceflare.co.uk>;tag=000c30a97025005c3fa02d4d-5ce6939d
Call-ID: 000c30a9-70250003-381e261d-34d10c8e@192.168.1.104
CSeq: 145 REGISTER
User-Agent: 3CXPhoneSystem 11.0.28976.849 (28862)
Content-Length: 0
{% endhighlight %}

Cisco phone does not receive a response, and then continues to send more REGISTER packets

{% highlight text %}
No packet received
{% endhighlight %}

Let's break down what actually happened here;

*   Cisco phone sends a REGISTER packet from 192.168.1.104:5060 to 5.79.5.158:5060
*   TP-Link ER6020 NAT randomizes the source port to 23201
*   3CX server receives REGISTER packet from 86.5.223.17:23201 to 5.79.5.158:5060
*   3CX server sends 407 response from 5.79.5.158:5060 to 86.5.223.17:5060
*   Cisco phone does not receive a response

So why did the Cisco phone not receive a response? The ER-6020 randomized the source port to 23201 and will forward any packets from 5.79.5.158:23201 back to the phone (which is to be expected with NAT source port randomization). However 3CX is sending its response to port 86.5.223.17:5060 instead of 86.5.223.17:23201, despite the packet being received by the server from src port 23201. This is because 3CX looks at the Via header of the REGISTER packet, and sends the response to the port inside there (which in this case is 5060), as you can see below;

{% highlight text %}
Via: SIP/2.0/UDP 192.168.1.104:5060;branch=z9hG4bK683a1a40;received=86.5.223.17
{% endhighlight %}

The SIP ALG feature on the ER6020 is supposed to rewrite these SIP packets so the port (in our case, 5060) is replaced with the newly randomized NAT source port (in our case, 23201). But this is not happening, and thus the response is never received.

### Test 2 - 3CX Softphone

So we know that the Softphone is working, let's look at the packet conversation and see what's different to the Cisco. In this test, we use Wireshark on the computer where the Softphone is installed, and also use Wireshark on the server side.

Softphone sends REGISTER packet

{% highlight text %}
Internet Protocol Version 4, Src: 192.168.1.101 (192.168.1.101), Dst: 5.79.5.158 (5.79.5.158)
User Datagram Protocol, Src Port: 50822 (50822), Dst Port: sip (5060)

REGISTER sip:3cx.voiceflare.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP 192.168.1.101:50822;branch=z9hG4bK-d8754z-ae09014c5a6a9d05-1---d8754z-;rport
Max-Forwards: 70
Contact: &lt;sip:2101@192.168.1.101:50822;rinstance=b9a426fa141ad0b8>
To: &lt;sip:2101@3cx.voiceflare.co.uk:5060>
From: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=196d716f
Call-ID: ODBiMThkMTBlMTNkNzViZjhmNjFlMGVkOWI5ZDYxOTI.
CSeq: 1 REGISTER
Expires: 120
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE
Supported: replaces
User-Agent: 3CXPhone 6.0.26523.0
Content-Length: 0
  {% endhighlight %}

3CX server receives packet

{% highlight text %}
Internet Protocol Version 4, Src: 86.5.223.17 (86.5.223.17), Dst: 5.79.5.158 (5.79.5.158)
User Datagram Protocol, Src Port: 36321 (36321), Dst Port: sip (5060)

REGISTER sip:3cx.voiceflare.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP 192.168.1.101:50822;branch=z9hG4bK-d8754z-ae09014c5a6a9d05-1---d8754z-;rport
Max-Forwards: 70
Contact: &lt;sip:2101@192.168.1.101:50822;rinstance=b9a426fa141ad0b8>
To: &lt;sip:2101@3cx.voiceflare.co.uk:5060>
From: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=196d716f
Call-ID: ODBiMThkMTBlMTNkNzViZjhmNjFlMGVkOWI5ZDYxOTI.
CSeq: 1 REGISTER
Expires: 120
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE
Supported: replaces
User-Agent: 3CXPhone 6.0.26523.0
Content-Length: 0
  {% endhighlight %}

3CX server sends packet

{% highlight text %}
Internet Protocol Version 4, Src: 5.79.5.158 (5.79.5.158), Dst: 86.5.223.17 (86.5.223.17)
User Datagram Protocol, Src Port: sip (5060), Dst Port: 36321 (36321)

SIP/2.0 407 Proxy Authentication Required
Via: SIP/2.0/UDP 192.168.1.101:50822;branch=z9hG4bK-d8754z-ae09014c5a6a9d05-1---d8754z-;rport=36321;received=86.5.223.17
Proxy-Authenticate: Digest nonce="414d535c079dae1434:0e5072f08759b92e57a4b45600d18248",algorithm=MD5,realm="3CXPhoneSystem"
To: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=84420f52
From: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=196d716f
Call-ID: ODBiMThkMTBlMTNkNzViZjhmNjFlMGVkOWI5ZDYxOTI.
CSeq: 1 REGISTER
User-Agent: 3CXPhoneSystem 11.0.28976.849 (28862)
Content-Length: 0
  {% endhighlight %}

Softphone receives packet

{% highlight text %}
Internet Protocol Version 4, Src: 5.79.5.158 (5.79.5.158), Dst: 192.168.1.101 (192.168.1.101)
User Datagram Protocol, Src Port: sip (5060), Dst Port: 50822 (50822)

SIP/2.0 407 Proxy Authentication Required
Via: SIP/2.0/UDP 192.168.1.101:50822;branch=z9hG4bK-d8754z-ae09014c5a6a9d05-1---d8754z-;rport=36321;received=86.5.223.17
Proxy-Authenticate: Digest nonce="414d535c079dae1434:0e5072f08759b92e57a4b45600d18248",algorithm=MD5,realm="3CXPhoneSystem"
To: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=84420f52
From: &lt;sip:2101@3cx.voiceflare.co.uk:5060>;tag=196d716f
Call-ID: ODBiMThkMTBlMTNkNzViZjhmNjFlMGVkOWI5ZDYxOTI.
CSeq: 1 REGISTER
User-Agent: 3CXPhoneSystem 11.0.28976.849 (28862)
Content-Length: 0
  {% endhighlight %}

Again, let's break down what happened here;

*   Softphone sends a REGISTER packet from 192.168.1.101:50822 to 5.79.5.158:5060
*   TP-Link ER6020 NAT randomizes the source port to 36321
*   3CX server receives REGISTER packet from 86.5.223.17:36321 to 5.79.5.158:5060
*   3CX server sends 407 response from 5.79.5.158:5060 to 86.5.223.17:36321
*   Softphone receives 407 response from 5.79.5.158:5060

### So why is it broken?

So from the results in test 2, we can determine that SIP ALG is still broken, if you look at the Via header you'll see that the SIP ALG is still not functioning correctly, and contains the original source port (50822) instead of the newly randomized source port (36321), just like the Cisco phone.

{% highlight text %}
Via: SIP/2.0/UDP 192.168.1.101:50822;branch=z9hG4bK-d8754z-ae09014c5a6a9d05-1---d8754z-;rport
  {% endhighlight %}

So why did the softphone work, but not the Cisco phone? It's because the softphone has included a small parameter on the end of the Via header called 'rport'. Let's take a look at the [SIP RFC 3581][8], which defines 'Symmetric Response Routing' for SIP.

{% highlight text %}
This extension defines a new parameter for the Via header field, called "rport", that allows a 
client to request that the server send the response back to the source IP address and port 
where the request came from. 
  {% endhighlight %}

Now it turns out that this had already been discussed (in extensive detail) back in 2010 over at <http://forum.sipsorcery.com/viewtopic.php?f=6&t=2165>, although no one had done an analysis of why it was working, or what the viable solutions were.

### How to fix it?

There are several ways that you can fix this problem, all with their pros and cons.

A) Disable port randomization on your NAT (this is referred to as 'static-port' in BSD) However, this could break some phone equipment that doesn't already do its own source port randomization, because if two phones insist on receiving a response on 5060 from the same host, then the router won't know where to send the packet to. Even if the phone does it's own randomization, you could also end up with potential port collision, because if two computers choose the same source port for the same destination, then the router is then not able to prevent overlapping.

B) Use static port forwarding (one-to-one NAT) for the phone. If you have phone equipment that doesn't enable rport, then you can enable this feature and force the packets to flow back to the phone. However it means you can only have one "broken phone" on your network, because any response packets on the source port would be forcibly sent to one phone.

C) Enable SIP ALG on your router. This is a good way of resolving the problem but sadly many routers do not implement SIP ALG correctly, and many do it differently. For example, some routers implement SIP ALG by disabling port randomization for SIP packets, where as other routers re-write the Via header in the SIP packet.

D) Enable 'rport' on your phone. Some phones do this by default (such as the Softphone), and it's possible that some phones also allow you to enable/disable this in their configuration. However, despite a 15 minute search on Google, the Cisco 7940 doesn't seem to allow the rport to be optionally enabled or disabled, it's always disabled.

E) Enable forced 'rport' on your server. Some servers allow you to force 'rport', for example using the [NDLB-force-rport][9] option in [FreeSWITCH][10]. However the 3CX server does not appear to let you do this. This can also cause some phones to break, and should be enabled on an opt-in basis.

F) Use a local SIP gateway behind NAT. You could set up a SIP gateway in your LAN which trunks to your external SIP server, but I've never been a fan of using port forwarding or selective one-to-one NAT for trunking, it means having to ensure a specific port range is only NAT'd (for RTP, SIP etc), and some routers don't handle this very well.

G) Use a SIP friendly VPN gateway. Some people opt to run their phones over a VPN gateway, this eliminates a lot of routing/mangling issues that you'd typically see running SIP clients straight over the internet. However, I'm yet to find a gateway that does this properly for a cheap price. The Meraki equipment looks good, but I haven't tested this yet and it's a tad expensive.

H) Use a different phone. Although until you have purchased the phone and tested it, then it's not guaranteed to work. And if you change routers or providers, then it could break.

### Moral of the story

The SIP RFCs really do suck, and different engineers end up implementing them slightly differently. This means that specific combinations of servers, routers and phone are not guaranteed to work, and it isn't always clear who should be to blame, because these problems can be interpreted in different ways depending on how you look at it. This is purely because of the looseness of the SIP RFC specifications, and the problem isn't going to go away any time soon.

I submitted a ticket to TP-Link on 10th May 2013 asking them to release a firmware fix for their SIP ALG to add support for broken phones, but it could be argued that the phone manufacturer or the server vendors should be the one fixing their side. I'm hoping that TP-Link will step up and offer a fix, they seem to be a decent company and this would really give them a chance to show that they care.

I've submitted a ticket to 3CX asking them to include the ability to force 'rport' for specific clients, but given that they can't even be bothered to upgrade their [vulnerable 3CX phone libraries][11] on the basis that it is open source software, I'm not holding my breath! (Kudos to Stefan Kanthak for discovering this).

For shits and giggles, I've also submitted a ticket to Cisco asking them to release a firmware upgrade that allows for the rport to be forcibly enabled. I don't for a second believe that they will ever do such a thing, but thought I'd try for the sake of completeness.

### Question time

So who is the blame here? 3CX? Cisco? TP-Link? RFCs? Let me know your thoughts.

 [1]: http://www.cisco.com/en/US/products/hw/phones/ps379/ps1854/index.html
 [2]: http://www.3cx.com/blog/docs/cisco-7940-sip/
 [3]: http://www.gradwell.com/
 [4]: http://community.virginmedia.com/t5/Up-to-120Mb-Setup-Equipment/IMPORTANT-R37-breaks-SOME-hardware-VoIP-SIP-phones-as-of-13th/td-p/1608966
 [5]: http://www.tp-link.dk/products/details/?model=TL-WR1043ND
 [6]: http://www.tp-link.com/en/products/details/?model=TL-ER6020
 [7]: http://wiki.wireshark.org/SIP
 [8]: http://www.ietf.org/rfc/rfc3581.txt
 [9]: http://wiki.freeswitch.org/wiki/NDLB#NDLB-force-rport
 [10]: http://www.freeswitch.org
 [11]: http://www.securityfocus.com/archive/1/526541