import glob

files = glob.glob("/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mergeFiles_noSex/*")

with open('cmd_mergeFiles_noSex.sh', 'w') as file:
        file.write('#!/bin/bash\n\
#SBATCH --job-name=mergeFiles_noSex\n\
#SBATCH --time=00:30:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n')

        for elt in files:
                file.write(f'sbatch {elt}\n')
