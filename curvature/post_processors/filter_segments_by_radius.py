# -*- coding: UTF-8 -*-
import argparse
from curvature.geomath import distance_on_earth

class FilterSegmentsByRadius(object):
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    @classmethod
    def parse(cls, argv):
        parser = argparse.ArgumentParser(prog='filter_segments_by_radius', description='Filter segments by curve radius (in meters), removing them from their parent way.')
        parser.add_argument('--min', type=float, default=None, help='The minimum radius to include in output.')
        parser.add_argument('--max', type=float, default=None, help='The maximum radius to include in output.')
        args = parser.parse_args(argv)
        if not args.min and not args.max:
            raise RuntimeError("Error: one or more of [--min, --max] options are required\n")
        return cls(args.min, args.max)

    def select_segment(self, segment):
        if self.min is not None and self.min > segment['radius']:
            return False
        if self.max is not None and self.max < segment['radius']:
            return False
        return True

    def process(self, iterable):
        for collection in iterable:
            for way in collection['ways']:
                all_segments = way['segments']
                last_index = len(all_segments) - 1
                indexes = [i for i, segment
                    in enumerate(all_segments)
                    if i == 0 or i == last_index or self.select_segment(segment)
                ]
                way['segments'] = filtered_segments = [all_segments[i] for i in indexes]
                for i, segment in enumerate(way['segments']):
                    if i + 1 < len(way['segments']):
                        segment['end'] = end = filtered_segments[i + 1]['start']
                        start = segment['start']
                        segment['length'] = distance_on_earth(start[0], start[1], end[0], end[1])
            yield(collection)