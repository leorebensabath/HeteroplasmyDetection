import glob

files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/chrM/batch*/*')

with open('cmd_chrM.sh', 'w') as file:
        file.write('#!/bin/bash\n\
#SBATCH --job-name=chrM\n\
#SBATCH --time=00:10:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n')

        for elt in files:
                file.write(f'sbatch {elt}\n')
