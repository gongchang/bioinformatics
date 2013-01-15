#!/usr/bin/env python
import sys

def csv_to_fasta(csv_file,fasta_file):
    """a .csv file is converted into a fasta file
      the first column of the .csv file is turned into the id,
      and the second column of the .csv file is turned into the seq
    """
    file1=open(csv_file,"r")
    lines=file1.readlines()
    
    file2=open(fasta_file,"w")
    
    #each line ends with "\r" and thus all rows are read as a single string
    if len(lines)==1:
        records=lines[0].split("\r")
        for sequence in records:
            record=sequence.strip(" \r\n").split(",")
            id=record[0]
            #print id
            seq=record[1]
            file2.write(">%s\n%s\n" %(id,seq))
    else:
        for line in lines:
            record=line.strip(" \r\n").split(",")
            id=record[0]
            seq=record[1]
            file2.write(">%s\n%s\n" %(id,seq))
    

if __name__=="__main__":
    csv_to_fasta(sys.argv[1],sys.argv[2])
