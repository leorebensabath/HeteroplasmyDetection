import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_called/*.vcf')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.vcf', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/filterMutect2/batch{i}/fm2_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name={i}_{j}\n\
#SBATCH --time=00:30:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/filterMutect2_out/batch{i}/fm2_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_filtered\n')
            cmdFile.write('ml java\n')

            cmd = f'/oak/stanford/groups/euan/tools/gatk/gatk-4.1.3.0/gatk FilterMutectCalls \\\n\
-R /oak/stanford/groups/euan/projects/leore_mtdna/Rattus_norvegicus.Rnor_6.0.dna.toplevel.v9.fa \\\n\
--autosomal-coverage 2 \\\n\
--mitochondria-mode \\\n\
-V {file} \\\n\
-O /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_filtered/{file_name}.filtered.vcf\n'

            cmdFile.write(cmd)

