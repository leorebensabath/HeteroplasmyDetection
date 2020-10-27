import pickle
import os
import glob
import pandas as pd

tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]
time_points = [8, 9, 10, 11]

#tissue = 56
#sex = 1
dic = {}
with open('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/mergedVcfVariantCounts.txt', 'r') as f :
    for line in f :
        line = line.split(" : ")
        dic[line[0]] = int(line[1])

for tissue in tissues : 
    print(tissue)

i = 0
while (i < len(tissues)) :
    tissue = tissues[i]
    print("________________tissue : ", tissue)
    b = True
    for sex in sexs :
        for time_point in time_points :
            if (dic[f'{tissue}_2_{sex}_{time_point}.vcf'] == 0)&(tissue in tissues):
                tissues.remove(tissue)
                b = False
    if b : 
        i += 1

for tissue in tissues :
    for sex in sexs :

        dic_locations = {}

        for time_point in time_points :
            with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', 'rb') as file :
            #with open(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', 'rb') as file :
                df_test = pickle.load(file)
                df_test = df_test.reset_index()

                df_test = df_test.astype({"location": int})

                i = 0
                while (df_test.loc[i]['p_value'] <= 0.05):
                    i += 1
                locations = df_test["location"][:i]
                dic_locations[time_point] = list(locations)

        dic_locations

        inter_locations = []
        for elt in dic_locations :
            inter_locations += dic_locations[elt]

        inter_locations = set(inter_locations)
        len(inter_locations)
        df_result = pd.DataFrame(columns = (['Time point'] + list(inter_locations)))

        for time_point in time_points :

            with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/AFPickleFiles/{tissue}_2_{sex}_{time_point}.pickle', 'rb') as file :
            #with open(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/pickle/AFPickleFiles/{tissue}_2_{sex}_{time_point}.pickle', 'rb') as file :
                dic_scores = pickle.load(file)
                dic_list = pickle.load(file)

            insert = {'Time point' : time_point}
            for location in list(inter_locations) :
                if location in dic_scores :
                    insert[location] = dic_scores[location]
                else :
                    insert[location] = 0
            df_result = df_result.append(insert, ignore_index = True)

        df_result = df_result.astype({"Time point": "int32"})
        df_result = df_result.set_index("Time point")

        df_result.to_csv(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/timeSeriesDF/{tissue}_{sex}.csv', index = True)
