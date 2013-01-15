import sys
def blast_process(filename,output_filename):
    lines=open(filename,'r')
    file=open(output_filename,'w')
    s=set('')
    for line in lines:
        if line.split()[0] in s:
            pass
        else:
            s.add(line.split()[0])
            if int(line.split()[3])<18:
                pass
            else:
                file.write(line)


if __name__=="__main__":
    blast_process(sys.argv[1],sys.argv[2])
                
    



