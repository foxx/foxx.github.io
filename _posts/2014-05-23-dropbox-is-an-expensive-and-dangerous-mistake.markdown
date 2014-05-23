---
layout: post
title:  DropBox is a dangerous and expensive mistake
date:   2014-05-23 00:00:00
categories: general
coverimage: /img/covers/nope1.jpg
type: small
weight: 19
---

Our requirements were quite simple, we wanted a cloud storage system that could store sensitive files, such as tax returns, accountancy and personal family albums.

### BoxCryptor is not safe

DropBox is an established brand with multiple device support and good pricing. However they have suffered with multiple security problems over the years, such as making [passwords optional (?!)](http://techcrunch.com/2011/06/20/dropbox-security-bug-made-passwords-optional-for-four-hours/) and [others](https://www.google.co.uk/search?q=dropbox+password+hack).

Although [BoxCryptor](https://www.boxcryptor.com/) offers client side encryption for the big cloud providers, their client application is extremely buggy (at least on Windows 7) if you're dealing with more than a few hundred files. Not only was it slow, we also suffered with [file corruption](https://www.google.co.uk/search?q=boxcryptor+file+corruption) which caused the entire contents of the file to be replaced with null bytes. The mounted drive would also show files/folders as randomly missing, later returning if logout and login.

### TrueCrypt inside DropBox is not safe

The plan was to use [TrueCrypt inside DropBox](http://www.cloudwards.net/the-ultimate-guide-to-using-truecrypt-for-dropbox/) for the sensitive data, and skip using encryption for the less sensitive things. The container was several GB in size, and requires block level sync so you don't have to upload the entire file on every change. DropBox supports this [feature](http://serverfault.com/questions/52861/how-does-dropbox-version-upload-large-files), however other popular providers such as [Google Drive](https://drive.google.com/), [OneDrive](https://onedrive.live.com/about/en-gb/) and [Box](https://www.box.com/) do not. However storing a TrueCrypt container on DropBox increases the risk of sync conflicts, and concerns regarding [cryptanalysis](http://www.truecrypt.org/docs/volume-clones#) by analysing container revisions. 

This approach also requires you to classify files as either sensitive or unsensitive, requiring each file to be reviewed and still susceptable to human error. For example, nudity accidently slipping through the net in your photo albums imported from a camera. Or forgetting to remove a file permently after it was accidently uploaded.


### DropBox is fundementally unsafe

The concept of storing unencrypted data in the cloud is not just a potentially expensive mistake, it's also a dangerous one that is changing our perception of privacy. You shouldn't need to give up security for the sake of durability or accessibility.

### Client side encryption should be standard

For cloud storage to be secure, you need [client side encryption](http://wuala.com/en/learn/technology). In simple terms, this encrypts your data before transit, and ensures that files cannot be decrypted without the key. However, this introduces a whole new problem called [key management](https://spideroak.com/privacypost/cloud-security/secure-encryption-key-management-in-the-cloud/).

There are a few providers which offer this service, and even some in-depth comparisons by [lifehacker](http://lifehacker.com/the-best-cloud-storage-services-that-protect-your-priva-729639300).

Here are the three that stand out the most;

* [tresorit.com](https://tresorit.com/)

  This has been in private beta since [2011](http://en.wikipedia.org/wiki/Tresorit), and was released to general public in April 2014. The lack of maturity does scare me a little bit, and their client is not open sourced, so it's unclear if the encryption is flawed. However they plan on releasing this code in the near future (confirmed via telephone, no article found). Their data is physically stored in the EU. They also don't support two factor yet.

* [spideroak.com](https://spideroak.com/)

  These guys have been around since [2007](http://en.wikipedia.org/wiki/SpiderOak), and seem to have a decent level of maturity. Sadly their client is not open source either, but they plan to do so in the [near future](https://spideroak.com/faq/questions/35/why_isnt_spideroak_open_source_yet_when_will_it_be/).

* [wuala.com](http://wuala.com/)

  Been around since [2008](http://en.wikipedia.org/wiki/Wuala), good maturity but again their client is not open source.

I'm going to review these providers over the next few weeks, and do a seperate post about them.
