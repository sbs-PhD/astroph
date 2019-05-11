#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys

"""
 Count lines in a csv file
"""
def count_line(filename):
    return len(open(filename).readlines()) - 1 # line 1 is header
    
"""
 Sorts the line numbers in a given range and saves them to a file
"""
def sort_line(num_lines):
    quant = num_lines // 4
    
    my_randoms = random.sample(range(1, num_lines), quant)
    my_randoms.sort()
    
    #print(my_randoms)
    #print("N. lines: {0} N. Selected: {1}".format(num_lines, quant))
    #print("Min: {0} Max: {1} Sum: {2}".format(min(my_randoms), max(my_randoms), sum(my_randoms)))
    
    # Save the list
    outf = None
    outf = open('selected_lines.lst','w')
    for num in my_randoms:
        outf.write('{0:d}\n'.format(num))
    outf.close()
    return

"""
 Separates selected from the original time series
"""
def separate_test(filename):
    inf = None
    inf = open('selected_lines.lst','r')
    my_randoms = []
    with inf as f:
        for line in f:
            my_randoms.append(int(line))
    inf.close()
    #print(my_randoms)
    
    outf1 = None
    outf2 = None
    inf = None
 
    inf = open(filename,'r')
    inf.readline() # skip 1st line
    
    outf1 = open('separate_lines.csv','w')
    outf2 = open('to_filled_lines.csv','w')
    with inf as f:
        for i, line in enumerate(f):
            if (i+1) in my_randoms:
                #print(i+1)
                # save the file to be compared after
                outf1.write(line)
            else:
                # save the file to be filled
                outf2.write(line)
    inf.close()
    outf1.close()
    outf2.close()
    return


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
                filename = str(sys.argv[1])
                num = count_line(filename)
                sort_line(num)
                separate_test(filename)
                print('Read successfully...')
            else:
                print('Error: Use {0} datafilename'.format(str(sys.argv[0])))
                return 0
        except (EnvironmentError) as err:
            print('Error {0}'.format(err))

    return 0

if __name__ == "__main__":
    sys.exit(main())

