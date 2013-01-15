import sys

def fasta_extract(filename,output):
    file1=open(filename,'r')
    newfile=open(output,'w')
    
    a=0
    while 1:
        line=file1.readline()
        if not line: break
        a+=1
        if line.startswith('@HWI') and a%4==1:
            newfile.write('>%s'% (line[1:]))
        elif line[0] in ['N','A','G','C','T'] and a%4==2:
            newfile.write('%s' % line)
        else:
            pass
    file1.close()
    
    #lines=file1.readlines()
    #length=len(lines)
    #
    #for i in range(length):
    #    line=lines[i]
    #    if line.startswith('@HWI') and i%4==0:
    #        newfile.write('>%s'% line[1:])
    #    elif line[0] in ['N','A','G','C','T'] and i%4==1:
    #        newfile.write('%s' % line)
    #    else:
    #        pass

if __name__=="__main__":
    fasta_extract(sys.argv[1],sys.argv[2])
    
