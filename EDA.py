#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:02:28 2019

@author: aaboyles
"""
from math import *
import numpy as np
import pandas as pd
import skbio
from plotnine import *

with open('HXB2.txt', 'r') as file:
  hxb2 = file.read().upper()

nchar = len(hxb2)

#inputFile = "Indiana_KY_pol_alnnotstr1_Quest_Labcorp_full_985pos_dedupe_332taxa_no_nonIndiana_plus_refs_new3.csv"
lanlData = pd.read_csv('results.txt', sep='\t')
#lanlData = pd.read_csv(inputFile)
lanlData['SequenceLength'] = [len(x) for x in lanlData['Sequence']]
(ggplot(lanlData, aes('SequenceLength')) + geom_histogram())

subset = lanlData[lanlData['SequenceLength'] < 10000]
(ggplot(subset, aes('SequenceLength')) + geom_histogram())

# I don't believe this aligner actually works like this, so consider it a
# placeholder for a more careful tending to
aligner = skbio.alignment.StripedSmithWaterman(hxb2)
subset['Aligned'] = [aligner(seq).aligned_target_sequence for seq in subset['Sequence']]
subset['AlignedLength'] = [len(x) for x in subset['Aligned']]
(ggplot(subset, aes('AlignedLength')) + geom_histogram())

def pullNuc(seq, i):
  if len(seq) > i:
    return seq[i]
  else:
    return '-'

matrix = pd.DataFrame()
for i in range(nchar):
  matrix[i] = pd.Series([pullNuc(seq, i) for seq in subset['Sequence']])

def entropy(nucs):
  vcs = nucs.value_counts(1)
  total = 0
  for i in range(len(vcs)):
    total = total + (vcs[i]*log(vcs[i], 2))
  return -total

perNucleotide = pd.DataFrame()
perNucleotide['location'] = [i for i in range(nchar)]
perNucleotide['entropy'] = [entropy(matrix[i]) for i in range(nchar)]

# Distribution of Entropies

(ggplot(perNucleotide, aes('entropies')) + geom_histogram())

# Entropy Per Position

(ggplot(perNucleotide, aes('index', 'entropies')) + geom_col())
