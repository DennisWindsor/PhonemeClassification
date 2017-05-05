#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 22:17:26 2017

@author: dennis
"""

# Refactor with numpy?

from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
from operator import add
import csv
import random

# For testing - set current distance measure
fdist = cosine

data_file = open("phone_data.csv","r+")
data_reader = csv.reader(line.replace('\0','') for line in data_file)

# Phonemes present in data
phones = set()
# K-means
means = []
# Data for training and testing
mfccs = []

# Read in labeled data
for line in data_reader:
    phones.add(line[0])
    mfccs.append([float(x) for x in line[1:]])

# Set means randomly
for i in range(len(phones)):
    mean = mfccs[random.randrange(0,len(mfccs))]
    while mean in means:
        mean = mfccs[random.randrange(0,len(mfccs))]
    means.append(mean)

# Separate training and testing data
train_data = mfccs[0:80000]
test_data = mfccs[80000:]

# Ten iterations of updating means
for _ in range(10):
    nearest = []
    for mfcc in train_data:
        near_dist = float('inf')
        near = None
        for i, mean in enumerate(means):
            dist = fdist(mfcc, mean)
            if dist < near_dist:
                near_dist = dist
                near = i
    # Update means
    sums = [[0 for i in range(len(mfccs[0]))] for _ in range(len(means))]
    counts = [0 for i in range(len(means))]
    for i, mfcc in enumerate(train_data):
        map(add, mfcc, sums[nearest[i]])
        counts[nearest[i]] +=1
    # update means
    for i in range(len(means)):
        means[i] = [x/counts[i] for x in sums[i]]
    
print(len(phones))
print(len(mfccs))
data_file.close()