import pickle
import glob
import pandas as pd
import numpy as np
from os import path
import random as rd
import collections

df_summary = pd.DataFrame(columns = ['Tissue', 'Sex', 'Size inter = 2', 'Size inter = 3', 'Size inter = 4'], dtype = 'int')

#files = glob.glob(f'/Users/leore/Desktop/AshleyLabProject/code/plink_study/stat_study_manual/pickle/{tissue}_2_{sex}_*.pickle')

tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]
num_iter = 1000000

for tissue in tissues :
    for sex in sexs :
        print("tissue : ", tissue)
        print("sex : ", sex)
        files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/dfTestPickleFile/{tissue}_2_{sex}_*.pickle')

        if len(files) == 4 :
            dic = {}

            for file in files :
                with open(file, "rb") as f:
                    file_infos = file.split('/')[-1].replace('.pickle', '').split('_')
                    time_point = int(file_infos[3])
                    dic[time_point] = {}

                    df = pickle.load(f)
                    df = df.reset_index()
                    df = df.astype({"location": int})

                    dic[time_point]["locations"] = list(df["location"])

                    i = 0
                    i_case = 0
                    while (df.loc[i]['p_value'] <= 0.05):
                        if (df.loc[i]['stat_value'] >= 0.0):
                            i_case += 1
                        i += 1
                    j = 0
                    j_control = 0

                    while (df.loc[j]['p_value'] <= 0.05) :
                        if (df.loc[j]['stat_value'] <= 0.0) :
                            j_control += 1
                        j += 1

                    locations_pos = df["location"][:i_case+j_control][df['stat_value'][:i+j]>0]
                    locations_neg = df["location"][:i_case+j_control][df['stat_value'][:i+j]<0]

                    dic[time_point]["case locations"] = list(locations_pos)
                    dic[time_point]["control locations"] = list(locations_neg)

            dic_count_inter = {1: [], 2: [], 3: [], 4: []}
            for i in range(num_iter) :
                dic_simulations = {}
                dic_results = {"case_locations":[], "control_locations":[]}
                for time_point in range(8, 12) :
                    locations = dic[time_point]["locations"]
                    case_locations = dic[time_point]["case locations"]
                    control_locations = dic[time_point]["control locations"]

                    dic_simulations[time_point] = {}

                    n_case = len(case_locations)
                    n_control = len(control_locations)
                    simulations = rd.sample(locations, n_case + n_control)
                    case_simulation = simulations[:n_case]
                    control_simulation = simulations[-n_control:]

                    dic_simulations[time_point]["case_simulation"] = case_simulation
                    dic_simulations[time_point]["control_simulation"] = control_simulation

                    dic_results["case_locations"] += case_simulation
                    dic_results["control_locations"] += control_simulation

                dic_results["case_locations"]
                case_occurrences = collections.Counter(dic_results["case_locations"]).values()
                control_occurences = collections.Counter(dic_results["control_locations"]).values()
                case_count_intersect = collections.Counter(case_occurrences)
                control_count_intersect = collections.Counter(control_occurences)

                count_intersect = {}
                for key in np.union1d(list(case_count_intersect.keys()), list(control_count_intersect.keys())) :
                    count_intersect[key] = case_count_intersect.get(key, 0) + control_count_intersect.get(key, 0)
                dic_simulations
                for key in count_intersect :
                    dic_count_inter[key].append(count_intersect[key])

            dic_prob = {}

            for i in range(2, 5) :
                dic_prob[i] = {}
                counter = collections.Counter(dic_count_inter[i])
                dic_prob[i][0] = (num_iter - len(dic_count_inter[i]))/num_iter
                if len(dic_count_inter[i]) != 0 :
                    for j in range(1, max(dic_count_inter[i])+1):
                         dic_prob[i][j] = counter[j]/num_iter
                else :
                    dic_prob[i][0] = 1.0

            df_summary = df_summary.append({"Tissue": tissue, "Sex": sex, "Size inter = 2": dic_prob[2], "Size inter = 3": dic_prob[3], "Size inter = 4": dic_prob[4]}, ignore_index = True)

df_summary

df_summary = df_summary.sort_values(['Tissue', 'Sex'])
df_summary = df_summary.astype({"Tissue": "int32", "Sex": "int32"})
df_summary.to_csv('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/testSummaryBootstrap.csv', index = False)

#p values from bootstrap distributions#######################################################################################################################
path_intersection = '/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/results_pass1B/testSummaryIntersection.csv'
path_bootstrap = '/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/results_pass1B/testSummaryBootstrap.csv'

df_intersection = pd.read_csv(path_intersection, sep=',', delimiter=None, header=0)
df_bootstrap = pd.read_csv(path_bootstrap, sep=',', delimiter=None, header=0)

df_intersection.insert(3, "2: p value", value = [0.0 for i in range(len(df_intersection))])
df_intersection.insert(5, "3: p value", value = [0.0 for i in range(len(df_intersection))])
df_intersection.insert(7, "4: p value", value = [0.0 for i in range(len(df_intersection))])

for i in range(len(df_intersection)) :
    for j in [2, 3, 4] :
        size_intersection = int(df_intersection.loc[i][f'{j}'])
        assert((df_intersection.loc[i]["Tissue"] == df_bootstrap.loc[i]["Tissue"])&(df_intersection.loc[i]["Sex"] == df_bootstrap.loc[i]["Sex"]))

        distribution = df_bootstrap.loc[i][f'Size inter = {j}']
        distribution = ast.literal_eval(distribution)
        if size_intersection in distribution.keys() :
            p_value = sum(distribution[k] for k in range(size_intersection, max(distribution.keys())+1))
        else :
            p_value = 0.0
        df_intersection.at[i, f'{j}: p value'] = round(p_value, 5)

df_intersection = df_intersection.set_index(["Tissue", "Sex"])

df_intersection.to_csv('/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/results_pass1B/bootstrap_p_values.csv', index = False)

def color_negative_red(val):
    color = 'yellow' if val < 0.05 else None
    return 'background-color: %s' % color

df_intersection = df_intersection.style.applymap(color_negative_red, subset=['2: p value', '3: p value', '4: p value'])

df_intersection.to_excel('/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/results_pass1B/bootstrap_p_values.xlsx')

