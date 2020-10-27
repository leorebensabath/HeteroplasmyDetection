import glob

files = glob.glob("/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/bedTissueSignificant/*.bed")

with open("makeAnnotatedVcfMotrpac.sh", "w") as cmdFile :
    cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name=arg\n\
#SBATCH --time=01:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/pythonScripts/makeAnnotatedVcfMotrpac.out\n')
    cmdFile.write("ml biology\nml bedtools\n")
    for file in files :
        file_name = file.split('/')[-1][:-4]
        cmdFile.write(f'bedtools intersect -a /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/bedTissueSignificant/Rattus_norvegicus.Rnor_6.0.96.sorted.gtf -b {file} > /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/annotationMotrpac/{file_name}\n')

