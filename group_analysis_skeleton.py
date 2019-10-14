#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    path="C:\\Users\\emily\\Documents\\GitHub\\ps2-emilyschwartzman18"
    #added this as a timesaver, because python is not recognizing files from the local directory without full path
    source=path+"\\testingroom"+room
    destination=path+"\\rawdata\\"
    os.rename(source+"\\experiment_data.csv",source+"\\experiment_data_"+room+".csv")
    shutil.copy(source+"\\experiment_data_"+room+".csv",destination)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    tmp=sp.loadtxt(path+'\\rawdata\\experiment_data_'+room+'.csv',delimiter=',')
    data=np.vstack([data,tmp])


#%%
# calculate overall average accuracy and average median RT
#
acc_avg=np.mean(data,axis=0)[3] # 91.48%
    
mrt_avg=np.mean(data,axis=0)[4] # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
wordcount=0
wordacc_sum=0
wordmrt_sum=0
faceacc_sum=0
facemrt_sum=0
facecount=0
for x in range(len(data)):#for each row of data
    if data[x,1]==1:#if stimulus is faces
        wordacc_sum=wordacc_sum+data[x,3]
        wordmrt_sum=wordmrt_sum+data[x,4]
        wordcount=wordcount+1
    else:
        faceacc_sum=faceacc_sum+data[x,3]
        facemrt_sum=facemrt_sum+data[x,4]
        facecount=facecount+1
wordacc_avg=wordacc_sum/wordcount
wordmrt_avg=wordmrt_sum/wordcount
faceacc_avg=faceacc_sum/facecount
facemrt_avg=facemrt_sum/facecount

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.mean(data[data[...,2]==1],axis=0)[3]  # 94.0%
acc_bp = np.mean(data[data[...,2]==2],axis=0)[3]  # 88.9%
mrt_wp = np.mean(data[data[...,2]==1],axis=0)[4]  # 469.6ms
mrt_bp = np.mean(data[data[...,2]==2],axis=0)[4] # 485.1ms


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
wrdat=data[data[...,1]==1] #word data
fcdat=data[data[...,1]==2] #face data

mrt_wrwp=np.mean(wrdat[wrdat[...,2]==1],axis=0)[4] #words - white/pleasant
mrt_wrbp=np.mean(wrdat[wrdat[...,2]==2],axis=0)[4] #words - black/pleasant
mrt_fcwp=np.mean(fcdat[fcdat[...,2]==1],axis=0)[4] #faces - white/pleasant
mrt_fcbp=np.mean(fcdat[fcdat[...,2]==2],axis=0)[4] #faces - black/pleasant

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats as stats
stats.ttest_rel(wrdat[wrdat[...,2]==1][...,4],wrdat[wrdat[...,2]==2][...,4],axis=0)
stats.ttest_rel(fcdat[fcdat[...,2]==1][...,4],fcdat[fcdat[...,2]==2][...,4],axis=0)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORD STIMULI: {:.2f}%, {:.1f} ms'.format(wordacc_avg*100,wordmrt_avg))
print('FACE STIMULI: {:.2f}%, {:.1f} ms'.format(faceacc_avg*100,facemrt_avg))
print('\nWHITE/PLEASANT CONDITION: {:.2f}%, {:.1f} ms'.format(acc_wp*100,mrt_wp))
print('BLACK/PLEASANT CONDITION: {:.2f}%, {:.1f} ms'.format(acc_bp*100,mrt_bp))
print('\nWHITE/PLEASANT WORD RTs: {:.1f} ms'.format(mrt_wrwp))
print('BLACK/PLEASANT WORD RTs: {:.1f} ms'.format(mrt_wrbp))
print('WHITE/PLEASANT FACE RTs: {:.1f} ms'.format(mrt_fcwp))
print('BLACK/PLEASANT FACE RTs: {:.1f} ms'.format(mrt_fcbp))
print('\nT TEST - WHITE/PLEASANT FACE RTs VS BLACK/PLEASANT FACE RTs: t={:.2f}, p={:.5f}'.format(stats.ttest_rel(wrdat[wrdat[...,2]==1][...,4],wrdat[wrdat[...,2]==2][...,4],axis=0)[0],stats.ttest_rel(wrdat[wrdat[...,2]==1][...,4],wrdat[wrdat[...,2]==2][...,4],axis=0)[1]))
print('\nT TEST - WHITE/PLEASANT WORD RTs VS BLACK/PLEASANT WORD RTs: t={:.2f}, p={:.4f}'.format(stats.ttest_rel(fcdat[fcdat[...,2]==1][...,4],fcdat[fcdat[...,2]==2][...,4],axis=0)[0],stats.ttest_rel(fcdat[fcdat[...,2]==1][...,4],fcdat[fcdat[...,2]==2][...,4],axis=0)[1]))