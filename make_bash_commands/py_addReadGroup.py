import glob

for i in range(1, 6) :
    files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/*.bam')

    n = len(files)

    for j in range(n) :
        file = files[j]
        file_name = file.split("/")[-1].replace('.bam', '')
        sample_name = file.split("/")[-1].split(".")[0]

        with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/addReadGroup/batch{i}/rg_{j}_{sample_name}.sh', 'w') as cmdFile :
            cmdFile.write(f'#!/bin/bash\n\
#SBATCH --job-name=arg\n\
#SBATCH --time=00:30:00\n\
#SBATCH --ntasks=1\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem-per-cpu=16G\n\
#SBATCH --out=/oak/stanford/groups/euan/projects/leore_mtdna/whole_pipeline_pass1B/addReadGroup_out/batch{i}/rg_{j}_{sample_name}.out\n')

            cmdFile.write(f'mkdir -p /oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/read_group_added\n')
            cmdFile.write('ml java\nml biology\nml samtools\n')

            cmd = f'java -jar /oak/stanford/groups/euan/tools/picard/picard.jar AddOrReplaceReadGroups \\\n\
I={file} \\\n\
O=/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch{i}/read_group_added/{file_name}.rg.bam \\\n\
RGLB=lib1 \\\n\
RGPL=ILLUMINA \\\n\
RGPU=unit1 \\\n\
RGSM={sample_name} \\\n\
CREATE_INDEX=true \\\n\
REFERENCE_SEQUENCE=/oak/stanford/groups/euan/projects/leore_mtdna/Rattus_norvegicus.Rnor_6.0.dna.toplevel.v9.fa\n'

            cmdFile.write(cmd)
