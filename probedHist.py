#
# probedHist.py
# 
# Generates two histograms
#   1) Histogram of the number of cells that create signficant absorption
#        along all the LOSs
#   2) Same, but with the number of cells divided by the number of cells
#        along that LOS


import numpy as np
import matplotlib.pyplot as plt


ion_list = ['HI', 'MgII', 'CIV', 'OVI']
gal_list = ['D9o2', 'D9q', 'D9m4a']
lab_list = ['dwSN', 'dwALL_1', 'dwALL_8']

abscellLoc = '/home/matrix3/jrvander/sebass_gals/dwarfs/abcells'
abscellLoc = '/home/jacob/research/dwarfs/abscells/'

fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2, figsize=(10.2, 10.2))

axes = [ax11, ax12, ax21, ax22]

for ion in ion_list:
    print ion 
    ax = axes[ion_list.index(ion)]    

    for galID, lab in zip(gal_list, lab_list):

        count = np.zeros(1000)        

        # Read in the file
        filename = '{0:s}.{1:s}.bulk_abscells.dat'.format(galID, ion)
        f = open(abscellLoc+filename)
        f.readline()
        for line in f:
            losnum = int(line.split()[0])
            count[losnum-1] += 1
        f.close()

        ax.hist(count, bins=15, log=True, histtype='step', label=lab)

    ax.set_xlabel('Number of Absorbing Cells along LOS')
    ax.set_ylabel('Frequency')
    ax.set_title(ion)
    ax.legend(frameon=False, loc='upper right')

plt.tight_layout()
s = 'numSigCellsAlongLOS.png'
plt.savefig(s)




