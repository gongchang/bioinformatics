#!/usr/bin/env python
import sys

def sam_count(filename):
    file1=open(filename,'r')
    lines=file1.readlines()
    sum1=0 #sum1 represents all reads
    sum2=0 #sum2 represents all non-aligned reads
    sum3=0 #sum3 represents all aligned reads that have an edit distance of 0
    sum4=0 #sum4 represents all aligned reads that have an edit distance >=1
    for line in lines:
        list1=line.split('\t')
        if line.find('ILLUMINA')==0:
            sum1=sum1+1
            if len(list1)==12:
                sum2=sum2+1
            elif len(list1)==14:
                if int(list1[13].split("\n")[0].split(":")[2])==0:
                    sum3=sum3+1
                else:
                    sum4=sum4+1
                    
    print "all reads,non-aligned reads,aligned reads,perfect reads,reads with one or more mismatch:",sum1,sum2,sum1-sum2,sum3,sum4

if __name__=="__main__":
    sam_count(sys.argv[1])
    
    
