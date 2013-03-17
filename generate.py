#!/usr/bin/python

import sys
import argparse
import random
import math
import numpy
from numpy import *
from numpy.random import *
from automaton import Tilemap2dAutomaton
from perlin import PerlinNoise
import Fbm

try:
    import json
except:
    import simplejson as json

parser = argparse.ArgumentParser(description="Generates a map using a 2d Tilemap automaton")
parser.add_argument('--size-x', type=int, required=True, help="map maximum x coordinate")
parser.add_argument('--size-y', type=int, required=True, help="map maximum y coordinate")
parser.add_argument('--method', type=str, required=True, help="automaton2d|perlin")
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout, help="file to save generated map")

STATES = ["land", "water"]

def generate_random(max_x, max_y):
    rand_map = random_integers(0, len(STATES) -1, (max_y, max_x))

    total_tiles = max_x * max_y
    print "generated new map with %s tiles:" % total_tiles 
    stats = {}
    for col in rand_map:
        for row in col:
            stat = stats.get(row, 0)
            stats[row] = stat + 1

    print "breakdown:"
    for stat, count in stats.items():
        print "%s: %s (%s percent)" % (STATES[stat], count, float(count)/total_tiles * 100)

    return rand_map

def write(tilemap, options):
    options.outfile.write(json.dumps({'tilemap': tilemap.tolist()}))

if __name__ == "__main__":
    args = parser.parse_args()

    if args.method == "automaton2d":
        seedmap = generate_random(args.size_x, args.size_y)
        tilemap = Tilemap2dAutomaton(seedmap, range(len(STATES)))
        tilemap.run_rule()
        write(tilemap.grid, args)
    elif args.method == "perlin":
        noise = PerlinNoise()

        persistence = 1.0 / 2.0 
        octaves = 6 

        height_map = []
        for i in range(args.size_y):
            height_map.append([])

            for j in range(args.size_x):
                fbm = Fbm.fractional_browning_motion(octaves, noise, persistence,  
                         i * 1.0 / args.size_x, j * 1.0 / args.size_y)

                #normalize to 0-255
                height_map[i].append(int(round((fbm + 1) / 2.0 * 255)))

        args.outfile.write(json.dumps({'tilemap': height_map}))
