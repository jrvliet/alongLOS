#
# Determines the number of cells along a line of sight
#

import sys

expn_list1 = '0.900 0.926 0.950 0.975 0.990 1.002'.split()
expn_list2 = '0.901 0.925 0.950 0.976 0.991 1.001'.split()
expn_list3 = '0.900 0.925 0.950 0.975 0.990 1.000'.split()
expn_list = [expn_list1, expn_list2, expn_list3]
galID_list = ['D9o2', 'D9q', 'D9m4a']

baseLoc = '/home/matrix3/jrvander/sebass_gals/dwarfs/'

for galID, expn in zip(galID_list, expn_list):
    print ''
    print galID
    for a in expn:
        print a
        loc = '{0:s}/{1:s}_outputs/a{2:s}/cellIDs/'.format(baseLoc, galID, a)
       
        outfilename = '{0:s}_{1:s}_numCellsAlongLOS.dat'.format(galID, a) 
        fout = open(loc+outfilename, 'w')
        fout.write('#LOS \t Num Cells Along\n')

        for i in range(1,1000):
            filename = 'los{0:04d}.cellID.dat'.format(i)
            cellcount = 0
            f = open(loc+filename)
            f.readline()
            for line in f:
                cellcount += 1
            f.close()

            fout.write('{0:d}\t{1:d}\n'.format(i, cellcount))
        fout.close()











