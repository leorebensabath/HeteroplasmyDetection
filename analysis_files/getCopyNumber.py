import sys
import numpy as np
import glob
import pandas as pd
import pickle
import sys

def avDepth(file) :
    with open(file, 'r') as file :
        print(file)
        cov_aut = []
        cov_mit = []
        for line in file :
            if line[:4] != 'chrM' :
                line = line.split()
                if int(line[2]) != 0 :
                     cov_aut.append(int(line[2]))
            elif line[:4] == 'chrM' :
               line = line.split()
               if len(line) == 3 :
                   if int(line[2]) != 0 :
                        cov_mit.append(int(line[2]))
    return(np.mean(cov_aut), np.mean(cov_mit))


if __name__ == "__main__":
    file = sys.argv[1]
    sample_name = file.split('/')[-1].split('.')[0]
    depthAuto, depthMit = avDepth(file)
    copyNumber = depthMit*2/depthAuto
    batch = file.split('/')[-3]
    file_name = file.split('/')[-1]
    output_file = f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/{batch}/coverageInfos/{file_name}'
    with open(output_file, "w") as output :
        output.write(f'{sample_name} {depthAuto} {depthMit} {copyNumber}')
