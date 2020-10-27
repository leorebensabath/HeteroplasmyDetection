import glob

files = glob.glob("/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mutect2/batch4/*")
print(len(files))
with open('cmd_mutect2.sh', 'w') as file:
    file.write('#!/bin/bash\n\
#SBATCH --job-name=mutect2\n\
#SBATCH --time=00:30:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n')

    for elt in files:
        path = elt[:83]
        file.write(f'cd {path}\n')
        file.write(f'sbatch {elt[84:]}\n')
