import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/N_cigar_splitted/*.bam')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.bam', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mutect2/batch{i}/m2_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name={i}_{j}\n\
#SBATCH --time=03:00:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=32G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/mutect2_out/batch{i}/m2_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_called\n')
            cmdFile.write('ml java\n')

            cmd = f'/oak/stanford/groups/euan/tools/gatk/gatk-4.1.3.0/gatk Mutect2 \\\n\
-R /oak/stanford/groups/euan/projects/leore_mtdna/Rattus_norvegicus.Rnor_6.0.dna.toplevel.v9.fa \\\n\
-L chrM --mitochondria-mode \\\n\
-I {file} \\\n\
-O /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/mutect2_called/{file_name}.vcf \n'

            cmdFile.write(cmd)
