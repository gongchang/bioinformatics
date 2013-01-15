#!/usr/bin/env python
import sys

def macs_peaks_knowngene_overall_analysis(macs_peaks_strand_filename,knowngene_genesymbol_filename,annotated_peaks_filename,unannotated_peaks_filename):
    """
    Peak_summit is used in mapping the peaks to the genes
    (1) macs_peaks_strand_file format
    chr13	34719701	34719876	176	110	13	136.57	35.89	0	19	-
    chr13	34967509	34967562	54	28	4	101.15	64.94	4	0	+
    
    (2) knowngene_genesymbol_file format
    #name	chrom	strand	txStart	txEnd	cdsStart	cdsEnd	exonCount	exonStarts	exonEnds	GeneSymbol
    uc007aet.1	chr1	-	3195984	3205713	3195984	3195984	2	3195984,3203519,	3197398,3205713,	mKIAA1889
    uc007aeu.1	chr1	-	3204562	3661579	3206102	3661429	3	3204562,3411782,3660632,	3207049,3411982,3661579,	Xkr4

    """
    macs_file=open(macs_peaks_strand_filename,'r')
    peaks=macs_file.readlines()
    
    gene_file=open(knowngene_genesymbol_filename,'r')
    genes=gene_file.readlines()
    
    list1=[]
    for i in range(20):
        list1.append("chr%s+" % (i))
        list1.append("chr%s-" % (i))
    list1.append("chrM+")
    list1.append("chrM-")
    list1.append("chrX+")
    list1.append("chrX-")
    list1.append("chrY+")
    list1.append("chrY-")
    
    dic1={}
    for j in list1:
        dic1[j]=[]
        
    for gene in genes[1:]: #the knowngene_genesymbol_file has a header
        chr=gene.split('\t')[1]+gene.split('\t')[2] # e.g.,"chr1" + "-"
        if chr in dic1.keys():
            dic1[chr].append(gene.strip('\n').split('\t'))
            dic1[chr][-1][3]=int(dic1[chr][-1][3]) #the txStart position is like "12345" and should be stored as 12345
            dic1[chr][-1][6]=int(dic1[chr][-1][6]) #the cdsEnd position is like "12345" and should be stored as 12345
            
    annotated_peaks=open(annotated_peaks_filename,'w')
    unannotated_peaks=open(unannotated_peaks_filename,'w')
    a=0 # used to store number of unannoted peaks
    b=0 #used to store number of annotated peaks
    for line in peaks:
        peak=line.strip('\n').split('\t')
        peak_chr=peak[0]+peak[10] #e.g., "chr1"+ "-"
        peak_start=int(peak[1])
        peak_end=int(peak[2])
        peak_summit=int(peak[1])+int(peak[4])
        low=0
        high=len(dic1[peak_chr])-1
        gene_pos=return_loci(dic1[peak_chr],3,6,peak_summit,low,high)#1 and 2 denote the positions in the list for txStart and cdsEnd
        if gene_pos=="not found!":
            unannotated_peaks.write(line)
            a=a+1
        else:
            peak.append(dic1[peak_chr][gene_pos][-1])
            new_peak='\t'.join(peak)+'\n'
            annotated_peaks.write(new_peak)
            b=b+1
    
    print "unannotated peaks: %s\t and annotated peaks: %s\n" %(a,b)
    macs_file.close()
    gene_file.close()
    annotated_peaks.close()
    unannotated_peaks.close()
    
def return_loci(list1,i,j,number1,low,high):
    """given a list1 of [(...,number_a1,number_b1,...),(...,num_a2,num_b2,...),...], and a number1
       find out whether number1 is in between any number_a and number_b
       i and j denote the posion of number_a and number_b
       low starts with 0, and high starts with len(list1)-1
    """
    while low<=high:
        mid=(low+high)/2
        if list1[mid][i]>number1:
            high=mid-1
        elif list1[mid][j]<=number1:
            low=mid+1
        elif list1[mid][i]<=number1 and number1<list1[mid][j]:
            return mid
        
    return "not found!"

def return_loci_modified(list1,i,j,number1,number2,low,high):
    """given a list1 of [(...,number_a1,number_b1,...),(...,num_a2,num_b2,...),...], and a pair of number1 and number2(number1 <number2),
       find out whether number1 and number2  are contained between any number_a and number_b
       i and j denote the posion of number_a and number_b
       low starts with 0, and high starts with len(list1)-1
       
       number1 and numbers refer to the start and end position of the peak, and (number_a1,number_b1) the start and end of the gene
    """
    while low<=high:
        mid=(low+high)/2
        if list1[mid][i]>=number2 or number1<list1[mid][i]<number2:
            high=mid-1
        elif list1[mid][j]<=number1 or number1<list1[mid][j]<number2:
            low=mid+1
        elif list1[mid][i]<=number1 and number2<=list1[mid][j]:
            return mid
        
    return "not found!"

if __name__=="__main__":
    macs_peaks_knowngene_overall_analysis(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
