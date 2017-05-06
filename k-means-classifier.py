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
fdist = euclidean

# Limit size of data
train_start = 0
train_stop = 10000
test_start = 10000
test_stop = 12000

data_file = open("phone_data.csv","r+")
data_reader = csv.reader(line.replace('\0','') for line in data_file)

# Phonemes present in data
phones = set()
# Actual values
true_values = []
# K-means
means = []
# Data for training and testing
mfccs = []

# Read in labeled data
print('Reading data')
for line in data_reader:
    phones.add(line[0])
    true_values.append(line[0])
    mfccs.append([float(x) for x in line[1:]])

print('Choosing means')

# Set means randomly
for i in range(len(phones)):
    mean = mfccs[random.randrange(0,len(mfccs))]
    while mean in means:
        mean = mfccs[random.randrange(0,len(mfccs))]
    means.append(mean)

# Separate training and testing data
train_data = mfccs[train_start:train_stop]
test_data = mfccs[test_start:test_stop]

print('Training')
# Ten iterations of updating means
for i in range(5):
    print('Iteration {}'.format(i))
    nearest = []
    for mfcc in train_data:
        near_dist = float('inf')
        near = None
        for i, mean in enumerate(means):
            dist = fdist(mfcc, mean)
            if dist < near_dist:
                near_dist = dist
                near = i
        if near is None:
            print('Incorrect NoneType')
            print(near)
            print(near_dist)
            input()
        nearest.append(near)
    # Update means
    sums = [[0 for i in range(len(mfccs[0]))] for _ in range(len(means))]
    counts = [0 for i in range(len(means))]
    for i, mfcc in enumerate(train_data):
        sums[nearest[i]] = [x+y for x, y in zip(mfcc, sums[nearest[i]])]
        counts[nearest[i]] +=1
    # update means
    for i in range(len(means)):
        if counts[i] != 0:
            means[i] = [x/counts[i] for x in sums[i]]
        else:
            print('Zero count')

# Test how well clustering has worked
guesses=[]    
for _ in range(len(means)):
    guesses.append([])
print('Testing')
for i, phone in enumerate(test_data):
    value = true_values[80000+i]
    near_dist = float('inf')
    near = None
    for j, mean in enumerate(means):
        dist = fdist(mean, phone)
        if dist < near_dist:
            near_dist = dist
            near = j
    guesses[near].append(value)
print('Results')
for guess in guesses:
    print(guess)
    input()
data_file.close()