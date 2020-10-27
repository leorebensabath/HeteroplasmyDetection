import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/read_group_added/*.bam')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.bam', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/computeDepths/batch{i}/depth_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name=arg\n\
#SBATCH --time=03:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/computeDepths_out/batch{i}/depth_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/depths\n')
            cmdFile.write('ml java\nml biology\nml samtools\n')

            cmd = f'samtools depth {file} \\\n\
> /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/depths/{file_name}.txt\n'

            cmdFile.write(cmd)
