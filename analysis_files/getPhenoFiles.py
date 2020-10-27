import glob
import numpy as np
import sys
import pickle

def getSamplesPass1B(tissue, group, sex, time_point) :
    '''
    tissue : [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
              67, 68, 69, 70]
    group : Training - 2 ; Control - 3
    sex : Male -1 ; Female - 2
    time_point : [8, 9, 10, 11]
    8 : 1 week of training or control time (Phase 1B)
    9 : 2 weeks of training (Phase 1B)
    10 : 4 weeks of training (Phase 1B)
    11 : 8 weeks of training or control time (Phase 1B)
    '''
    with open('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/pheno_viallabel-data.pickle', 'rb') as file :
        df = pickle.load(file)

    files = glob.glob('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch*/pass_filter/*.vcf')

    return_files = []

    sampleCandidates = list(df.loc[(df['pass1bf0009'] == str(group)) & (df['pass1bf0027'] == str(sex)) & (df['pass1bf0010'] == str(time_point))].index)

    samples = list(filter(lambda x: x[7:9] == str(tissue), sampleCandidates))

    with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/results/{tissue}_{group}_{sex}_{time_point}', 'w') as result_file:
        for file in files:
            vial_label =  file.split("/")[-1].split(".")[0]
            if vial_label in samples :
                result_file.write(file + '\n')

if __name__ == "__main__":
    tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    groups = [2, 3]
    sexs = [1, 2]
    time_points = {2 : [8, 9, 10, 11], 3 : [11]}

    for tissue in tissues :
        for group in groups :
            for sex in sexs :
                for time_point in time_points[group] :
                    files = getSamplesPass1B(tissue, group, sex, time_point)
