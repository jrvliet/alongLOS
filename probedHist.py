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

figa, ((ax11a, ax12a), (ax21a, ax22a)) = plt.subplots(2, 2, figsize=(10.2, 10.2))
figb, ((ax11b, ax12b), (ax21b, ax22b)) = plt.subplots(2, 2, figsize=(10.2, 10.2))
axesa = [ax11a, ax12a, ax21a, ax22a]
axesb = [ax11b, ax12b, ax21b, ax22b]

numLOS = 999
numbins = 20

for ion in ion_list:
    print ion 
    axa = axesa[ion_list.index(ion)]    
    axb = axesb[ion_list.index(ion)]    

    for galID, lab in zip(gal_list, lab_list):

        counts = np.zeros(numLOS)
        norms = np.zeros(numLOS)
        listfile = '{0:s}.{1:s}.list'.format(galID, ion)
        flist = open(abscellLoc+'individual/'+listfile)
        filecount = 0.
        for fline in flist:
            filecount += 1.
            a = fline.split('.')[1]+'.'+fline.split('.')[2]

            # Get the number of cells along each LOS
            numCells = np.zeros(numLOS)
            numCellFilename = '{0:s}_{1:s}_numCellsAlongLOS.dat'.format(galID,a)
            fnum = open(abscellLoc+'individual/'+numCellFilename)
            fnum.readline()
            for numline in fnum:
                l = numline.split()
                losnum = int(l[0])
                num = int(l[1])
                numCells[losnum-1] = num
            fnum.close()


            # Get the number of absorbing cells along each LOS
            count = np.zeros(numLOS)        

            # Read in the file
            f = open(abscellLoc+'individual/'+fline.strip())
            f.readline()
            for line in f:
                losnum = int(line.split()[0])
                count[losnum-1] += 1
            f.close()

            # Normalize the number of absorbing cells by the 
            # total number of cells along the LOS
            norm = np.zeros(numLOS)
            for i in range(0,len(count)):
                norm[i] = count[i]/numCells[i]
            
            # Add these to the running total
            for i in range(0,len(count)):
                counts[i] += count[i]
                norms[i] += norm[i]

        for i in range(0,len(counts)):
            counts[i] = counts[i]/filecount
            norms[i] = norms[i]/filecount
        axa.hist(counts, bins=numbins, log=True, histtype='step', label=lab)
        axb.hist(norms, bins=numbins, log=True, histtype='step', label=lab)

    axa.set_xlabel('Number of Absorbing Cells along LOS')
    axa.set_ylabel('Frequency')
    axa.set_title(ion)
    axa.legend(frameon=False, loc='upper right')

    axb.set_xlabel('# Absorbing Cells along LOS / # Cells along LOS')
    axb.set_ylabel('Frequency')
    axb.set_title(ion)
    if ion=='HI':
        axb.legend(frameon=False, loc='upper left')
    else:
        axb.legend(frameon=False, loc='upper right')
        

figa.tight_layout()
s = 'numSigCellsAlongLOS.png'
figa.savefig(s)

figb.tight_layout()
s = 'numSigCellsAlongLOS_normed.png'
figb.savefig(s)





