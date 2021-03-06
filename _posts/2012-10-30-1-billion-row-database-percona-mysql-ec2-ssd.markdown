---
layout: post
title:  1.1 billion row 160GB Percona MySQL DB on EC2 with RAID 1 SSD1
date:   2012-10-30 00:00:00
categories: general
coverimage: /img/covers/billion-row-db.png
weight: 17
type: small
keywords: mysql, percona, innodb, billions, ec2, ssd
desc: Scaling to billions of rows using EC2, SSD and Percona MySQL with InnoDB
---

So today, we broke our hosting companies record.. 1.1 billion rows in a Percona MySQL InnoDB table! Sounds impressive, but reality soon kicks in when you can't run SELECT() queries against it for fear of saturating our poor SAS disks and locking up the web application. And even harder when you're working against the clock on deadlines. With a total datadir size of around 160GB, 1,159,945,113 rows in a single table and no long term NoSQL plans on the horizon, our immediate options were limited. 

The affected database servers were limited to just 300 IOPS over SAS RAID 1, of which the disk IO showed a cool and steady 99.95% average IO utilization for a 24 hour period. So in a small moment of caffeine fueled epiphany, we fired up the biggest bad ass EC2 instance possible (hi1.4xlarge), this is where things started to get fun. 

For those of you that don't know about the hi1.4xlarge specs, let me fill you in; 

*   8 virtual cores, clocking in at a total of 35 ECU (EC2 Compute Units).
*   60.5 GB of RAM.
*   10 Gigabit Ethernet connectivity
*   2 TB of local SSD-backed storage, visible to you as a pair of 1 TB volumes.
*   120,000 random read IOPS (theoretical 240,000 IOPS in RAID 1) 

Wait.. what? 240 *THOUSAND* IOPS? I thought "no, it's gotta be a typo", the last time I played with SSDs, the floor limit was around 4k IOPS. 
After firing up a few tests, I damn near came when I saw the results scrolling by in my putty window. 

{% highlight text %}
$ cat /proc/mdstat
[=>...................]  resync =  5.1% (54948740/1073610560) finish=30.4min speed=557191K/sec 
[=>...................]  resync =  5.3% (57746260/1073610560) finish=30.0min speed=563297K/sec 

$ spew --write -r 1000M /mnt/ssd/test.1000mb
WTR:   107042.42 KiB/s   Transfer time: 00:00:09    IOPS:   214084.84

$ spew -g /mnt/ssd/5000mb lol.txt
Total write transfer time (WTT):          00:00:45
Total write transfer rate (WTR):   112676.70 KiB/s
Total write IOPS:                  225353.40 IOPS

$ spew --read -r 1000mb /mnt/ssd/lol.txt
RTR:   327998.76 KiB/s   Transfer time: 00:00:03    IOPS:   655997.52

$ spew --read 1000mb /mnt/ssd/lol.txt
RTR:   381131.60 KiB/s   Transfer time: 00:00:02    IOPS:   762263.21

{% endhighlight %} 

After being recommended to give 'ioping' tool a try, I re-ran these tests and sadly the numbers were not as exciting; 

{% highlight text %}
$ ioping /dev/md0 -R

--- /dev/md0 (device 1023.9 Gb) ioping statistics ---
8592 requests completed in 3000.2 ms, 4343 iops, 17.0 mb/s
min/avg/max/mdev = 0.1/0.2/0.3/0.0 ms


$ ioping -R /dev/xvdf

--- /dev/xvdf (device 1024.0 Gb) ioping statistics ---
8644 requests completed in 3000.3 ms, 4369 iops, 17.1 mb/s
min/avg/max/mdev = 0.1/0.2/0.3/0.0 ms

$ ioping -R /dev/xvdg

--- /dev/xvdg (device 1024.0 Gb) ioping statistics ---
8331 requests completed in 3000.3 ms, 4133 iops, 16.1 mb/s
min/avg/max/mdev = 0.1/0.2/0.4/0.0 ms

$ ioping -L /dev/md0
262144 bytes from /dev/md0 (device 1023.9 Gb): request=1 time=0.1 ms
262144 bytes from /dev/md0 (device 1023.9 Gb): request=2 time=1.4 ms
262144 bytes from /dev/md0 (device 1023.9 Gb): request=3 time=1.2 ms
262144 bytes from /dev/md0 (device 1023.9 Gb): request=4 time=1.3 ms
^C
--- /dev/md0 (device 1023.9 Gb) ioping statistics ---
4 requests completed in 3376.8 ms, 1007 iops, 251.6 mb/s
min/avg/max/mdev = 0.1/1.0/1.4/0.5 ms

$ ioping -L /dev/md0 -R

--- /dev/md0 (device 1023.9 Gb) ioping statistics ---
2950 requests completed in 3000.6 ms, 1178 iops, 294.5 mb/s
min/avg/max/mdev = 0.1/0.8/2.4/0.1 ms

{% endhighlight %} So for shits and giggles, I thought I'd see if I could max out the supposedly 10Gbit switch port - although finding a test file that would allow download at full 10gbit line speed proved extremely difficult. Eventually we found leaseweb mirrors, but even with 32 threads we only peaked at around 201mb/sec. (2gbit). 

{% highlight text %}
$ axel "http://mirror.us.leaseweb.net/speedtest/10000mb.bin"
Downloaded 4273.0 megabytes in 35 seconds. (124459.79 KB/s)
Downloaded 953.7 megabytes in 8 seconds. (110156.90 KB/s)
{% endhighlight %}

By this point I was having more fun with a server that costs 3 bucks an hour, than I ever could have done with a $500/hour high-class hooker on a Friday night. 

To get the most performance possible, I used the following approach; 

{% highlight text %}
$ mdadm --create /dev/md0 --level=1 --raid-disks=2 /dev/xvdf /dev/xvdg
$ echo "60000000" >  /proc/sys/dev/raid/speed_limit_min
$ echo "60000000" >  /proc/sys/dev/raid/speed_limit_max
$ mkfs.ext4 /dev/md0
$ mount /dev/md0 /mnt/ssd -o defaults,noatime,nobarrier,barrier=0
{% endhighlight %} 

After a few hours of pure geek heaven, I calmed down and started thinking how we could overcome a few stumbling blocks; 

*   If the instance is stopped, any data on the SSDs is discarded and it takes several hours to reload from EBS.
*   The server was not part of the managed hosting platform, and thus couldn't be used directly in production code or use any live replication.
*   EC2 SSDs were not automatically placed into RAID 1 (they are a pair of 1TB drives), and require initial sync time.
*   All queries on the EC2 instance would have to be ran as one-off scripts, and couldn't be sanely implemented into our existing code base at this stage.
*   The effective data was split over two existing databases, and merging them would be troublesome So we took an LVM snapshot of databases and started to copy the datadir's to EC2.. And this is where the fun started to turn into a nightmare of 70+ hours work. 

Whilst attempting to resolve a transfer speed problem with the networks team, one of the firewalls locked up. I almost choked on my tea as I saw the 93796434 alarms flood my mailbox. This lasted several (very long) minutes, and once the fail over kicked in we decided to leave it until monday and settle for 10MB/sec. Now, I'm not an impatient kinda guy, but this was like driving a Austin Metro after just having a test drive in a Lamborghini. Patiently, I sit and watch the rsync progress meter get closer and closer, teasing me with its damn fluxuating average speed. 

{% highlight text %}
  3211001856   2%    4.63MB/s    8:22:12
  4918378496   3%    5.72MB/s    6:41:37
  4984176640   3%    5.27MB/s    7:15:30
  5630132224   3%    9.31MB/s    4:05:25
  5807833088   3%    5.10MB/s    7:27:03 (FUUUU!)
{% endhighlight %} 

After about 30 minutes of flicking to and from the putty window and realising it's now 8pm, I reluctantly background my screen session and sign off for the night. 

### The next day..

At this point we had both a SQL dump and a datadir snapshot, but there was a problem. In order to run two datadirs, you either need to merge them, or you need to run two instances of MySQL, and I gave up pretty quickly trying to modify Debian's init scripts to support multiple MySQL instances. So I opt'd to merge; Annoyingly, using symlink's seems to break Percona innobackupex copy-back tool fails with the following message; 

{% highlight text %}
Original data directory is not empty! at /usr/bin/innobackupex line 503.
{% endhighlight %}

To fix this, you have to modify the datadir var in my.cnf to point directly at your SSD mount to make it work. With that problem sorted, we then play the waiting game again; 

{% highlight text %}
  TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND
20690 be/4 root       73.46 M/s   74.44 M/s  0.00 % 90.73 % perl /usr/bin/innobackupex --copy-back 2012-10-05-1349463601
{% endhighlight %}

By this stage I was beginning to wish I never ran that 10gbit line speed test, everything else felt so slow and slugish in comparison, and made our production systems feel like I was back in '99!  Once that finished, we copied in the other datadir sub directories (using the first ib_logfile0), but as you can expect MySQL did not like this; 

{% highlight text %}
InnoDB: Error: tablespace id is 45004 in the data dictionary
InnoDB: but in file ./db3/stats.ibd it is 352!
121006 16:38:59  InnoDB: Assertion failure in thread 140320318387968 in file fil0fil.c line 776
{% endhighlight %}

At this point we got tablespace id mismatch problems, and had to use the recovery toolkit; 

[http://www.mysqlperformanceblog.com/2011/05/13/connecting-orphaned-ibd-files/](http://www.mysqlperformanceblog.com/2011/05/13/connecting-orphaned-ibd-files/)

For those that know me, you'll know that the Percona Toolkit scares the shit out of me, and those 3 seconds it took to run ibdconnect were the longest 3 seconds of my life. 

{% highlight text %}
$ ./ibdconnect -o /mnt/ssd/mysql/ibdata1 -f /mnt/ssd/mysql/db3/stats.ibd -d db3 -t stats
Checking field lengths for a row (SYS_INDEXES): OFFSETS: 15 8 16 22 29 45 49 53 57
TABLE_ID: 45015
SPACE: 45010
Updating SPACE(0x00000160 , 0x60010000) for TABLE_ID: 45015
sizeof(s)=4
Next record at offset: 3C33
Record position: 3C33
Checking field lengths for a row (SYS_INDEXES): OFFSETS: 15 8 16 22 29 36 40 44 48
TABLE_ID: 45016
SPACE: 45011
Next record at offset: 3C76
Record position: 3C76
Checking field lengths for a row (SYS_INDEXES): OFFSETS: 15 8 16 22 29 36 40 44 48
TABLE_ID: 45016
SPACE: 45011
Next record at offset: 3CB9
Record position: 3CB9
Checking field lengths for a row (SYS_INDEXES): OFFSETS: 15 8 16 22 29 37 41 45 49
TABLE_ID: 45016
SPACE: 45011
Next record at offset: 3CFD
Record position: 3CFD
Checking field lengths for a row (SYS_INDEXES): OFFSETS: 15 8 16 22 29 45 49 53 57
TABLE_ID: 45016
SPACE: 45011
Next record at offset: 74
SYS_INDEXES is updated successfully
{% endhighlight %} 

I breathed a sigh of relief when I saw the word "Successfully" at the end, but sadly this process did not work very well and any attempt to access the database resulted in a hard crash. 

{% highlight text %}

121006 17:07:55  InnoDB: Error: page 8161126 log sequence number 1658523585474
InnoDB: is in the future! Current system log sequence number 809510181307.
InnoDB: Your database may be corrupt or you may have copied the InnoDB
InnoDB: tablespace but not the InnoDB log files. See
InnoDB: http://dev.mysql.com/doc/refman/5.5/en/forcing-innodb-recovery.html
InnoDB: for more information.
121006 17:07:55  InnoDB: Error: page 8159233 log sequence number 1787841102626
InnoDB: is in the future! Current system log sequence number 809510181307.
121006 17:07:55  InnoDB: Error: page 8256560 log sequence number 1653165438801
InnoDB: is in the future! Current system log sequence number 809510181307.
121006 17:07:55  InnoDB: Error: page 8241153 log sequence number 1787774448211
InnoDB: is in the future! Current system log sequence number 809510181307.
121006 17:07:55  InnoDB: Assertion failure in thread 139979472467712 in file btr0btr.c line 697
InnoDB: Failing assertion: mach_read_from_4(seg_header + FSEG_HDR_SPACE) == space
InnoDB: We intentionally generate a memory trap.
InnoDB: Submit a detailed bug report to http://bugs.mysql.com.
InnoDB: If you get repeated assertion failures or crashes, even
InnoDB: immediately after the mysqld startup, there may be
InnoDB: corruption in the InnoDB tablespace. Please refer to
InnoDB: http://dev.mysql.com/doc/refman/5.5/en/forcing-innodb-recovery.html
InnoDB: about forcing recovery.
17:07:55 UTC - mysqld got signal 6 ;
This could be because you hit a bug. It is also possible that this binary
or one of the libraries it was linked against is corrupt, improperly built,
or misconfigured. This error can also be caused by malfunctioning hardware.
We will try our best to scrape up some info that will hopefully help
diagnose the problem, but since we have already crashed,
something is definitely wrong and this may fail.
Please help us make Percona Server better by reporting any
bugs at http://bugs.percona.com/

Thread pointer: 0x4ef90e10
Attempting backtrace. You can use the following information to find out
where mysqld died. If you see no messages after this, something went
terribly wrong...
stack_bottom = 7f4f82bb6e80 thread_stack 0x20000
/usr/sbin/mysqld(my_print_stacktrace+0x2e)[0x7b453e]
/usr/sbin/mysqld(handle_fatal_signal+0x484)[0x68e664]
/lib/x86_64-linux-gnu/libpthread.so.0(+0xfcb0)[0x7f5b8193fcb0]
/lib/x86_64-linux-gnu/libc.so.6(gsignal+0x35)[0x7f5b815a7445]
/lib/x86_64-linux-gnu/libc.so.6(abort+0x17b)[0x7f5b815aabab]
/usr/sbin/mysqld[0x83739b]
/usr/sbin/mysqld[0x838faa]
/usr/sbin/mysqld[0x83ca11]
/usr/sbin/mysqld[0x885246]
/usr/sbin/mysqld[0x8879e0]
/usr/sbin/mysqld[0x7dc9fb]
/usr/sbin/mysqld(_ZN7handler7ha_openEP5TABLEPKcii+0x3e)[0x6923ae]
/usr/sbin/mysqld(_Z21open_table_from_shareP3THDP11TABLE_SHAREPKcjjjP5TABLEb+0x5dc)[0x619f2c]
/usr/sbin/mysqld(_Z10open_tableP3THDP10TABLE_LISTP11st_mem_rootP18Open_table_context+0xbb8)[0x5674c8]
/usr/sbin/mysqld(_Z11open_tablesP3THDPP10TABLE_LISTPjjP19Prelocking_strategy+0x435)[0x568de5]
/usr/sbin/mysqld(_Z30open_normal_and_derived_tablesP3THDP10TABLE_LISTj+0x48)[0x569748]
/usr/sbin/mysqld(_Z18mysqld_list_fieldsP3THDP10TABLE_LISTPKc+0x25)[0x5e1f65]
/usr/sbin/mysqld(_Z16dispatch_command19enum_server_commandP3THDPcj+0xaf7)[0x5a1537]
/usr/sbin/mysqld(_Z24do_handle_one_connectionP3THD+0x14f)[0x63c4bf]
/usr/sbin/mysqld(handle_one_connection+0x51)[0x63c581]
/lib/x86_64-linux-gnu/libpthread.so.0(+0x7e9a)[0x7f5b81937e9a]
/lib/x86_64-linux-gnu/libc.so.6(clone+0x6d)[0x7f5b81664dbd]

Trying to get some variables.
Some pointers may be invalid and cause the dump to abort.
Query (7f4f74004b88): is an invalid pointer
Connection ID (thread ID): 1
Status: NOT_KILLED
{% endhighlight %} 

So the only alternative was to try and get two instances of MySQL working (VERY frustrating), or import the raw SQL. Now using single threaded exports on MySQL isn't too bad, but using single threaded imports is extremely slow. It took approx 42 minutes to dump 1.1 billion rows across 160GB, so not too bad. 

Interesting note, the row count in show table status LIES!! It lies hard. It almost made me delete the entire thing and start over - luckily I did a COUNT(*) check on production before hand  There are a few problems with the current multi-threaded import tools currently available; 

*   mydumper does not compile very well across different platforms (See \[bug here\]\[1\]).
*   mysqldump does not allow you to use multiple threads
*   both mysqldump and mydumper do not allow you to extract the indexes as ALTER statements (I'll go into more detail about this in another blog post).
*   using mysql client to import/execute files does not handle connection problems gracefully, and you WILL end up with lost data!! 

In the end, we used the following approach: 

*   Dumped each database table data into its own individual file, with no schema or indexes.
*   Dumped each database table schema into it's own individual file, with just the schema
*   Imported the schema files into the new database, then ran SQLYog's "Schema Comparison" tool to manually generate the ALTER statements.
*   Imported the data files (concurently) into the new database (at this point there are no indexes, so it's much faster)
*   Imported the indexes (sequentially) into the new database We also had to apply the following 

`my.cnf` tuning to get a reasonable amount of performance; 

{% highlight text %}
max_connect_errors=100000000
sort_buffer_size=128M
read_buffer_size=128M
key_buffer              = 512M
key_buffer_size         = 512M
innodb_log_buffer_size=64M
innodb_log_files_in_group = 2
max_allowed_packet      = 1G
net_read_timeout = 60
thread_stack            = 128K
thread_cache_size       = 128
join_buffer_size = 128M
thread_cache = 16
table_cache            = 10000
thread_concurrency     = 32
wait_timeout=1024
interactive_timeout = 1024
tmp_table_size = 6000M
max_heap_table_size = 6000M

innodb_flush_neighbor_pages = 0
innodb_buffer_pool_size = 39080M
innodb_buffer_pool_instances=32
innodb_read_ahead=none
innodb_io_capacity=20000
innodb_adaptive_flushing        = 1
innodb_adaptive_flushing_method = estimate
query_cache_size        = 0
query_cache_type        = 0
innodb_flush_log_at_trx_commit = 0
innodb_flush_method = O_DIRECT

query_cache_min_res_unit = 512
query_cache_limit       = 3M

datadir         = /mnt/ssd/datadir
tmpdir          = /mnt/ssd/tmp
innodb_data_home_dir = /mnt/ssd/datadir
innodb_log_group_home_dir = /mnt/ssd/datadir

{% endhighlight %} 

After these tweaks were added in, we imported roughly 24,592,269 rows in about 5 minutes, with an ETA of 3 hours until finish - not bad! 

{% highlight text %}
Query OK, 19464 rows affected (0.22 sec)
Records: 19464  Duplicates: 0  Warnings: 0

Query OK, 19492 rows affected (0.17 sec)
Records: 19492  Duplicates: 0  Warnings: 0

Query OK, 19485 rows affected (0.18 sec)
Records: 19485  Duplicates: 0  Warnings: 0
{% endhighlight %} Once the database was fully imported and confirmed working, I copied the datadir to an EBS volume, so it would be much faster to start up the next time. Let me tell you, the above was the accumulation of several hours of frustrated fighting with Navicat/SQLYog/mysqldump/innodb/mydumper - and made me realise just how little tools there are for dealing with large data sets. Here are a couple of interesting blogs I found on the subject; 

* <http://www.mysqlperformanceblog.com/2012/05/16/benchmarking-single-row-insert-performance-on-amazon-ec2/> 
* <http://www.dslreports.com/shownews/Mysql-and-a-billion-rows-using-innodb-87890> 
* <http://palominodb.com/blog/2011/08/02/mydumper-myloader-fast-backup-and-restore> 
* <http://37signals.com/svn/posts/3174-taking-the-pain-out-of-mysql-schema-changes> 

### Results 

Sadly, we can't post any benchmarks as it would involve disclosing the database schema and data for the benchmarks to be relevant, and we ran out of time to create any meaningful graphs. However, I can tell you that queries which originally took 40+ minutes, were now taking around 49 seconds. This was my second time using SSDs in a production environment, and honestly, the performance boost was shocking. 

Some annoyances mysql client does not gracefully recover from errors when executing a large SQL dump; 

{% highlight text %}

ERROR 2013 (HY000) at line 4997: Lost connection to MySQL server during query
Percona 5.5 + mysqldumper + Ubuntu 11 64bit fails to run properly when using the latest repo.
{% endhighlight %} 

EC2 Ubuntu 11 64bit instance does not have a working setuptools package, you should install from source instead. 

{% highlight text %}

** Message: Connected to a MySQL server
** Message: Started dump at: 2012-10-08 16:53:16

Segmentation fault (core dumped)

[3230741.530652] processqueue[13125]: segfault at 0 ip 00007f784b722336 sp 00007f784a99be60 error 4 in libglib-2.0.so.0.3200.3[7f784b69f000+f2000]
[3230747.945488] processqueue[13131]: segfault at 0 ip 00007f72bba59336 sp 00007f72bacd2e60 error 4 in libglib-2.0.so.0.3200.3[7f72bb9d6000+f2000]
[3230758.194969] processqueue[13137]: segfault at 0 ip 00007f0c5aa93336 sp 00007f0c59d0ce60 error 4 in libglib-2.0.so.0.3200.3[7f0c5aa10000+f2000]
[3230780.686775] processqueue[13141]: segfault at 0 ip 00007f9eb5cec336 sp 00007f9eb4f65e60 error 4 in libglib-2.0.so.0.3200.3[7f9eb5c69000+f2000]
[3230784.336484] processqueue[13146]: segfault at 0 ip 00007f132641c336 sp 00007f1325695e60 error 4 in libglib-2.0.so.0.3200.3[7f1326399000+f2000]
[3230794.710549] processqueue[13153]: segfault at 0 ip 00007fb97bac9336 sp 00007fb97ad42e60 error 4 in libglib-2.0.so.0.3200.3[7fb97ba46000+f2000]
{% endhighlight %} 

Using `mysqldump --threads` is useless - see <http://lists.mysql.com/mysql/227886>

Here is a slightly annoying message you might see after trying to stop/start instances too quickly, if you get this message and you know you haven't reached your limit - just wait about 5-10 minutes and the error will go away. 

{% highlight text %}
"You have requested more instances (2) than your current instance 
limit of 1 allows for the specified instance type."
{% endhighlight %} 

And if you break fstab, there is no recovery KVM. You have to boot another instance to repair it.. and if you deattach the root device, you will get this next time; 

{% highlight text %}
Invalid value 'i-73851d0e' for instanceId. 
Instance does not have a volume attached at root (/dev/sda1)
Basically you have to forcibly reattach the 8GB drive to /dev/sda1 :X
{% endhighlight %} 

EC2 can also be bitchy when it comes to releasing/attaching disks, and using tools such as cfdisk.. sometimes, they hang, and that can cause data corruption (or in our case, DID cause data corruption!) 

{% highlight text %}
[2228865.779561] INFO: task cfdisk:15288 blocked for more than 120 seconds.
[2228865.779574] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[2228865.779581] cfdisk          D ffff880f22cd36c0     0 15288      1 0x00000004
[2228865.779586]  ffff880ebdf17cb8 0000000000000286 0000000000000000 000000000000000e
[2228865.779591]  ffff880ebdf17fd8 ffff880ebdf17fd8 ffff880ebdf17fd8 00000000000136c0
[2228865.779595]  ffff880ec124adc0 ffff880e98432dc0 0000000000000000 7fffffffffffffff
[2228865.779599] Call Trace:
[2228865.779611]  [<ffffffff816508cf>] schedule+0x3f/0x60
[2228865.779615]  [<ffffffff81650f15>] schedule_timeout+0x2a5/0x320
[2228865.779622]  [<ffffffff8111e7c4>] ? write_cache_pages+0x124/0x460
[2228865.779627]  [<ffffffff813a54b1>] ? notify_remote_via_irq+0x31/0x50
[2228865.779630]  [<ffffffff8111e0a0>] ? set_page_dirty_lock+0x50/0x50
[2228865.779634]  [<ffffffff8165296e>] ? _raw_spin_unlock_irqrestore+0x1e/0x30
[2228865.779638]  [<ffffffff8164ff8f>] wait_for_common+0xdf/0x180
[2228865.779644]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2228865.779649]  [<ffffffff8105e2c0>] ? try_to_wake_up+0x200/0x200
[2228865.779653]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2228865.779656]  [<ffffffff8165010d>] wait_for_completion+0x1d/0x20
[2228865.779659]  [<ffffffff8119bf8c>] writeback_inodes_sb_nr+0x7c/0xa0
[2228865.779662]  [<ffffffff8119c1fe>] writeback_inodes_sb+0x2e/0x40
[2228865.779665]  [<ffffffff811a324e>] __sync_filesystem+0x4e/0x90
[2228865.779668]  [<ffffffff811a32af>] sync_one_sb+0x1f/0x30
[2228865.779673]  [<ffffffff81178005>] iterate_supers+0xa5/0x100
[2228865.779676]  [<ffffffff811a3360>] sys_sync+0x30/0x70
[2228865.779679]  [<ffffffff8165ad42>] system_call_fastpath+0x16/0x1b
[2229068.552059] blkfront device/vbd/2208 num-ring-pages 1 nr_ents 32.
[2229068.963419] blkfront: xvdk: barrier or flush: disabled
[2229068.964565]  xvdk: xvdk1
[2229115.116028] vbd vbd-2208: 16 Device in use; refusing to close
[2229225.779565] INFO: task cfdisk:15288 blocked for more than 120 seconds.
[2229225.779577] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[2229225.779584] cfdisk          D ffff880f22c136c0     0 15288      1 0x00000004
[2229225.779589]  ffff880ebdf17cd8 0000000000000286 ffff880ebdf17cf0 ffff880ebdf17cf0
[2229225.779594]  ffff880ebdf17fd8 ffff880ebdf17fd8 ffff880ebdf17fd8 00000000000136c0
[2229225.779598]  ffffffff81c0d020 ffff880e98432dc0 ffff880e00000000 7fffffffffffffff
[2229225.779603] Call Trace:
[2229225.779615]  [<ffffffff816508cf>] schedule+0x3f/0x60
[2229225.779618]  [<ffffffff81650f15>] schedule_timeout+0x2a5/0x320
[2229225.779623]  [<ffffffff813a54b1>] ? notify_remote_via_irq+0x31/0x50
[2229225.779626]  [<ffffffff813a5e6b>] ? xen_send_IPI_one+0x2b/0x30
[2229225.779632]  [<ffffffff81011770>] ? xen_smp_send_reschedule+0x10/0x20
[2229225.779636]  [<ffffffff810516c2>] ? ttwu_queue+0x92/0xd0
[2229225.779639]  [<ffffffff8164ff8f>] wait_for_common+0xdf/0x180
[2229225.779646]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2229225.779650]  [<ffffffff8105e2c0>] ? try_to_wake_up+0x200/0x200
[2229225.779653]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2229225.779656]  [<ffffffff8165010d>] wait_for_completion+0x1d/0x20
[2229225.779660]  [<ffffffff8119c15d>] sync_inodes_sb+0x8d/0xc0
[2229225.779665]  [<ffffffff81110000>] ? perf_event_create_kernel_counter+0x20/0xf0
[2229225.779668]  [<ffffffff811a3288>] __sync_filesystem+0x88/0x90
[2229225.779671]  [<ffffffff811a32af>] sync_one_sb+0x1f/0x30
[2229225.779676]  [<ffffffff81178005>] iterate_supers+0xa5/0x100
[2229225.779679]  [<ffffffff811a3377>] sys_sync+0x47/0x70
[2229225.779683]  [<ffffffff8165ad42>] system_call_fastpath+0x16/0x1b
[2229225.779686] INFO: task cfdisk:15523 blocked for more than 120 seconds.
[2229225.779692] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[2229225.779697] cfdisk          D ffff880f22c336c0     0 15523  29316 0x00000000
[2229225.779701]  ffff880ec04adcb8 0000000000000286 0000000000000000 000000000000000e
[2229225.779705]  ffff880ec04adfd8 ffff880ec04adfd8 ffff880ec04adfd8 00000000000136c0
[2229225.779709]  ffff880ec121adc0 ffff880d1c4144a0 ffff880ec04adce8 7fffffffffffffff
[2229225.779713] Call Trace:
[2229225.779716]  [<ffffffff816508cf>] schedule+0x3f/0x60
[2229225.779719]  [<ffffffff81650f15>] schedule_timeout+0x2a5/0x320
[2229225.779724]  [<ffffffff8111e7c4>] ? write_cache_pages+0x124/0x460
[2229225.779727]  [<ffffffff813a54b1>] ? notify_remote_via_irq+0x31/0x50
[2229225.779730]  [<ffffffff8111e0a0>] ? set_page_dirty_lock+0x50/0x50
[2229225.779734]  [<ffffffff8165296e>] ? _raw_spin_unlock_irqrestore+0x1e/0x30
[2229225.779738]  [<ffffffff8164ff8f>] wait_for_common+0xdf/0x180
[2229225.779741]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2229225.779744]  [<ffffffff8105e2c0>] ? try_to_wake_up+0x200/0x200
[2229225.779747]  [<ffffffff811a3290>] ? __sync_filesystem+0x90/0x90
[2229225.779750]  [<ffffffff8165010d>] wait_for_completion+0x1d/0x20
[2229225.779753]  [<ffffffff8119bf8c>] writeback_inodes_sb_nr+0x7c/0xa0
[2229225.779756]  [<ffffffff8119c1fe>] writeback_inodes_sb+0x2e/0x40
[2229225.779759]  [<ffffffff811a324e>] __sync_filesystem+0x4e/0x90
[2229225.779762]  [<ffffffff811a32af>] sync_one_sb+0x1f/0x30
[2229225.779765]  [<ffffffff81178005>] iterate_supers+0xa5/0x100
[2229225.779768]  [<ffffffff811a3360>] sys_sync+0x30/0x70
[2229225.779770]  [<ffffffff8165ad42>] system_call_fastpath+0x16/0x1b
[2229470.670222] block xvdh: releasing disk
{% endhighlight %}
