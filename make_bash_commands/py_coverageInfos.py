import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/depths/*.txt')

    n = len(files)
    print(len(files))

    for j in range(n) :
        file = files[j]
        sample_name = file.split('/')[-1].split('.')[0]
        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/coverageInfos/batch{i}/cov_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name=arg\n\
#SBATCH --time=03:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=32G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/coverageInfos_out/batch{i}/cov_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/coverageInfos\n')
            cmdFile.write('ml py-numpy/1.18.1_py36\nml py-pandas/1.0.3_py36\n')
            cmd = f'python3 /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/pythonScripts/getCopyNumber.py {file}'

            cmdFile.write(cmd)
