import glob

files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/results/*')

n = len(files)

for j in range(n) :

    file = files[j]
    file_name = file.split("/")[-1]

    with open(file, 'r') as f :
        vcf_files = f.read().splitlines()

    with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mergeFiles/{file_name}.sh', 'w') as cmdFile :

        cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name=arg\n\
#SBATCH --time=01:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mergeFiles_out/{file_name}.out\n')

        cmdFile.write('ml java\nml biology\nml vcftools\n')

        for vcf_file in vcf_files :
	    
            cmdFile.write(f'bgzip {vcf_file}\n')
            cmdFile.write(f'tabix -f -p vcf {vcf_file}.gz \n')

        cmdFile.write('vcf-merge \\\n')

        for vcf_file in vcf_files :
            cmdFile.write(vcf_file + '.gz \\\n')
        cmdFile.write(f'--ref-for-missing 0/0 > /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/mergedFiles/{file_name}.vcf')
