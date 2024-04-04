# -*- coding: UTF-8 -*-
import argparse
class Head(object):
    def __init__(self, num):
        self.num = num

    @classmethod
    def parse(cls, argv):
        parser = argparse.ArgumentParser(prog='head', description='Return only the n first items')
        parser.add_argument('-n', type=int, default=None, required=True, help='The number of items to forward')
        args = parser.parse_args(argv)
        return cls(args.n)

    def process(self, iterable):
        idx = 0
        for collection in iterable:
            if idx >= self.num:
                break
            yield(collection)
            idx += 1