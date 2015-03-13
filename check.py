#!/usr/bin/env python

from glob import glob
from functools import wraps

import os
import fnmatch
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def benchmark_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        t = time.time()
        result = f(*args, **kwargs)
        logger.debug("%s: took %.4f"%(f.__name__, time.time()-t))
        return result
    return wrapper

def recursive_glob(path, pattern='*'):
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)

class PollCheck(object):
    def __init__(self):
        self.db = {}

    @benchmark_decorator
    def poll(self, path):
        fields = ['st_atime', 'st_blksize', 'st_blocks', 'st_ctime', 'st_dev', 'st_gid', 
        'st_ino', 'st_mode', 'st_mtime', 'st_nlink', 'st_rdev', 'st_size', 'st_uid']

        for path in recursive_glob(path):
            lstat_result = os.stat(path)
            lstat_result = { field:getattr(lstat_result, field) for field in fields }
            if path in self.db and self.db[path] != lstat_result:
                logging.debug("Change detected: {}".format(path))
        self.db[path] = lstat_result

    def watch(self, path, interval):
        while True:
            self.poll(path)
            time.sleep(interval)


if __name__ == '__main__':
    pc = PollCheck()
    pc.watch('./', 0.25)
