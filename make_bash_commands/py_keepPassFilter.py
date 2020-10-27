import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_filtered/*.vcf')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.vcf', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/keepPassFilter/batch{i}/fm2Pass_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name={i}_{j}\n\
#SBATCH --time=00:30:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/keepPassFilter_out/batch{i}/fm2Pass_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/pass_filter\n')
            cmdFile.write('ml java\nml biology\nml bcftools\n\n')

            cmd = f'bcftools view -i \'FILTER="PASS"\' {file} > /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/pass_filter/{file_name}.pass.vcf\n'

            cmdFile.write(cmd)
