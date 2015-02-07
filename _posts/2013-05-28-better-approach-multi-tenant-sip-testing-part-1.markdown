---
layout: post
title:  Better approach for multi-tenant SIP testing - part 1
date:   2013-05-28 00:00:00
categories: general
coverimage: /img/postcontent/multi-tenant-1.png
weight: 16
type: small
keywords: voip, sip, 3cx, 3cxphone, 3cx phone, vmware, windows, multi user, multiuser
desc: How to properly test multi user SIP platforms
---


Building our own VoIP platform has been an interesting journey, and there are many scenarios you need to test to ensure the call flow is handled correctly. Attempting to test this logic with desk phones can quickly become overwhelming, and makes the development process dependent on hardware. Although you should always do a hardware compatibility test on every release, virtualizing this system is a great way of speeding up development. This approach has saved me countless hours in unnecessary overheads during testing.

In our scenario, we have a total of 12 users/DDIs which would very quickly become troublesome if we didn't virtualize.

*   Cluster of 3 FS servers
*   2 customer domains on FS1, total of 6 users
*   1 customer domain on FS2, total of 3 users
*   1 faux provider on FS3, total of 3 users

The faux provider essentially acts like a PSTN gateway, so you can simulate making calls to PSTN without having to use a real provider. Two of the customer domains are on switch 1, the other domain is on switch 2. You then need to ensure that the call flow works correctly when transferring calls between domains, and when calls are bridged/transferred via FS apps.

### Tools used

*   [VMWare Workstation][2] to create a Windows 7 guest
*   3cxphone
*   WindowManager
*   some custom .bat scripts
*   a custom background

### Multiple instances

3CXPhone does not allow you to run multiple instances, instead you have to have one windows user per phone, and create a copy of the program as well. This allows you to run the phone within the context of another user, thus bypassing the multiple instance protection. So for 12 phones, we need 12 windows accounts and 12 application copies, like such;

[![multi-tenant-2.png](/img/postcontent/multi-tenant-2.png)](/img/postcontent/multi-tenant-2.png)

[![multi-tenant-3.png](/img/postcontent/multi-tenant-3.png)](/img/postcontent/multi-tenant-3.png)

### Automating start/stop

Starting and stopping each phone manually is also a pain in the ass, because you'd have to enable the run as context and then re-enter the login details every time. Instead, we use a small batch script to automate this procedure, it will ask you for a password the first time you run it after which it will never ask again (even after reboot).

{% highlight text %}
@echo off
echo "Starting new phones"
runas /savecred /user:sphone1 "C:\Program Files (x86)\3CXPhone\3CXPhone1.exe"
runas /savecred /user:sphone2 "C:\Program Files (x86)\3CXPhone\3CXPhone2.exe"
runas /savecred /user:sphone3 "C:\Program Files (x86)\3CXPhone\3CXPhone3.exe"
runas /savecred /user:sphone4 "C:\Program Files (x86)\3CXPhone\3CXPhone4.exe"
runas /savecred /user:sphone5 "C:\Program Files (x86)\3CXPhone\3CXPhone5.exe"
runas /savecred /user:sphone6 "C:\Program Files (x86)\3CXPhone\3CXPhone6.exe"
runas /savecred /user:sphone7 "C:\Program Files (x86)\3CXPhone\3CXPhone7.exe"
runas /savecred /user:sphone8 "C:\Program Files (x86)\3CXPhone\3CXPhone8.exe"
runas /savecred /user:sphone9 "C:\Program Files (x86)\3CXPhone\3CXPhone9.exe"
runas /savecred /user:sphone10 "C:\Program Files (x86)\3CXPhone\3CXPhone10.exe"
runas /savecred /user:sphone11 "C:\Program Files (x86)\3CXPhone\3CXPhone11.exe"
runas /savecred /user:sphone12 "C:\Program Files (x86)\3CXPhone\3CXPhone12.exe"
{% endhighlight %}

To stop the phones, we use the following script;

{% highlight text %}
@echo off
echo "Killing old phones"
taskkill /F /IM "3cxphone1.exe"
taskkill /F /IM "3cxphone2.exe"
taskkill /F /IM "3cxphone3.exe"
taskkill /F /IM "3cxphone4.exe"
taskkill /F /IM "3cxphone5.exe"
taskkill /F /IM "3cxphone6.exe"
taskkill /F /IM "3cxphone7.exe"
taskkill /F /IM "3cxphone8.exe"
taskkill /F /IM "3cxphone9.exe"
taskkill /F /IM "3cxphone10.exe"
taskkill /F /IM "3cxphone11.exe"
taskkill /F /IM "3cxphone12.exe"
{% endhighlight %}

### Creating a background template

Next you want to decide on a layout for your phones on the desktop, depending on your screen size. In our case, we knew we wanted 12 phones to fit onto a 1920x1080 space so after choosing a neutral background image, we mocked up the spacing in photoshop and put a label above each one. Export as a PNG and set as your background. Starting your phones up for the first time will result in everything being cramped into the middle, looking a bit like this;

[![multi-tenant-4.png](/img/postcontent/multi-tenant-4.png)](/img/postcontent/multi-tenant-4.png)

## Positioning the windows

Manually dragging the windows would suck, and this is where WindowManager comes in. There are many automated window positioning tools out there (such as Actual Window Manager) but not all of them support multi user positioning, where as WindowManager seems to work well (most of the time). Move each phone into the correct position (you can do this at random for now, as the phones have not been configured), and then start WindowManager. Delete any items from the windowmanager list that are not relevant to 3CXPhone, so you end up with a list like the following;

[![multi-tenant-4.png](/img/postcontent/multi-tenant-4.png)](/img/postcontent/multi-tenant-5.png)

Go into each item and tick the "Move to" checkbox, select "This position" and then click "Get". This should cause the x/y cords to be automatically filled in, click OK then repeat this for each phone in the list, as seen below;

[![multi-tenant-6.png](/img/postcontent/multi-tenant-6.png)](/img/postcontent/multi-tenant-6.png)

WindowManager can sometimes be a little fussy, and doesn't always position correctly. If this happens, simply click "Quit" on the WindowManager program and then re-run it. Don't right click on the taskbar button as this will cause it to disable and not exit, which doesn't fix the problem. Once you run it, you should see the windows automatically position themselves on the page. You'll need to then configure each phone with the correct user/domain relevant to the label above each one.

And boom, you now have a segregated and fully functional testing environment for your multi-tenant platform. It's also worth mentioning that you could do this in Linux if you don't want to pay for a Windows license. Have you done similar things like this? Feel free to link to your article/project in the comments below.

And here's the final result;

[![multi-tenant-1.png](/img/postcontent/multi-tenant-1.png)](/img/postcontent/multi-tenant-1.png)

 [1]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/8.png
 [2]: http://www.vmware.com/products/workstation/ "http://www.vmware.com/products/workstation/"
 [3]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/3.png
 [4]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/4.png
 [5]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/51.png
 [6]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/6.png
 [7]: http://blog.simplicitymedialtd.co.uk/wp-content/uploads/2013/05/7.png