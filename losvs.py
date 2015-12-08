#!/usr/bin/python
#
# Filename: losvs.py
# Version: 1
# Created: 30/01/14
# Modified: 30/01/14
# Author: Jacob Vander Vliet
#
# Description:
#  Designed to explore the relation between a cell's posistion and
#  it's line of sight velocity. Working within an inpact parameter bin
#  it plots the distance a cell lies along the line of sight against
#  it's line of sight veloctiy. 
#
# Operation: 
#  python losvs.py <galID> <expansion parameter> <ion>
# 
# Example: 
#  python losvs.py D9m4a 0.650 CIV
#
# Notes:
#  Run from "dwarfs" folder

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from math import sqrt, pow

# Read in command line arguements
galID = sys.argv[1]
expn = sys.argv[2]
ion = sys.argv[3]

# File that contains list of cells contributing to absorption
abscellf = galID+'_'+expn+'_'+ion+'_abscells.dat'
abscell_loc = './'+galID+'_outputs/'
lines_loc = abscell_loc+'a'+expn+'/'+ion+'/'

print abscellf
print abscell_loc
print lines_loc

# Read in the abs cells file
abscells = np.loadtxt(abscell_loc+abscellf, skiprows=1)
abs_losnum = abscells[:,0]
abs_cellnum = abscells[:,2]

# Read in the lines.info file for this box 
lines_info = np.loadtxt(lines_loc+'lines.info', skiprows=2)
imp = lines_info[:,1]
phi = lines_info[:,2]

# Read in the line.dat for this box
lines_dat = np.loadtxt(lines_loc+'lines.dat', skiprows=2)
xen_dat = lines_dat[:,0]
yen_dat = lines_dat[:,1]
zen_dat = lines_dat[:,2]
xex_dat = lines_dat[:,3]
yex_dat = lines_dat[:,4]
zex_dat = lines_dat[:,5]

# Array of impact parameter bins to use
minimpact = np.arange(0.0, 1.4, 0.1)
maximpact = np.arange(0.1, 1.5, 0.1)

# Need the galaxy's virial radius
summaryf = '/home/matrix3/jrvander/galaxy_files/summaries/'+galID+'.dat'
sumf = open(summaryf)
sumf.readline()
sumf.readline()
for line in sumf:
    expansion = line.split()[0]
    if expansion==expn:
        Rvir = float(line.split()[3])
sumf.close()
print Rvir

# Read in the box for this ion and redshift
boxname = galID+'_GZa'+expn+'.'+ion+'.txt'
box = np.loadtxt(lines_loc+boxname, skiprows=2)

# Loop over impact parameter bins
for i in range(0,len(minimpact)):

    minD = minimpact[i] * Rvir
    maxD = maximpact[i] * Rvir
    
    vlos = []
    dlos = []

    # Loop over all absorbing cells
    for j in range(0,len(abs_losnum)):
        
        # Get the impact parameter for this LOS
        losnum = int(abs_losnum[j])
        D = imp[losnum-1]
        print '\nD: ', D

        # Get the entry point of this LOS
        xen = xen_dat[losnum-1]
        yen = yen_dat[losnum-1]
        zen = zen_dat[losnum-1]
        xex = xex_dat[losnum-1]
        yex = yex_dat[losnum-1]
        zex = zex_dat[losnum-1]
        
        # Get the distance from the galaxy to the entry point
        b = sqrt( pow(xen, 2) + pow(yen, 2) + pow(zen, 2) )
        print 'b: ', b

        # Get the distance from the galaxy to the exit point
        e = sqrt( pow(xex, 2) + pow(yex, 2) + pow(zex, 2) )
        print 'e: ', e

        # Get the length of the LOS
        L = sqrt( pow(xen-xex, 2) + pow(yen-yex, 2) + pow(zen-zex, 2) )
        print 'L: ', L

        # Check if this LOS is inside the limits
        if D>minD and D<maxD:

            cell = abs_cellnum[j]
            
            # Open the losdata for this LOS
            losdata = open(lines_loc+galID+'.'+ion+'.los'+str(losnum).zfill(4)+'.losdata')
            losdata.readline()
            losdata.readline()
            
            # Find the LOS velocity of the cell
            for line in losdata:
                loscellID = line.split()[27]
                if loscellID == cell:
                    vlos_cell = float(line.split()[3])
                    vlos.append(vlos_cell)
                    break
            losdata.close()

            # Get the location of the cell
            x = box[cell-1,1]
            y = box[cell-1,2]
            z = box[cell-1,3]

            print 'x: ', x
            print 'y: ', y
            print 'z: ', z

            # Get the distance from this cell to the galaxy
            f = sqrt( pow(x, 2) + pow(y, 2) + pow(z, 2))
            print 'f: ', f

            # Get the distance from the cell to the midpoint along the LOS
            c = sqrt( pow(f, 2) - pow(D, 2) )
            print 'c: ', c

            # Get the distance from the midpoint to the exit point along the LOS
            g = sqrt( pow(e, 2) - pow(D, 2) )
            print 'g: ',g

            # Get the distance from the cell to the entry point along the LOS
            a = L - c - g
            print 'a: ', a
            dlos.append(a)
            
    # Plot the data
    plt.plot(dlos, vlos, '.')
    plt.title('Min: '+minD+'\tMax: '+maxD)
    plt.xlabel('Distance along LOS')
    plt.ylabel('LOS Velocity')
    plt.savefig(galID+'_a'+expn+'_'+ion+'_'+minD+'_'+maxD+'.pdf')
