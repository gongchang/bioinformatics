#!/usr/bin/env python
#these barcodes need to be reverse_complemented to produce the real barcode

#L1BCS=['GACTCA','GTACAC','GCATGT','TCAGAG','TACGCA','TGATGC','CGTATC','CATCGA','CTGCAT','ATGTCA']
#L1BC1,2,3,4,5,6,7,8,9,10
#L1=['TGAGTC','GTGTAC','ACATGC','CTCTGA','TGCGTA','GCATCA','GATACG','TCGATG','ATGCAG','TGACAT']

#these linker sequences are already reverse_complemented
#linker1='CTGTAGGCACCATCAAT'
#linker3='TTTAACCGCGAATTCCAG'

import sys
from fasta import *

def multiplex_parse(input_filename,*output_filenames):
    """this script is used to separate the .fasta files barcoded in the 3'adaptor
    """
    
    #output_files should contain sample files,bad_adaptor, bad_barcode,adaptor_ligation
    
    #one bad adaptor file (no 3' adaptor is detected, either the sequences are too long or there are mutations in)
    #and one bad barcode file (no barcode detected or there are mutations in the barcode)
    #and one adaptor file,just 5'adaptor-3'adaptor ligation products
    
    #the structure of the read looks like: miRNA_seq+3'adaptor+Barcode+PCR_seq,
    #RC(reverse complement) of 3'adaptor seq:GTAGGCACCATCAAT for linker-1
    #the RC of the barcodes are shown below in the list "multiplex"
    
    linker1="CTGTAGGCACCATCAAT"#length=17
    #linker2="CACTCGGGCACCAAGGA"#length=17
    #linker3="TTTAACCGCGAATTCCAG"#length=18
    
    #barcodes before reverse complement:
    #['GACTCA','TCAGAG','CGTATC','GTACAC','GCATGT','TACGCA','TGATGC','CATCGA','CTGCAT','ACTGAC','AGCATA']
    multiplex_linker1=['TGAGTC','CTCTGA','GATACG','GTGTAC','ACATGC','TGCGTA','GCATCA','TCGATG','ATGCAG','GTCAGT','TATGCT']

    #WM239A_Ago1IP,WM239A_Ago2IP,WM239A_Ago3IP,0517_Ago1IP,0812_Ago1IP,0504_Ago2IP,0517_Ago2IP,0805_Ago3IP,0812_Ago3IP,0805_Ago3IP_dKO,0812_Ago3IP_dKO
    #multiplex2_linker1=['TGAGT','CTCTG','GATAC','GTGTA','ACATG','TGCGT','GCATC','TCGAT','ATGCA','GTCAG','TATGC']
    #multiplex3_linker1=['TGAG','CTCT','GATA','GTGT','ACAT','TGCG','GCAT','TCGA','ATGC','GTCA','TATG']
    
    outputs=[]#
    for i in range((len(output_filenames))):
        outputs.append(open(output_filenames[i],'w'))
    
    records=Fasta(input_filename)
    for key in records.keys():
        sequence=records[key][0:]
        index1=sequence.find(linker1)    
        #outputs[28]: bad_adaptor, outputs[29]: bad_barcode, outputs[30]: adaptor_ligation
        if index1>0 and index1<=27:
            #index+17(length_of_linker1)+6 should  be less than or equal to 50(the length of the read) (in that case ,the barcode is in its full length)
    
            barcode=sequence[index1+17:index1+23]
            if barcode in multiplex_linker1:
                j=multiplex_linker1.index(barcode)
                outputs[j].write('>%s\n%s\n' % (record.id,sequence[0:index1]))
            else:
                #bad_barcode_file:
                outputs[12].write('>%s\n%s\n' % (record.id,sequence))
               
        elif index1==0:
            #outputs[30] should be adaptor_ligation_file
            outputs[13].write('>%s\n%s\n' % (record.id,sequence))
        else:
            #outputs[28] should be bad_adaptor_file
            outputs[11].write('>%s\n%s\n' % (record.id,sequence))
        

if __name__=="__main__":
    list1=["WM239A_Ago1IP","WM239A_Ago2IP","WM239A_Ago3IP","0517_Ago1IP","0812_Ago1IP","0504_Ago2IP","0517_Ago2IP","0805_Ago3IP","0812_Ago3IP","0805_Ago3IP_dKO","0812_Ago3IP_dKO"]
    list2=[i+"_01242011.fasta" for i in list1]
        
    list3=["bad_adaptor_01242011.fasta","bad_barcodes_01242011.fasta","adaptor_ligation_01242011.fasta"]
    list2.extend(list3)
    #list2:11 sample files,bad_adaptor_file,bad_barcode_file,adaptor_ligation_file
    #[0:10],[11],[12],[13]
    multiplex_parse(sys.argv[1],*list2)


