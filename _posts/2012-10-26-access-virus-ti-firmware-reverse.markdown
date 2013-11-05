---
layout: post
title:  ACCESS VIRUS TI FIRMWARE – REVERSE ENGINEERING ATTEMPT #1
date:   2012-10-26 00:00:00
categories: general
coverimage: /img/covers/access_virus_ti_03.jpg
---

After several times of looking around on eBay for an Access Virus TI, and each time deciding that I didn't really have £800 to blow on a unit, I went in search of a firmware emulator. This drew a blank, so I decided to have a shot at poking into the firmware. I'd done this a few times before (mostly with phones and routers), but never with this. I didn't have an actual unit to look inside, so first I had to find some pictures and/or a hardware spec. 


### Lets get started

I am by no means an expert when it comes to this subject, so some information on this post may be incorrect. The tools used were Windows 7, IDA Pro, binwalk, Hex Workshop, various 563xx tools (see below) 

Luckily for me this work had already been done by the guys over at midibox: 

{% highlight text %}
* 2X Freescale 150mhz dspb56367ac150 DSP's (the nord lead 3 has 6x 120's)  
* 6x samsung k6r4008v10-ui10 memory chips,  
* A totally seperate keyboard controller with 4mhz pic (pic16c238-04/sp) - connected to virus thru midi !  
* lots of ne5532 opamps,  
* Somesort of ST electronics dsp (lettering unreadable) connected to a samsung kex400874e-uf70 memory chip,  
* Cirrus logic, one chip adc/dac cs12556-c31,  
* Texas Instruments tusb3200ac streaming usb controller,  
* Lots of White leds,  
* A white finish thats highly prone to shoing up dust, grime & scratches,  
* Very heavy aluminum end caps (at least it feels solid),  
* the front wooden bar is mdf with wooden vineer, lime ?  
* A 'trailing blob' psu -inside- the case,  
* a really dodgy looking power cap.. that looked ready to explode. &lt;/li>  
{% endhighlight %}

I had some difficulty finding an exact match for "dspb56367ac150", but we did find a DSP56367, which is part of the Motorola DSP 563xx Freescale family (24-bit @ 150mhz). Here is a link to the specification of this chip www.freescale.com/files/dsp/doc/data_sheet/DSP56367.pdf 

Extracting firmware from installation Next was to get hold of their latest firmware/software, which was a bit tricky. This involved signing up for an account on their website, confirming via email, then downloading the relevant software. In our case, we found the following file on their site; 

{% highlight text %}
* Virus TI Software Installer_v45300_x64.zip  
* Virus TI Software Installer 64-bit.msi  
* Virus TI Setup Guide.pdf  
{% endhighlight %}

After extracting the MSI with 7zip (no need to install), this gave us the following files; 

{% highlight text %}
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 AbletonLive6_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Atmosphere_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Attack01_12_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Attack13_24_vrt  
-rw-r--r-- 1 foxx foxx 66K Jan 13 2009 BackupTI2ROMA  
-rw-r--r-- 1 foxx foxx 66K Jan 13 2009 BackupTI2ROMB  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMC  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMD  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROME  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMF  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMG  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMH  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMI  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMJ  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMK  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROML  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMM  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMN  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMO  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMP  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMQ  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMR  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMS  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMT  
-rw-r--r-- 1 foxx foxx 66K Jan 8 2009 BackupTI2ROMU  
-rw-r--r-- 1 foxx foxx 66K Jan 19 2009 BackupTI2ROMV  
-rw-r--r-- 1 foxx foxx 66K Jan 19 2009 BackupTI2ROMW  
-rw-r--r-- 1 foxx foxx 66K Jan 19 2009 BackupTI2ROMX  
-rw-r--r-- 1 foxx foxx 66K Jan 19 2009 BackupTI2ROMY  
-rw-r--r-- 1 foxx foxx 66K Jan 19 2009 BackupTI2ROMZ  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMA  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMB  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMC  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMD  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROME  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMF  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMG  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMH  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMI  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMJ  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMK  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROML  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMM  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMN  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMO  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMP  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMQ  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMR  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTIROMS  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTISnowROMA  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTISnowROMB  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTISnowROMC  
-rw-r--r-- 1 foxx foxx 66K Oct 9 2008 BackupTISnowROMD  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 ca5000_vrt  
-rw-r--r-- 1 foxx foxx 508K May 11 2010 DIFXApiDll  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Discoveryv2_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 DrREX_BL_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 EMU_Proteus_2000_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Evolver_vrt  
-rw-r--r-- 1 foxx foxx 8.1M Oct 17 2011 firmware_bin  
-rw-r--r-- 1 foxx foxx 8.1M Oct 17 2011 firmware_bin64  
-rw-r--r-- 1 foxx foxx 298K Oct 14 2011 firmwareupdater_exe  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 hybrid_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 ImpOSCar_vrt  
-rw-r--r-- 1 foxx foxx 1.6M Oct 14 2011 installassist_exe  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Korg_MS20_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Korg_Polysix_vrt  
-rw-r--r-- 1 foxx foxx 1.9K Oct 9 2008 Live6RemoteInstall_rtf  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Malstrom_BL_vrt  
-rw-r--r-- 1 foxx foxx 2.2K Oct 9 2008 manual_ico  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 MiniMonsta_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Moog_Voyager_RME_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 NovationKSRack_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 NovationNova_vrt  
-rw-r--r-- 1 foxx foxx 20K Jan 8 2009 PAOS3FXDemo  
-rw-r--r-- 1 foxx foxx 30K Mar 23 2011 PAOS45FeaturesDemo  
-rw-r--r-- 1 foxx foxx 44K Feb 16 2010 PAOS4FeaturesDemo  
-rw-r--r-- 1 foxx foxx 6.8K Oct 9 2008 PATAtomizer  
-rw-r--r-- 1 foxx foxx 26 Oct 9 2008 PATMyPatches  
-rw-r--r-- 1 foxx foxx 17K Oct 9 2008 PATOS2Patches  
-rw-r--r-- 1 foxx foxx 17K Oct 9 2008 PATTutorial  
-rw-r--r-- 1 foxx foxx 16K Oct 9 2008 PAVocoderInput  
-rw-r--r-- 1 foxx foxx 704K Oct 9 2008 PDF_AbletonLiveTutorial  
-rw-r--r-- 1 foxx foxx 2.6M Oct 14 2011 PDF_Addendum  
-rw-r--r-- 1 foxx foxx 265K Mar 15 2011 PDF_Atomizer_Manual  
-rw-r--r-- 1 foxx foxx 103K Oct 14 2011 PDF_Changelog  
-rw-r--r-- 1 foxx foxx 756K Oct 9 2008 PDF_CubaseTutorial  
-rw-r--r-- 1 foxx foxx 1.1M Oct 9 2008 PDF_FLStudioTutorial  
-rw-r--r-- 1 foxx foxx 53K Mar 16 2011 PDF_LicenseAgreement  
-rw-r--r-- 1 foxx foxx 198K Oct 9 2008 PDF_Patchnames  
-rw-r--r-- 1 foxx foxx 260K Oct 9 2008 PDF_ProtoolsTutorial  
-rw-r--r-- 1 foxx foxx 49K Mar 15 2011 PDF_Readme_EN  
-rw-r--r-- 1 foxx foxx 4.5M Jul 28 2011 PDF_SonarTutorial  
-rw-r--r-- 1 foxx foxx 839K Oct 9 2008 PDF_TutorialProgramming  
-rw-r--r-- 1 foxx foxx 433K Oct 9 2008 PDF_TutorialVirusControl  
-rw-r--r-- 1 foxx foxx 2.4M Mar 15 2011 PDF_VirusSnow_Quickstart  
-rw-r--r-- 1 foxx foxx 1.8M Jan 6 2009 PDF_VirusSnow_Reference  
-rw-r--r-- 1 foxx foxx 2.2M Mar 15 2011 PDF_VirusTI_Quickstart  
-rw-r--r-- 1 foxx foxx 1.8M Mar 15 2011 PDF_VirusTI_Reference  
-rw-r--r-- 1 foxx foxx 609K Mar 15 2011 PDF_VirusTI_Setup_Guide  
-rw-r--r-- 1 foxx foxx 16K Oct 9 2008 PDF_Warranty_Card  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 PPGWave2V_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Pro_53_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 RolandJuno106_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 S_Bass_Station_vrt  
-rw-r--r-- 1 foxx foxx 330K Oct 9 2008 setup_cd_ico  
-rw-r--r-- 1 foxx foxx 2.3K Mar 17 2011 Sidstation_vrt  
-rw-r--r-- 1 foxx foxx 157K Mar 23 2011 SNG_AbletonLiveTutorialSong  
-rw-r--r-- 1 foxx foxx 104K Jun 17 2011 SNG_AbletonLiveTutorialSongSnow  
-rw-r--r-- 1 foxx foxx 143K Mar 23 2011 SNG_CubaseTutorial  
-rw-r--r-- 1 foxx foxx 116K Oct 9 2008 SNG_CubaseTutorialSnow  
-rw-r--r-- 1 foxx foxx 236K Jul 28 2011 SNG_FLStudioTutorialSong  
-rw-r--r-- 1 foxx foxx 169K Oct 9 2008 SNG_ProtoolsTutorialSong  
-rw-r--r-- 1 foxx foxx 159K Oct 9 2008 SNG_ProtoolsTutorialSongSnow  
-rw-r--r-- 1 foxx foxx 270K Jul 28 2011 SNG_SonarTutorialSong  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 strike_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Stylus_RMX_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Subtractor_BL_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 synchronic_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 TCMercury_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 The_Oddity_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Trilogy_vrt  
-rw-r--r-- 1 foxx foxx 3.3K Oct 9 2008 UserConfiguration_txt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 Vanguard_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 velvet_vrt  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 VirusABC_vrt  
-rw-r--r-- 1 foxx foxx 3.1M Oct 17 2011 viruscontrolcenter_exe  
-rw-r--r-- 1 foxx foxx 14M Oct 17 2011 viruscontrol_dll  
-rw-r--r-- 1 foxx foxx 14M Oct 17 2011 viruscontrol_dll64  
-rw-r--r-- 1 foxx foxx 565K Oct 14 2011 VirusControlPluginTISnowVST  
-rw-r--r-- 1 foxx foxx 157K Oct 14 2011 VirusControlPluginTISnowVST64  
-rw-r--r-- 1 foxx foxx 565K Oct 14 2011 VirusControlRTAS_TI_DPM  
-rw-r--r-- 1 foxx foxx 286 Oct 9 2008 VirusControlRTAS_TI_Res  
-rw-r--r-- 1 foxx foxx 565K Oct 14 2011 VirusControlVST3  
-rw-r--r-- 1 foxx foxx 157K Oct 14 2011 VirusControlVST364  
-rw-r--r-- 1 foxx foxx 27K Oct 9 2008 VirusTI_ctl_rmx  
-rw-r--r-- 1 foxx foxx 253K Oct 14 2011 VirusUpdaterDll  
-rw-r--r-- 1 foxx foxx 304K Oct 14 2011 VirusUpdaterDll64  
-rw-r--r-- 1 foxx foxx 7.9K May 27 2010 virususb_cat  
-rw-r--r-- 1 foxx foxx 221K May 27 2010 virususb_dll  
-rw-r--r-- 1 foxx foxx 1.9K May 27 2010 virususb_inf  
-rw-r--r-- 1 foxx foxx 458K May 27 2010 virususb_sys  
-rw-r--r-- 1 foxx foxx 243K May 27 2010 virususbx64_dll  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 V_Station_vrt  
-rw-r--r-- 1 foxx foxx 7.8K May 27 2010 vtiaudio_cat  
-rw-r--r-- 1 foxx foxx 3.6K May 27 2010 vtiaudio_inf  
-rw-r--r-- 1 foxx foxx 49K May 27 2010 vtiaudio_sys  
-rw-r--r-- 1 foxx foxx 7.9K May 11 2010 vtimidi_cat  
-rw-r--r-- 1 foxx foxx 4.3K May 11 2010 vtimidi_inf  
-rw-r--r-- 1 foxx foxx 32K May 11 2010 vtimidi_sys  
-rw-r--r-- 1 foxx foxx 2.3K Oct 9 2008 xpand_vrt  
{% endhighlight %}

Obviously, the file that drew our attention the most was firmware_bin64, so lets have a look at what our initial inspections show According to Google, IFF is basically an image format, so this is probably a false positive. 

{% highlight bash %}
$ file firmware_bin64  
firmware_bin64: IFF data  
{% endhighlight %}

Strings shows some interesting results, the fact we have a list of file names near the start means we're probably dealing with some sort of compressed archive or squashed file. 

{% highlight bash %}
$ strings firmware_bin64 | head -n10  
FORM  
QTABL  
2lcd_backup_000.bin  
lcd_backup_001.bin  
lcd_backup_002.bin  
lcd_backup_003.bin  
lcd_backup_004.bin  
lcd_backup_005.bin  
lcd_backup_006.bin  
lcd_backup_007.bin  
---| SNIPPED ---|  
{% endhighlight %}

Binwalk opcodes scan shows the binary might have an ARM bootloader somewhere in there, but this could be a false positive. 

{% highlight bash %}
$ binwalk -A firmware_bin64

DECIMAL HEX DESCRIPTION  
------------------------------------------------------------------------------------------------------|-  
534627 0x82863 ARM function prologue  
540298 0x83E8A ARMEB function epilogue  
541085 0x8419D ARMEB function epilogue  
548901 0x86025 ARM function epilogue  
567524 0x8A8E4 ARM function epilogue  
769219 0xBBCC3 ARMEB function epilogue  
797858 0xC2CA2 ARMEB function prologue  
842578 0xCDB52 ARM function epilogue  
847009 0xCECA1 ARM function epilogue  
2658496 0x2890C0 ARMEB function prologue  
2658531 0x2890E3 ARMEB function prologue  
2658566 0x289106 ARMEB function prologue  
2658601 0x289129 ARMEB function prologue  
2658636 0x28914C ARMEB function prologue  
2658671 0x28916F ARMEB function prologue  
2658706 0x289192 ARMEB function prologue  
2658741 0x2891B5 ARMEB function prologue  
3904543 0x3B941F ARM function prologue  
3910214 0x3BAA46 ARMEB function epilogue  
3911001 0x3BAD59 ARMEB function epilogue  
3918817 0x3BCBE1 ARM function epilogue  
3937440 0x3C14A0 ARM function epilogue  
4139135 0x3F287F ARMEB function epilogue  
4167774 0x3F985E ARMEB function prologue  
4212494 0x40470E ARM function epilogue  
4216925 0x40585D ARM function epilogue  
6167275 0x5E1AEB ARM function prologue  
6176235 0x5E3DEB ARM function prologue  
6185195 0x5E60EB ARM function prologue  
6194155 0x5E83EB ARM function prologue  
7453605 0x71BBA5 ARM function prologue  
7459276 0x71D1CC ARMEB function epilogue  
7460063 0x71D4DF ARMEB function epilogue  
7467879 0x71F367 ARM function epilogue  
7486502 0x723C26 ARM function epilogue  
7687954 0x754F12 ARMEB function epilogue  
7716593 0x75BEF1 ARMEB function prologue  
7765801 0x767F29 ARM function epilogue  
{% endhighlight %}

Binwalk normal scan shows a lot of LZMA data, but this looks to be mostly false positives: 

{% highlight python %}
$ binwalk firmware_bin64 | head -n10

DECIMAL HEX DESCRIPTION  
------------------------------------------------------------------------------------------------------|-  
146122 0x23ACA LZMA compressed data, properties: 0x90, dictionary size: 50331648 bytes, uncompressed size: 49186 bytes  
369588 0x5A3B4 LZMA compressed data, properties: 0xD0, dictionary size: 1074331648 bytes, uncompressed size: 160 bytes  
369727 0x5A43F LZMA compressed data, properties: 0xD0, dictionary size: 150994944 bytes, uncompressed size: 8257 bytes  
372248 0x5AE18 LZMA compressed data, properties: 0xD3, dictionary size: 1242103808 bytes, uncompressed size: 32 bytes  
372317 0x5AE5D LZMA compressed data, properties: 0xD3, dictionary size: 150994944 bytes, uncompressed size: 24650 bytes  
582498 0x8E362 LZMA compressed data, properties: 0x84, dictionary size: 553648128 bytes, uncompressed size: 210 bytes  
582840 0x8E4B8 LZMA compressed data, properties: 0x84, dictionary size: 553648128 bytes, uncompressed size: 213 bytes  
{% endhighlight %}

A further binwalk scan shows the presence of a JFFS2 filesystem and a PNG image. 

{% highlight python %}
$ binwalk firmware_bin64 | grep -v LZMA

DECIMAL HEX DESCRIPTION  
------------------------------------------------------------------------------------------------------|-  
3214531 0x310CC3 JFFS2 filesystem (old) data big endian, JFFS node length: 39  
8385066 0x7FF22A PNG image, 21 x 21, 8-bit/color RGBA, non-interlaced  
{% endhighlight %}

When we attempted to extract and mount the JFFS, this ended with failure. Upon inspecting the extracted data with file and binwalk, it would appear that this is also a false positive. 

{% highlight bash %}
$ dd if=firmware_bin64 bs=1 skip=3214531 of=1.jffs  
5174422+0 records in  
5174422+0 records out  
5174422 bytes (5.2 MB) copied, 5.18494 s, 998 kB/s

$ sudo mount -t jffs2 1.jffs lol  
mount: 1.jffs is not a block device (maybe try `-o loop'?)

$ sudo mount -o loop -t jffs2 1.jffs lol  
mount: wrong fs type, bad option, bad superblock on /dev/loop0,  
missing codepage or helper program, or other error  
In some cases useful info is found in syslog - try  
dmesg | tail or so

$ file 1.jffs  
1.jffs: data

$ binwalk 1.jffs | grep -v LZMA

DECIMAL HEX DESCRIPTION  
------------------------------------------------------------------------------------------------------|-  
0 0x0 JFFS2 filesystem (old) data big endian, JFFS node length: 39  
{% endhighlight %}

Unpacking firmware So next we take a look at the firmware image inside a hex editor, and see what is going on. 

[![access-virus-1.png](/img/postcontent/access-virus-1.png)](/img/postcontent/access-virus-1.png)


{% highlight text %}
1. size of the file list data chunk (03AE hex = 942)  
2. list of files (50 to be exact), separated out by a null byte (\x00): 941 bytes + 1 byte separator  
3. file number chunk + null byte (\x00) separator: starts at 0001  
4. Header identifier of some sort  
{% endhighlight %}

The way we found out that (3) was a file number chunk, was by converting the ASCII string "0001" through to "0050", adding a null byte, then searching in our hex editor (example: 3030 3439 00 = 0049.) Every time we searched, we were able to find a match, followed by what looked like readable information, such as: 

{% highlight text %}
0047......<head>
  .<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  .<titl 
{% endhighlight %}

{% highlight text %}
`0050....@charset "UTF-8";..VirusControlStyles {.}.p {..font-family: Geneva, Arial, Helvetica, sans-serif;..font-size: 12px;..font-style: normal;..font-weight: normal;..font-variant: normal;..text-transform: none;..color: #FFFFFF;.}.h1 {..font-family: Genev  
{% endhighlight %}
  
Problem now is that we don't seem to have any chunk sizes for each file, and we still need to ensure this theory is correct. So a quick and dirty python script does the following:

{% highlight text %}
* Jump to the end of the header identifier  
* Grab the size of the file list data chunk  
* Extract file list data chunk  
* Iterate over file list (increment from 1, zfill 4 positions with zeros, so 1 becomes 0001)  
* Scan the firmware for 0001~0050 followed by null byte

# 1st col = hex representation of the first 4 bytes of data (file number chunk)  
# 2nd col = seperator on the 5th byte (should always be null)  
# 3rd col = hex representation of bytes range 5~10  
# 4th col - ascii representation of bytes range 5~10

$ extract1.py  
30303031 00 0002800000 0001  
30303032 00 0002800000 0002  
30303033 00 0002800000 0003  
30303034 00 0002800000 0004  
30303035 00 0002800000 0005  
30303036 00 0002800000 0006  
30303037 00 0002800000 0007  
30303038 00 0002800000 0008  
30303039 00 0002800000 0009  
30303130 00 0002800000 0010  
30303131 00 0002800000 0011  
30303132 00 0002800000 0012  
30303133 00 0002800000 0013  
30303134 00 0002800000 0014  
30303135 00 0002800000 0015  
30303136 00 0002800000 0016  
30303137 00 0002800000 0017  
30303138 00 0002800000 0018  
30303139 00 0002800000 0019  
30303230 00 0002800000 0020  
30303231 00 0002800000 0021  
30303232 00 0002800000 0022  
30303233 00 0002800000 0023  
30303234 00 0002800000 0024  
30303235 00 0002800000 0025  
30303236 00 0002800000 0026  
30303237 00 0002800000 0027  
30303238 00 0002800000 0028  
30303239 00 0002800000 0029  
30303330 00 0002800000 0030  
30303331 00 0002800000 0031  
30303332 00 0002800000 0032  
30303333 00 0002800000 0033  
30303334 00 0002800000 0034  
30303335 00 0002800000 0035  
30303336 00 0002800000 0036  
30303337 00 0002800000 0037  
30303338 00 0002800000 0038  
30303339 00 0002800000 0039  
30303430 00 0002800000 0040  
30303431 00 0002800000 0041  
30303432 00 0002800000 0042  
30303433 00 0002800000 0043  
30303434 00 2f0b64464f 0044/  
dFO  
30303435 00 336b4c464f 00453kLFO  
30303436 00 1cfe1a464f 0046þFO  
30303437 00 0006813c21 0047&lt;!  
30303438 00 0006193c21 0048&lt;!  
§P303439 00 000da78950 0049  
30303530 00 0001804063 0050@c  
{% endhighlight %}
  
  
So we now extract one of these files manually with our hex editor, and see what happens. To find our end chunk size, we simply look ahead at the next chunk, find its start position, offset by -1 byte, and we're all clear. (i.e. start at the ASCII position of 0001\x00, and extract everything before ASCII position 0002\x00).

There is a HTML and CSS which extracted without problem, however we can see that the PNG doesn't seem to work. If we compare the first 10 bytes of our PNG, with our random test PNG, we can see that we've got some extra bytes at the start.

Lets look at this a bit closer.. We have a null byte at the start, but we are then left with two inconsistently changing numbers. If we convert 0DA7 - we get 3495. Our output file is 3498, if we minus off the length of these extra bytes, these two numbers are exactly the same. This means that we are actually extracting 3 bytes too many, and that we didn't really need to use the look ahead method mentioned earlier.. but hey-ho!
  
{% highlight text %}  
# BTN_Help.png  
000DA789504E470D0A1A0A = ....PNG....

# RANDOM PNG  
89504E470D0A1A0A000000 = .PNG.......

# EXTRA DATA (3 bytes at the start of BTN_Help.png)  
00 0D A7  
{% endhighlight %}
  
So, now we have our approach fine tuned, we attempt to extract all the chunks into individual files for easier analysis, using the above as a template. As you can see, the ASIZE/CSIZE are both matching (which means we are extracting the expected size). along with the original byte offsets and file names etc. This script also dumps the files out to disk for us.

{% highlight bash %}
# FNO = file chunk number (4x zero padded)  
# FNAME = original filename from file list  
# SPOS = start position in bytes on the original firmware file  
# FSPOS = file start position (this is where the actual file starts)  
# EPOS = end position in bytes (this is where the actual file ends)  
# ASIZE = size of extracted chunk  
# CSIZE = size expected by the firmware

$ python extract2.py  
FNO FNAME SPOS FSPOS EPOS ASIZE/CSIZE  
0001 lcd_backup_000.bin 958 966 1606 640/640  
0002 lcd_backup_001.bin 1606 1614 2254 640/640  
0003 lcd_backup_002.bin 2254 2262 2902 640/640  
0004 lcd_backup_003.bin 2902 2910 3550 640/640  
0005 lcd_backup_004.bin 3550 3558 4198 640/640  
0006 lcd_backup_005.bin 4198 4206 4846 640/640  
0007 lcd_backup_006.bin 4846 4854 5494 640/640  
0008 lcd_backup_007.bin 5494 5502 6142 640/640  
0009 lcd_backup_008.bin 6142 6150 6790 640/640  
0010 lcd_backup_009.bin 6790 6798 7438 640/640  
0011 lcd_configuring_000.bin 7438 7446 8086 640/640  
0012 lcd_configuring_001.bin 8086 8094 8734 640/640  
0013 lcd_connected_000.bin 8734 8742 9382 640/640  
0014 lcd_flashrom_000.bin 9382 9390 10030 640/640  
0015 lcd_flashrom_001.bin 10030 10038 10678 640/640  
0016 lcd_flashrom_002.bin 10678 10686 11326 640/640  
0017 lcd_flashrom_003.bin 11326 11334 11974 640/640  
0018 lcd_flashrom_004.bin 11974 11982 12622 640/640  
0019 lcd_flashrom_005.bin 12622 12630 13270 640/640  
0020 lcd_flashrom_006.bin 13270 13278 13918 640/640  
0021 lcd_flashrom_007.bin 13918 13926 14566 640/640  
0022 lcd_flashrom_008.bin 14566 14574 15214 640/640  
0023 lcd_flashrom_009.bin 15214 15222 15862 640/640  
0024 lcd_restore_000.bin 15862 15870 16510 640/640  
0025 lcd_restore_001.bin 16510 16518 17158 640/640  
0026 lcd_restore_002.bin 17158 17166 17806 640/640  
0027 lcd_restore_003.bin 17806 17814 18454 640/640  
0028 lcd_restore_004.bin 18454 18462 19102 640/640  
0029 lcd_restore_005.bin 19102 19110 19750 640/640  
0030 lcd_restore_006.bin 19750 19758 20398 640/640  
0031 lcd_restore_007.bin 20398 20406 21046 640/640  
0032 lcd_restore_008.bin 21046 21054 21694 640/640  
0033 lcd_restore_009.bin 21694 21702 22342 640/640  
0034 lcd_update_000.bin 22342 22350 22990 640/640  
0035 lcd_update_001.bin 22990 22998 23638 640/640  
0036 lcd_update_002.bin 23638 23646 24286 640/640  
0037 lcd_update_003.bin 24286 24294 24934 640/640  
0038 lcd_update_004.bin 24934 24942 25582 640/640  
0039 lcd_update_005.bin 25582 25590 26230 640/640  
0040 lcd_update_006.bin 26230 26238 26878 640/640  
0041 lcd_update_007.bin 26878 26886 27526 640/640  
0042 lcd_update_008.bin 27526 27534 28174 640/640  
0043 lcd_update_009.bin 28174 28182 28822 640/640  
0044 vti.bin 28822 28830 3111938 3083108/3083108  
0045 vti_2.bin 3111938 3111946 6481750 3369804/3369804  
0046 vti_snow.bin 6481750 6481758 8381816 1900058/1900058  
0047 Changes.htm 8381816 8381824 8383489 1665/1665  
0048 Welcome.htm 8383489 8383497 8385058 1561/1561  
0049 BTN_Help.png 8385058 8385066 8388561 3495/3495  
0050 vcstyles.css 8388561 8388569 8388953 384/384

{% endhighlight %}
  
  
Final sanity check, ensure the file size is correct on disk

{% highlight bash %}
$ python  
>>> import os  
>>> os.path.getsize("vcstyles.css")  
384

$ md5sum *  
e20091f333f03e495e52ee731e5d0251 BTN_Help.png  
d3d5da69f3eccba4126a5fa710ccfa2f Changes.htm  
97a76e68e1de1654f2b1320e4a0b6e84 lcd_backup_000.bin  
d4ef509624dae64181b23e0e01187052 lcd_backup_001.bin  
355410fc102e05dedd61bf2f0592418c lcd_backup_002.bin  
ffdd2d0792fbe02a6273cbe3817a2a5f lcd_backup_003.bin  
be983cae6ec12e91e023035460e8a129 lcd_backup_004.bin  
0528136dc4588f0681793f33cee3048c lcd_backup_005.bin  
be983cae6ec12e91e023035460e8a129 lcd_backup_006.bin  
ffdd2d0792fbe02a6273cbe3817a2a5f lcd_backup_007.bin  
355410fc102e05dedd61bf2f0592418c lcd_backup_008.bin  
d4ef509624dae64181b23e0e01187052 lcd_backup_009.bin  
4e4e156b3557c7d37af87392ade02caa lcd_configuring_000.bin  
c9c2c001b364f84253b487bd829342d6 lcd_configuring_001.bin  
4fecca5121a63263b528bab8e2bd3057 lcd_connected_000.bin  
3e05e54772a2344af42f23979bab326a lcd_flashrom_000.bin  
7e39a047fe8b8ba2eeea81cb0c63dee0 lcd_flashrom_001.bin  
d501c1230ba521369a458c6a17c39c57 lcd_flashrom_002.bin  
3a9afc8705ae649f35fd22ed6eadc47d lcd_flashrom_003.bin  
9eff0d5ccd3d967c1ed0df75f779193f lcd_flashrom_004.bin  
097b4f97ee0f865ed93cb9a36a2842d2 lcd_flashrom_005.bin  
9eff0d5ccd3d967c1ed0df75f779193f lcd_flashrom_006.bin  
3a9afc8705ae649f35fd22ed6eadc47d lcd_flashrom_007.bin  
d501c1230ba521369a458c6a17c39c57 lcd_flashrom_008.bin  
7e39a047fe8b8ba2eeea81cb0c63dee0 lcd_flashrom_009.bin  
c9f824f89e6e3e919a51cf65566479a0 lcd_restore_000.bin  
877b348505e59c682ce7a7d7d658f748 lcd_restore_001.bin  
f8d5aff898f14b4a53ebbc29b2fc3d51 lcd_restore_002.bin  
9c55fd905edd92ba77e688f6559d53f4 lcd_restore_003.bin  
4e7d756df9224208203aa6643fe4d85a lcd_restore_004.bin  
12df5f74f4f1b6e7b71fe461cfd8ccf7 lcd_restore_005.bin  
4e7d756df9224208203aa6643fe4d85a lcd_restore_006.bin  
9c55fd905edd92ba77e688f6559d53f4 lcd_restore_007.bin  
f8d5aff898f14b4a53ebbc29b2fc3d51 lcd_restore_008.bin  
877b348505e59c682ce7a7d7d658f748 lcd_restore_009.bin  
9b0d9a6b8a5e421ce7c95d4c52b32d2c lcd_update_000.bin  
45c7c20c28280952bd2e4dad0b8685b6 lcd_update_001.bin  
0e7535b55402ff72e438cdf8bb3f5e7c lcd_update_002.bin  
32a75edea33fddc4b0acd5a41d7b5eb8 lcd_update_003.bin  
e8727a2ba970e0bec88eaf947a848f1d lcd_update_004.bin  
7b28e713a7d370e6efbd4a822fb98670 lcd_update_005.bin  
e8727a2ba970e0bec88eaf947a848f1d lcd_update_006.bin  
32a75edea33fddc4b0acd5a41d7b5eb8 lcd_update_007.bin  
0e7535b55402ff72e438cdf8bb3f5e7c lcd_update_008.bin  
45c7c20c28280952bd2e4dad0b8685b6 lcd_update_009.bin  
0ba15401101f1526327e2fc5edc52822 vcstyles.css  
862b0d7c974a7d181d9342fe01b92715 vti_2.bin  
9acb16f3b96866163e3a95333cb1508e vti.bin  
d759e649c1f01bcf4fdec867bfec7b04 vti_snow.bin  
c0b8abe212b623bd58831b3800afe738 Welcome.htm  
{% endhighlight %}
  
  
Another quick test, and we can see the PNG now loads - woo! For shits and giggles, here it is: 

[![access-virus-2.png](/img/postcontent/access-virus-2.png)](/img/postcontent/access-virus-2.png)
  
If anyone is interested, here is the full working code used to extract the firmware chunks:
  
{% highlight python %}  
import os
import sys


# temp assign

_files = {}

import binascii

class sstr(str):
    def index_end(self, substring, *args, **kwargs):
        res = super(sstr, self).index(substring, *args, **kwargs)
        return res + len(substring)

class FirmwareScan(object):
    def __init__(self, file):
        self.file = file
        self.filelist = {}

    def prep(self):
        self.data = sstr(open(self.file, 'rb').read())
        self._build_filelist()

    def _find_file_position(self, fnum):
        k = "%sx00" % ( str(fnum).zfill(4), )
        _total_found = self.data.count(k)
        assert not _total_found == 0, "unable to find file chunk - %s" % ( k, )
        assert not _total_found > 1 , "duplicate file chunks - %s" % ( k, )
        return self.data.index(k)

    def _build_filelist(self):
        # find our file list offsets
        _fl_start = self.data.index_end("x51x54x41x42x4Cx00x00")
        _fl_end = self.data.index("x32", _fl_start)

        # find our file list size offset
        _d = self.data[_fl_start:_fl_end]

        # calculate the filelist size
        _fl_size = int(binascii.hexlify(_d), 16)

        # extract filelist (small amount of manual offsetting)
        _fl_data = self.data[_fl_end+1:][:_fl_size-1].split("x00")
        _fl_data = filter(lambda x: x, _fl_data)

        # define the file number range
        _start_fnum = 1
        _end_fnum = len(_fl_data)+1

        _str = "%(fileno)-6s %(filename)-30s %(start_pos)-10s %(chunk_start)-10s %(end_pos)-10s %(size)s/%(calc_size)s"
            print _str % {
            'fileno' : "File Num",
            'filename' : "File Name",
            'start_pos' : 'SPOS',
            'chunk_start' : 'CSPOS',
            'end_pos' : 'EPOS',
            'size' : 'Actual Size',
            'calc_size' : 'Chunk Size'
        }
                
        # now build the filelist
        for x in xrange(_start_fnum, _end_fnum):
            _start_pos = self._find_file_position(x)
            if not x == _end_fnum-1:
                _end_pos = self._find_file_position(x+1)
            else:
                _end_pos = len(self.data)
    
            _filename = _fl_data[x-1]
            _f_size = int(binascii.hexlify(self.data[_start_pos:][5:8]), 16)
    
            _chunk_start = _start_pos + 8
            
            self.filelist[x] = {
                'start_pos' : _start_pos,
                'chunk_start' : _chunk_start,
                'end_pos' : _end_pos,
                'filename' : _filename,
                'size' : _f_size,
                'calc_size' : _end_pos - _chunk_start,
                'fileno' : str(x).zfill(4),
            }
            
            print _str % self.filelist[x]
            
            continue

            #print binascii.hexlify(self.data[_start_pos:][:4]),binascii.hexlify(self.data[_start_pos:][4]), binascii.hexlify(self.data[_start_pos:][5:10]), self.data[_start_pos:][:10]


        def dump_to_disk(self, out):
            for k,v in self.filelist.iteritems():
                _start_pos = v.get('start_pos')
                _end_pos = v.get('end_pos')
                # extract data after 5 bytes
                fname = "%s/%s" % ( out, v.get('filename'), )
                f = open(fname, "wb")
                _chunk = self.data[_start_pos+5 : _end_pos]
                f.write(_chunk)
                f.close()
                print " - written %s (%s bytes)" % ( fname, os.path.getsize(fname), )
            
a = FirmwareScan(
    file = "../firmware_bin64"
)

a.prep()
"""a.dump_to_disk(
out = "/home/foxx/development/virusti/out"
)"""
{% endhighlight %}
    

### Analysing the firmware  

Really the files we are most interested in at vti.bin, vti_2.bin and vti_snow.bin. Obviously, there are 3 different types of Access Virus that this firmware applies to: TI, TI2 and TI Snow. So, lets start digging into those files. Again, we see more IFF headers, which is really strange, but it could mean that these extracted files also have some sort of packing on them.

{% highlight bash %}  
$ file vti.bin  
vti.bin: IFF data

$ file vti_2.bin  
vti_2.bin: IFF data

$ file vti_snow.bin  
vti_snow.bin: IFF data

# VTI.BIN - first 10 bytes  
46 4F 52 4D 00 2F 0B 5C 46 30 30 30 00 00 8C 02 00 = FORM./.\F000.....

# firmware_bin64 - first 10 bytes  
46 4F 52 4D 00 80 01 51 54 41 42 4C 00 00 03 AE 32 = FORM...QTABL....2

{% endhighlight %}
  
Here is what happens if we jump ahead 10 bytes (or increment +1 byte each time), then run file against the extracted segment. As you can see, we didn't have any luck.
  
{% highlight bash %}
$ dd if=vti.bin bs=1 skip=1 > /tmp/1 && file /tmp/1  
/tmp/1: data

$ dd if=vti.bin bs=1 skip=12 > /tmp/1 && file /tmp/1  
/tmp/1: data

-- repeated skip 1~12, same results each time. Binwalk also showed up nothing --  
{% endhighlight %}
  
Okay so, file/binwalk doesn't appear to be finding anything, how about IDA pro? Make sure you set your CPU to "Motorola DSP 5600x: dsp563xx".
  
[![access-virus-3.png](/img/postcontent/access-virus-3.png)](/img/postcontent/access-virus-3.png)
  
We're going to try loading in 3 different variations of vti.bin. If we offset the file by 5 bytes (in our case, we deleted them manually via hex editor), IDApro seems to now recognise the file! At this point, it doesn't know how to identify the entry point, but it now shows the assembly within the ROM.
  
  
  

{% highlight bash %}
vti.bin = no offset = FAILURE  
vti-edit2.bin = offset first 10 bytes = FAILURE  
vti-edit.bin = offset first 5 bytes = SUCCESS  
{% endhighlight %}

[![access-virus-4.png](/img/postcontent/access-virus-4.png)](/img/postcontent/access-virus-4.png)

[![access-virus-5.png](/img/postcontent/access-virus-5.png)](/img/postcontent/access-virus-5.png)
  
I then tried using the following tools:
  
* "DSP56xxx Toolchain v3.6r1" from Tasking. (TASKING_DSP56k_v3.6r4.exe)
  http://www.tasking.com/forms/trial/download-dsp56xxx.shtml

* Suite56™ DSP Simulator
  http://styles.freescale.com/lgfiles/updates/Suite56/DSP56300_Tools.exe

* Freescale DSPS56SIMUM docs
  http://cache.freescale.com/files/dsp/doc/user_guide/DSPS56SIMUM.pdf

* DSP56xxx v3.6 C Cross-Compiler User Guide
  http://www.tasking.com/support/dsp56xxx/m_c56.pdf

All of those tools looked great, and would probably get us digging deeper into the firmware..... However due to my my lack of embedded development / assembly, this was the end of the line for me. Maybe one day I will look back at this once I'm a little more clued up about assembly.. Hopefully this post will be useful to others!
  