import glob
import pickle
import pandas as pd 
from scipy.stats import ranksums

def compare_AF(file1, file2) :

    with open(file1, "rb") as file1:
        group1_dic = pickle.load(file1)
        group1_lists = pickle.load(file1)
    with open(file2, "rb") as file2:
        group2_dic = pickle.load(file2)
        group2_lists = pickle.load(file2)
    keys1 = set(group1_lists.keys())
    keys2 = set(group2_lists.keys())
    locations = keys1.union(keys2)

    k1 = list(group1_lists.keys())[0]
    k2 = list(group2_lists.keys())[0]
    n1 = len(group1_lists[k1])
    n2 = len(group2_lists[k2])

    group_merged_lists = {}
    for location in locations :
        if location not in group1_lists :
            group1_lists[location] = [0 for i in range(n1)]
        if location not in group2_lists :
            group2_lists[location] = [0 for i in range(n2)]
        group_merged_lists[location] = [group1_lists[location], group2_lists[location]]


    df = pd.DataFrame(columns = ['location', 'stat_value', 'p_value', 'bonf'])
    i = 0
    n = len(locations)
    for location in locations :
        stat_value, p_value = ranksums(group1_lists[location], group2_lists[location])
        result = {'location' : int(location), 'stat_value' : stat_value, 'p_value' : p_value, 'bonf' : p_value*n}
        df = df.append(result, ignore_index = True)

    df = df.sort_values(['p_value'])
    df = df.set_index('location')
    return(group_merged_lists, df)

if __name__ == "__main__":
    dic = {}
    with open('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/mergedVcfVariantCounts.txt', 'r') as f :
        for line in f :
            line = line.split(" : ")
            dic[line[0]] = int(line[1])

    tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    groups = [2, 3]
    sexs = [1, 2]
    time_points = {2 : [8, 9, 10, 11], 3 : [11]}

    for tissue in tissues :
        for sex in sexs :
            for time_point in time_points[2] :
                if (dic[f'{tissue}_2_{sex}_{time_point}.vcf'] != 0) & (dic[f'{tissue}_3_{sex}_11.vcf'] != 0):
                    file1 = f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/AFPickleFiles/{tissue}_2_{sex}_{time_point}.pickle'
                    file2 = f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/AFPickleFiles/{tissue}_3_{sex}_11.pickle'
                    group_merged_lists, df = compare_AF(file1, file2)
                    print(df)
                    with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', 'wb') as file:

                        mon_pickler = pickle.Pickler(file)
                        mon_pickler.dump(df)
