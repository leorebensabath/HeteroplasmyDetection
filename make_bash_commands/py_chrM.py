import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/*.bam')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.bam', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/chrM/batch{i}/chrM_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name={i}_{j}\n\
#SBATCH --time=00:15:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/chrM_out/batch{i}/{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/chrM\n')
            cmdFile.write('ml java\nml biology\nml samtools\n')
            cmdFile.write(f'samtools view {file} chrM > /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/chrM/{file_name}.chrM.bam')
