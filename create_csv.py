#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:52:35 2017

@author: dennis
"""

import os
import csv


train_data = "speechdata/Training/"

output = open("phone_data.csv", "w+")
output_writer = csv.writer(output)

for foldername in os.listdir(train_data):
    for filename in os.listdir(train_data + foldername):
        if "mfcc" in filename:
            mfcc = open(train_data + foldername + "/" + filename)
            phn = open(train_data + foldername + "/" + filename[:-5] + ".phn")
            for line in phn:
                phn_data = line.split()
                start = int(phn_data[0])
                end = int(phn_data[1])
                for _ in range((end-start)//128-1):
                    try:
                        line = next(mfcc).split()
                        line = [float(x) for x in line]
                        output_writer.writerow([phn_data[2]] + line)
                    except StopIteration:
                        print("Wrong alignment")
