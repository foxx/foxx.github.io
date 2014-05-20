---
layout: post
title:  Storing billions of UUID fields in MySQL InnoDB
date:   2013-02-17 00:00:00
categories: general
coverimage: /img/covers/storing-billions-of-uuids.jpg
weight: 5
---

During one of our builds, we came up against a requirement of having to store UUIDs in MySQL. Not knowing which was the best way, we tried all of them. We ran these benchmarks on commodity hardware with no modifications on Percona MySQL 5.5 with no stock my.cnf changes. Our benchmarks showed that BINARY(16) was the fastest option. However, with some tuning to my.cnf you may see different results.

The conditions were;

*   Trimming is not allowed (not storing the entire hash is unsafe due to the way that UUIDs are created - see [this article][1]
*   Hashing is not allowed (hashing the UUID and then trimming the hash is unsafe for the same reasons as above)
*   Optimal SELECT/INSERT performance (The storage needed to perform well under heavy INSERT/SELECT load, and not slow down considerably as the table sizes grew)
*   Avoid unnecessary JOINs (Although we could store the UUIDs in a separate table, we want to try and avoid this where possible)

Our options were;

*   Store as a VARCHAR
*   Store as a BINARY(16)
*   Store as a CHAR(36)
*   Store as a series of BIGINT

Some inspiration and references were taken from the following articles;

[http://xcitestudios.com/blog/2010/01/31/mysql-and-binary16-the-reasonsbenefitsdr...][2] 
<http://kccoder.com/mysql/uuid-vs-int-insert-performance/>

### Store as CHAR(36)

Store UUID in hex format as CHAR(36).

{% highlight text %}
INSERT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               100000               1.87230491638
200000               100000               2.42642807961
300000               100000               3.65519285202
400000               100000               4.23701429367
500000               100000               4.88455510139
600000               100000               5.57620716095
700000               100000               7.50717425346
800000               100000               9.49350070953
900000               100000               10.1547751427
1000000              100000               12.0748021603
1100000              100000               12.277310133
1200000              100000               12.2819159031
1300000              100000               16.9854588509
1400000              100000               20.3873689175
1500000              100000               21.8642649651
1600000              100000               24.4224257469
1700000              100000               29.6857917309
1800000              100000               31.5416200161
1900000              100000               35.4671728611
2000000              100000               41.4726109505

SELECT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               10000                0.165283203125
200000               10000                0.163378000259
300000               10000                0.162928104401
400000               10000                0.164531946182
500000               10000                0.170125961304
600000               10000                0.167329072952
700000               10000                0.166491746902
800000               10000                0.174521684647
900000               10000                0.167996168137
1000000              10000                0.171768426895
1100000              10000                0.171753883362
1200000              10000                0.170397043228
1300000              10000                0.175933599472
1400000              10000                0.188637733459
1500000              10000                0.205511808395
1600000              10000                0.764106750488
1700000              10000                0.584647893906
1800000              10000                0.814380884171
1900000              10000                0.549372911453
2000000              10000                0.635137557983

{% endhighlight %}

### Store as INT

Split and store as INT Break up the UUID into 6 parts (based on the python attribute 'uuid.UUID.fields'), which consist of the following;

{% highlight text %}
1 - int(10) (4 bytes)
2 - smallint(5) (2 bytes)
3 - smallint(5) (2 bytes)
4 - tinyint(3) (1 byte)
5 - tinyint(3) (1 byte)
6 - bigint(20) (8 bytes)
autoinc - bigint(20) (8 bytes)
Total bytes per row: 24
{% endhighlight %}

These are then inserted into the database in 6 different fields, along with an auto increment BIGINT(20) `id` field. This allows you to store the UUIDs in a seperate table, then reference them as a single BIGINT, meaning you can store a maximum of 9,223,372,036,854,775,807 UUIDs.

{% highlight text %}
INSERT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               100000               2.19501686096
200000               100000               2.07490730286
300000               100000               2.34748411179
400000               100000               2.3466489315
500000               100000               2.49323415756
600000               100000               3.2193582058
700000               100000               3.01286005974
800000               100000               3.84334850311
900000               100000               4.00044703484
1000000              100000               4.83631157875
1100000              100000               7.02526879311
1200000              100000               5.22901296616
1300000              100000               6.71364355087
1400000              100000               6.89418077469
1500000              100000               5.10271024704
1600000              100000               6.458537817
1700000              100000               8.49526190758
1800000              100000               9.23726868629
1900000              100000               11.4352693558
2000000              100000               15.077085495

SELECT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               10000                1.68526768684
200000               10000                1.68020987511
300000               10000                1.68714618683
400000               10000                1.67019486427
500000               10000                1.69050502777
600000               10000                1.68600797653
700000               10000                1.66904735565
800000               10000                1.68317008018
900000               10000                1.67073392868
1000000              10000                1.69239616394
1100000              10000                1.69070410728
1200000              10000                1.68941402435
1300000              10000                1.67224788666
1400000              10000                1.68502855301
1500000              10000                1.68925213814
1600000              10000                1.68169212341
1700000              10000                1.67716264725
1800000              10000                1.67365789413
1900000              10000                1.68234705925
2000000              10000                1.71537613869
{% endhighlight %}

### Store as BINARY(16) string

Convert the UUID to a 16 byte string (using unhexlify/UNHEX) and store in a BINARY(16) field.

{% highlight text %}
INSERT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               100000               2.35787940025
200000               100000               1.5819132328
300000               100000               2.00737380981
400000               100000               2.36268806458
500000               100000               1.95024132729
600000               100000               2.52386879921
700000               100000               2.46662926674
800000               100000               3.63739991188
900000               100000               3.62550187111
1000000              100000               4.08164095879
1100000              100000               4.74432897568
1200000              100000               6.74240970612
1300000              100000               6.22160053253
1400000              100000               8.04201221466
1500000              100000               6.05508232117
1600000              100000               6.95644521713
1700000              100000               5.36873197556
1800000              100000               7.14802789688
1900000              100000               7.14896821976
2000000              100000               9.12283611298

SELECT PERFORMANCE
--------------------------------------------------------
total_rows           chunk_size           time_taken
100000               10000                0.0722301006317
200000               10000                0.0698809623718
300000               10000                0.0726082324982
400000               10000                0.0731747150421
500000               10000                0.0735011100769
600000               10000                0.0744516849518
700000               10000                0.0759541988373
800000               10000                0.0766224861145
900000               10000                0.0773425102234
1000000              10000                0.0773928165436
1100000              10000                0.0789988040924
1200000              10000                0.0786738395691
1300000              10000                0.077996969223
1400000              10000                0.0804636478424
1500000              10000                0.0809540748596
1600000              10000                0.0811409950256
1700000              10000                0.081680059433
1800000              10000                0.0814859867096
1900000              10000                0.0813221931458
2000000              10000                0.0838458538055
{% endhighlight %}

### Proof of concept code

{% highlight python %}
#!/usr/bin/env python

import MySQLdb
import logging
import uuid
import time
import random
from contextlib import contextmanager
from binascii import unhexlify, hexlify

def configure_logging():
    #FORMAT = "[%(asctime)-15s] [%(levelname)s] [%(process)d/%(processName)s] %(message)s"
    FORMAT = "[%(asctime)-15s] [%(filename)s:%(lineno)d] [%(process)d/%(processName)s] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

configure_logging()

def flatten_list(seq):
    merged = []
    for s in seq:
        for x in s:
            merged.append(x)
    return merged

class Benchmark(object):
    def __init__(self):
        self.start = time.time()
        self.marks = []
        self.times = []

    @contextmanager
    def benchmark(self):
        t = time.time()
        yield
        now = time.time()
        elapsed = now - t
        o = (t, now, elapsed)
        self.times.append(o)

    @contextmanager
    def mark(self, data):
        assert isinstance(data, dict)
        total_elapsed = sum(map(lambda x: x[2], self.times))
        o = (time.time(), total_elapsed, data)
        self.marks.append(o)
        self.times = []

    def dump(self):
        h = "%-20s %-20s %-20s"
        print h % ( "total_rows", "chunk_size", "time_taken")
        for x in self.marks:
            d = x[2]
            print h % ( d['total_rows'], d['chunk_size'], x[1])


class UUIDTest(object):

    # The amount of UUIDs pre-generated for each database commit
    # Setting this too high may result in "MySQL server has gone away" errors
    COMMIT_CHUNK_SIZE = 20000

    # The amount of rows to insert at any given time in a single 
    # commit using executemany().
    LOOP_SIZE = 100000

    # The amount of rows to insert in total for each test
    TOTAL_ROWS = 2000000

    # The amount of UUIDs to select against
    SELECT_CHUNK_SIZE = 2000

    def __init__(self, dbconn):
        self.db = dbconn

    def start(self):
        self.create_database()
        #self.run_test('uuidstore1')
        #self.run_test('uuidstore2')
        self.run_test('uuidstore3')

    def generate_uuid(self, total):
        """Generate a list of random UUIDs. Time spent generating
        these is not taken into consideration when comparing performance
        between each test. This is because we are only interested in the
        db select/insert performance"""

        x = map(lambda x: uuid.uuid4(), range(self.COMMIT_CHUNK_SIZE))
        return x

    ######################################################
    # UUIDSTORE3 TESTS
    ######################################################
    def uuidstore3_insert(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: str(x), uuidlist)
        
        # Insert UUIDs into database
        c = self.db.cursor()
        with self.ib.benchmark():
            c.executemany("""
                INSERT INTO `uuidstore3` (uuid)
                VALUES (%s)
            """, ui)
            self.db.commit()
        c.close()

    def uuidstore3_select(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: str(x), uuidlist)
        
        selectui_values = ui
        selectui_sql = [ '%s', ] * len(selectui_values)
        selectui_sql = ",".join(selectui_sql)

        # select
        c = self.db.cursor()
        with self.sb.benchmark():
            sql = """
                SELECT 
                    id
                FROM
                    `uuidstore3`
                WHERE
                    uuid IN (%s)
            """ % ( selectui_sql, )
            c.execute(sql, selectui_values)
            r = c.fetchall()
            assert len(r) == self.SELECT_CHUNK_SIZE
        c.close()

    ######################################################
    # UUIDSTORE2 TESTS
    ######################################################
    def uuidstore2_insert(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: unhexlify(str(x).replace("-", "")), uuidlist)
        
        # Insert UUIDs into database
        c = self.db.cursor()
        with self.ib.benchmark():
            c.executemany("""
                INSERT INTO `uuidstore2` (uuid)
                VALUES (%s)
            """, ui)
            self.db.commit()
        c.close()

    def uuidstore2_select(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: unhexlify(str(x).replace("-", "")), uuidlist)
        
        selectui_values = ui
        selectui_sql = [ '%s', ] * len(selectui_values)
        selectui_sql = ",".join(selectui_sql)

        # select
        c = self.db.cursor()
        with self.sb.benchmark():
            sql = """
                SELECT 
                    id
                FROM
                    `uuidstore2`
                WHERE
                    uuid IN (%s)
            """ % ( selectui_sql, )
            c.execute(sql, selectui_values)
            r = c.fetchall()
            assert len(r) == self.SELECT_CHUNK_SIZE
        c.close()

    ######################################################
    # UUIDSTORE1 TESTS
    ######################################################
    def uuidstore1_insert(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: x.fields, uuidlist)
        
        # Insert UUIDs into database
        c = self.db.cursor()
        with self.ib.benchmark():
            c.executemany("""
                INSERT INTO `uuidstore1` (uuid1, uuid2, uuid3, uuid4, uuid5, uuid6)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, ui)
            self.db.commit()
        c.close()

    def uuidstore1_select(self, uuidlist):
        # convert list into necessary format
        ui = map(lambda x: x.fields, uuidlist)

        # format sql
        selectui_sql = map(lambda x: """(
            uuid1 = %s AND 
            uuid2 = %s AND 
            uuid3 = %s AND 
            uuid4 = %s AND 
            uuid5 = %s AND 
            uuid6 = %s)""", range(len(ui)))
        selectui_sql = " OR ".join(selectui_sql)
        selectui_values = flatten_list(ui)

        # select
        c = self.db.cursor()
        with self.sb.benchmark():
            sql = """
                SELECT 
                    id
                FROM
                    `uuidstore1`
                WHERE
                    %s
            """ % ( selectui_sql, )
            c.execute(sql, selectui_values)
            r = c.fetchall()
            assert len(r) == self.SELECT_CHUNK_SIZE
        c.close()

    def run_test(self, test_name):
        # create benchmark object
        self.ib = Benchmark()
        self.sb = Benchmark()

        # Fetch some UUIDs
        cnt=0
        loopcnt=0
        selectcnt = 0
        while cnt < self.TOTAL_ROWS:
            # incr
            loopcnt += self.COMMIT_CHUNK_SIZE
            cnt += self.COMMIT_CHUNK_SIZE
            selectcnt += self.SELECT_CHUNK_SIZE
            print "currently at", cnt

            # Generate a list of UUIDs
            uuidlist = self.generate_uuid(self.COMMIT_CHUNK_SIZE)

            # insert
            insert_fn = "%s_insert" % ( test_name, )
            getattr(self, insert_fn)(uuidlist)

            # select
            selectui = random.sample(uuidlist, self.SELECT_CHUNK_SIZE)
            select_fn = "%s_select" % ( test_name, )
            getattr(self, select_fn)(selectui)

            # to avoid skewing the graphs, group into 
            if loopcnt >= self.LOOP_SIZE:
                self.ib.mark({
                    'total_rows' : cnt,
                    'chunk_size' : loopcnt
                })

                self.sb.mark({
                    'total_rows' : cnt,
                    'chunk_size' : selectcnt
                })
                loopcnt = 0
                selectcnt = 0

        print "TEST: INSERT %s" % ( test_name, )
        self.ib.dump()

        print "TEST: SELECT %s" % ( test_name, )
        self.sb.dump()

        print "WAT"

    def create_database(self):
        """Create databases and tables"""

        c = self.db.cursor()
        c.execute("DROP DATABASE IF EXISTS `uuidtest`")
        c.execute("CREATE DATABASE `uuidtest`")

        self.db.select_db("uuidtest")

        c.execute("""
            CREATE TABLE `uuidstore1` (
              `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `uuid1` int(10) unsigned NOT NULL,
              `uuid2` smallint(5) unsigned NOT NULL,
              `uuid3` smallint(5) unsigned NOT NULL,
              `uuid4` tinyint(3) unsigned NOT NULL,
              `uuid5` tinyint(3) unsigned NOT NULL,
              `uuid6` bigint(20) unsigned NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `uuid1` (`uuid1`,`uuid2`,`uuid3`,`uuid4`,`uuid5`,`uuid6`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """)
        
        c.execute("""
            CREATE TABLE `uuidstore2` (
              `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `uuid` binary(16) NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `uuid` (`uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """)

        c.execute("""
            CREATE TABLE `uuidstore3` (
              `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `uuid` char(36) DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `uuid` (`uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """)

        self.db.commit()

c = MySQLdb.connect('localhost', 'root', 'root')
u = UUIDTest(c)
u.start()

{% endhighlight %}

 [1]: http://blogs.msdn.com/b/oldnewthing/archive/2008/06/27/8659071.aspx
 [2]: http://xcitestudios.com/blog/2010/01/31/mysql-and-binary16-the-reasonsbenefitsdrawbacks-mysql/
