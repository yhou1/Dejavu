# -*- coding: UTF-8 -*-
import argparse
from curvature.collection_tools import SquashCurvatureNearbyProcessorAbstract
import sys

class SquashCurvatureNearTaggedNodes(SquashCurvatureNearbyProcessorAbstract):
    def __init__(self, tag=None, values=None, distance=0):
        self.tag = tag
        self.values = values
        super().__init__(distance)

    @classmethod
    def parse(cls, argv):
        parser = argparse.ArgumentParser(prog='squash_curvature_near_tagged_nodes', description='Squash the curvature on segments close to tagged nodes.')
        parser.add_argument('--tag', type=str, required=True, help='The tag to match on. Example: highway')
        parser.add_argument('--values', type=str, help='The tag values which will trigger squashing when found. Example: stop,give_way,traffic_signals,crossing,traffic_calming,mini_roundabout. If not specified, any value will match.')
        parser.add_argument('--distance', type=int, required=True, help='The number of meters forward and backward at which to squash curvature. Example: 30')
        args = parser.parse_args(argv)
        if args.values:
            values = args.values.split(',')
        else:
            values = None
        return cls(args.tag, values, args.distance)

    def process_collection(self, collection):
        for i, way in enumerate(collection['ways']):
            for j, segment in enumerate(way['segments']):
                if len(segment['start']) == 3 and self.node_matches(way['nodes'][segment['start'][2]]):
                    self.squash_segment_curvature_nearby(collection, i, j, 'start')
                if len(segment['end']) == 3 and self.node_matches(way['nodes'][segment['end'][2]]):
                    self.squash_segment_curvature_nearby(collection, i, j, 'end')
        return collection

    def node_matches(self, node):
        if self.tag in node['tags']:
            if self.values == None:
                return True
            elif node['tags'][self.tag] in self.values:
                return True
            else:
                return False
        else:
            return False