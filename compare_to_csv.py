#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.stats import ks_2samp
import numpy as np

def get_index_date_ad_save_together():
    # Creates files streaming
    file_one = None
    file_two = None

    """
    # Read the source file with previously separated lines 
    """
    file_one = open('separate_lines.csv','r')
    
    mjd_one  = []
    yyyymmdd = []
    vlr_s1   = []
    sig_s1   = []
    
    with file_one as f1:
        for line in f1:
            splits = line[:-1].split(',')
            mjd_one.append(splits[0])
            yyyymmdd.append(splits[1])
            vlr_s1.append(float(splits[2]))
            sig_s1.append(float(splits[3]))
    file_one.close()

    """
    # Read the source file with interpolated data 
    """
    file_two = open('file-interpolated-rounded.csv','r')
    mjd_two  = []
    vlr_s2   = []
    sig_s2   = []
    
    file_two.readline() # skip 1st line
    #file_two.readline() # skip 2nd line
    with file_two as f2:
        for line in f2:
            splits = line[:-1].split(',')
            mjd_two.append(splits[0])
            vlr_s2.append(float(splits[2]))
            sig_s2.append(float(splits[3]))
    file_two.close()
    
    """
     Compare
    """
    mjd = []
    dts = []
    fd1 = []
    er1 = []
    fd2 = []
    er2 = []
    
    c = 0
    for c in range(len(mjd_one)):
        x = 0
        for x in range(len(mjd_two)):
            if mjd_one[c] in mjd_two[x]:
                mjd.append(mjd_one[c])
                dts.append(yyyymmdd[c])
                fd1.append(float(vlr_s1[c]))
                er1.append(float(sig_s1[c]))
                fd2.append(float(vlr_s2[x]))
                er2.append(float(sig_s2[x]))
                #print('{0},{1},{2} {3:5.2f},{4:5.2f},{5:5.2f},{6:5.2f}'.format(mjd_one[c],mjd_two[x],yyyymmdd[c],vlr_s1[c],sig_s1[c],vlr_s2[x],sig_s2[x]))
            
    """
    # Write list
    
    """
    outf = open('final_to_evaluate_with_k-s-test.csv','w')
    outf.write('mjd,date,Soriginal,sigSoriginal,Scalc,sigScalc\n')
    c = 0
    for c in range(len(mjd)):
        outf.write('{0},{1},{2:5.2f},{3:5.2f},{4:5.2f},{5:5.2f}\n'.format(mjd[c], dts[c], fd1[c], er1[c], fd2[c], er2[c]))
    
    outf.close()
    
    """
     Kolmogorov-Smirnov Test
    """
    result_ks = ks_2samp(fd1,fd2)
    print(result_ks)
    
    fne = open('k-s_test.txt','w')
    fne.write('# Kolmogorov-Smirnov Test\n')
    fne.write('# statistic={0} pvalue={1}\n'.format(result_ks[0],result_ks[1]))
    fne.close()

    return 


def main():
    get_index_date_ad_save_together()
    return


if __name__ == "__main__":
    main()

