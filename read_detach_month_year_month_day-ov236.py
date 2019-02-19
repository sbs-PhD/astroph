#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'SBSoltau'
__date__    = '2018-03-13'
__version__ = '1.0.0'
__email__   = 'sbsoltau@gmail.com.br'
__status__  = 'Code to read files downloaded from University Michigan Radio Astronomy Observatory Database <https://dept.astro.lsa.umich.edu/datasets/umrao.php>'
__doc__ = """
 Open the 'ov236.txt' file to read.
 Creates:
         ov236-ymd.csv : with all frequencies and the year, month day column
  ov236-ymd-048GHz.csv : with the  4.8 GHz frequency and the year, month day column
  ov236-ymd-080GHz.csv : with the  8.0 GHz frequency and the year, month day column
  ov236-ymd-145GHz.csv : with the 14.5 GHz frequency and the year, month day column
"""

import datetime
import math
import os
import string
import sys

EPSILON = 1.19209e-07

def is_equals(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def isfloat(value):
  try:
    float(value.strip())
    return True
  except ValueError:
    return False


def isint(value):
  try:
    int(value.strip())
    return True
  except ValueError:
    return False


def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


def read_detach_month_year(filename):
    # Creates files streaming
    file_in = None
    file_ou = None
    nd = ' ' # None

    try:
        """
        # 1. Read the source file and select valid lines and data
        """
        if filename[-4:] == '.txt': # or filename[-4:] is '.txt':
            filenamecsv = filename[:-4]
        else:
            filenamecsv = filename

        file_in = open(filename,'r')
        file_ou = open(filenamecsv+'-ymd.csv','w')
         
        file_ou.write('YYYY\tMM\tDD\tFreq\tUT\tS\tSigS\tN\n')

        file_in.readline() # skip 1st line
        file_in.readline() # skip 2nd line

        """
         The Database format
         Source 1921-293  OV-236           Avg. Period =    1 days  UMRAO
         YYYYMMDD\tFreq\tUT\tS\tSigS\tN\n
         19740905\t8.0\t19.588\t5.23\t0.08\t1\n
        """
        yyyy      = [] # [0]
        mm        = [] # [1]
        dd        = [] # [2]
        freq      = [] # [3]
        ut        = [] # [4]
        S         = [] # [5] two-week averages of total flux density only (S)
        sigS      = [] # [6]
        N         = [] # [7] 
        c = 0
        with file_in as f:
            for line in f:
                splits=line[:-1].split('\t')
                
                yyyymmdd = str(splits[0])
                
                yyyy.append(int(yyyymmdd[:4]))
                mm.append(int(yyyymmdd[4:6]))
                dd.append(int(yyyymmdd[6:]))
                
                if isfloat(splits[1]):
                    freq.append(float(splits[1]))
                else:
                    freq.append(nd)

                if isfloat(splits[2]):
                    ut.append(float(splits[2]))
                else:
                    ut.append(nd)

                if isfloat(splits[3]):
                    S.append(float(splits[3]))
                else:
                    S.append(nd)

                if isfloat(splits[4]):
                    sigS.append(float(splits[4]))
                else:
                    sigS.append(nd)
                
                if isint(splits[5]):
                    N.append(int(splits[5]))
                else:
                    N.append(nd)
                    
                #print('{0:03d}|{1:4d} {2:02d} {3:02d} {4:4.1f} {5:6.3f} {6:6.2f} {7:6.2f} {8:2d}'.format((c+1), yyyy[c], mm[c], dd[c], freq[c], ut[c], S[c], sigS[c], N[c]))
                file_ou.write('{0:4d}\t{1:02d}\t{2:02d}\t{3:4.1f}\t{4:6.3f}\t{5:6.2f}\t{6:6.2f}\t{7:2d}\n'.format(yyyy[c], mm[c], dd[c], freq[c], ut[c], S[c], sigS[c], N[c]))

                c += 1
                           
        file_in.close()
        file_ou.close()
    except EOFError as exception1:
        print('Caught the EOF error.')
        raise exception1
    except IOError as exception2:
        print('Caught the I/O error.')
        raise exception2
    
    """
    # 2. Checks if all frequencies 4.8, 8.0 and 14.5 GHz are present in source database file
    """

    cf048 = 0
    cf080 = 0
    cf145 = 0

    for fq in freq:
        if is_equals(fq, 4.8, EPSILON):
            cf048 += 1
            #print('{0:4.1f}'.format(fq))
        elif is_equals(fq, 8.0, EPSILON):
            cf080 += 1
            #print('{0:4.1f}'.format(fq))
        elif is_equals(fq, 14.5, EPSILON):
            cf145 += 1
            #print('{0:4.1f}'.format(fq))

    print('\nSummary:\nThere are {0} valid lines in the {1} file.'.format(c, filename))
    print('Number of lines per UMRAO radio frequencies')
    print('-'*27)
    print(' Freq.(GHz) | Number lines')
    print('-'*12 + '+' + '-'*14)
    print('     4.8    |    {0:5d}'.format(cf048))
    print('     8.0    |    {0:5d}'.format(cf080))
    print('    14.5    |    {0:5d}'.format(cf145))
    print('-'*27)

    """
    # 3.  Writes separate files csv for each 4.8, 8.0 and 14.5 GHz frequencies .
    """

    try:
        if cf048:
            file048out = open(filenamecsv+'-ymd-048GHz.csv','w')
            file048out.write('YYYY\tMM\tDD\tFreq\tUT\tS\tSigS\tN\n')
        if cf080:
            file080out = open(filenamecsv+'-ymd-080GHz.csv','w')
            file080out.write('YYYY\tMM\tDD\tFreq\tUT\tS\tSigS\tN\n')

        if cf145:
            file145out = open(filenamecsv+'-ymd-145GHz.csv','w')
            file145out.write('YYYY\tMM\tDD\tFreq\tUT\tS\tSigS\tN\n')
            
        for i in range(len(freq)):
            if cf048 and is_equals(freq[i], 4.8, EPSILON):
                file048out.write('{0:4d}\t{1:02d}\t{2:02d}\t{3:4.1f}\t{4:6.3f}\t{5:6.2f}\t{6:6.2f}\t{7:2d}\n'.format(yyyy[i], mm[i], dd[i], freq[i], ut[i], S[i], sigS[i], N[i]))
            elif cf080 and is_equals(freq[i], 8.0, EPSILON):
                file080out.write('{0:4d}\t{1:02d}\t{2:02d}\t{3:4.1f}\t{4:6.3f}\t{5:6.2f}\t{6:6.2f}\t{7:2d}\n'.format(yyyy[i], mm[i], dd[i], freq[i], ut[i], S[i], sigS[i], N[i]))
            elif cf145 and is_equals(freq[i], 14.5, EPSILON):
                file145out.write('{0:4d}\t{1:02d}\t{2:02d}\t{3:4.1f}\t{4:6.3f}\t{5:6.2f}\t{6:6.2f}\t{7:2d}\n'.format(yyyy[i], mm[i], dd[i], freq[i], ut[i], S[i], sigS[i], N[i]))

        if cf048:
            file048out.close()

        if cf080:
            file080out.close()

        if cf145:
            file145out.close()

    except EOFError as exception1:
        print('Caught the EOF error.')
        raise exception1
    except IOError as exception2:
        print('Caught the I/O error.')
        raise exception2

    return 0

"""
# Main
"""

def main(argv=None):
    if argv is None:
        argv = sys.argv
        try:
            total = len(sys.argv)

            if (total == 2):
                print ('{0} reading file {1}.'.format(str(sys.argv[0]),str(sys.argv[1])))

                #print('-'*80)
                read_detach_month_year(str(sys.argv[1]))
                #print('-'*80)

                #print('Read successfully...')

            else:
                print('Error: Use {0} datafilename'.format(str(sys.argv[0])))
                return 0
        except (EnvironmentError) as err:
            print('Error {0}'.format(err))

    return 0

if __name__ == "__main__":
    sys.exit(main())
