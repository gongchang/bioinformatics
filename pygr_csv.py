#!/usr/bin/env python
from optparse import OptionParser
from pygr import worldbase

def pygr_csv():
    """usage example:
            pygr_csv.py -i pygr_in.csv -o pygr_out.csv
    (1)pygr_in.csv format:
        name,chromosome,start,end
        seq1,chr7,10042,10052
        seq2,chr8,999932,999942
    
    (2)pygr_out.csv format:
        name,sequence,5p_flank,3p_flank
        seq1,ctaaccctaa,ccctaaccctaaccctaacc,ccctaaccctaaccctaacc
        seq2,cacgtggata,cagacacatgcatatgtaca,tatgcacacacatgctgtca

    """
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_filename")
    parser.add_option("-o", "--output", dest="output_filename")
    (options, args) = parser.parse_args()

    input_file=open(options.input_filename,'r')
    input_lines=input_file.readlines()[1:]
    
    output_file=open(options.output_filename,'w')
    Header="name,sequence,5p_flank,3p_flank\n"
    output_file.write(Header)
    
    hg19 = worldbase.Bio.Seq.Genome.HUMAN.hg19()
    current_line=1
    for line in input_lines:
        record=line.strip(" \r\n").split(",")
        if len(record)==4:
            name=record[0]
            chrom=record[1]
            start=int(record[2])
            end=int(record[3])
            if chrom in hg19:
                sequence=hg19[chrom][start:end]
                flank5=hg19[chrom][start-20:start]
                flank3=hg19[chrom][end:end+20]
                new_record="%s,%s,%s,%s\n" %(name,sequence,flank5,flank3)
                output_file.write(new_record)
        else:
            print "corrupted input record,%s,current_line:%s\n" %(line,current_line)
            break
        current_line+=1
    
    
if __name__=="__main__":
    pygr_csv()
