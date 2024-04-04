#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import msgpack
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from curvature.post_processors.filter_out_ways_with_tag import FilterOutWaysWithTag
from curvature.post_processors.add_segments import AddSegments
from curvature.post_processors.add_segment_length_and_radius import AddSegmentLengthAndRadius
from curvature.post_processors.add_segment_curvature import AddSegmentCurvature
from curvature.post_processors.filter_segment_deflections import FilterSegmentDeflections
from curvature.post_processors.split_collections_on_straight_segments import SplitCollectionsOnStraightSegments
from curvature.post_processors.roll_up_length import RollUpLength
from curvature.post_processors.roll_up_curvature import RollUpCurvature
from curvature.post_processors.filter_collections_by_curvature import FilterCollectionsByCurvature
from curvature.post_processors.sort_collections_by_sum import SortCollectionsBySum

# Take the following processing steps first:
# 1. Collect the highway ways and their points into collections.
# 2. Filter out unpaved ways and highway types we aren't interested in.
# 3. Add segments and their lengths & radii.
# 4. Calculate the curvature and filter curvature values for "deflections" (noisy data)
# 5. Split our collections on long straight-aways (longer than 1.5 miles) to avoid
#    highlighting long straight roads with infrequent curvy-sections.
# 6. Sum the length and curvature of the sections in each way for reuse.
# 7. Filter out collections not meeting our minimum curvature thresholds.
# 3. Sort the items by their curvature value.
# 3. Save the intermediate data.


chain = [
  msgpack.Unpacker(sys.stdin.buffer, use_list=True, encoding='utf-8'),
  FilterOutWaysWithTag('surface', ['unpaved','dirt','gravel','fine_gravel','sand','grass','ground','pebblestone','mud','clay','dirt/sand','soil']),
  FilterOutWaysWithTag('service', ['driveway', 'parking_aisle', 'drive-through', 'parking', 'bus', 'emergency_access']),
  AddSegments(),
  AddSegmentLengthAndRadius(),
  AddSegmentCurvature(),
  FilterSegmentDeflections(),
  SplitCollectionsOnStraightSegments(2414),
  RollUpLength(),
  RollUpCurvature(),
  FilterCollectionsByCurvature(min=300),
  SortCollectionsBySum(key='curvature', reverse=True)
]

process_chain = reduce(lambda acc, processor: processor.process(acc), chain)

def print_msgpack(arg):
  sys.stdout.buffer.write(msgpack.packb(arg, use_bin_type=True))

for collection in process_chain:
  print_msgpack(collection)