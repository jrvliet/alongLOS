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

    for a in expn:

        loc = '{0:s}_outputs/a{1:s}/cellIDs/'.format(galID, a)
        
        for i in range(1,1000):
            filename = 'los{0:4d}.cellID.dat'.format(i)
            print filename
            sys.exit()
        
