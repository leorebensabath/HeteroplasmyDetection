import pickle
import glob
import pandas as pd

files = glob.glob('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/dfTestPickleFile/*.pickle')

df_summary = pd.DataFrame(columns = ['tissue', 'sex', 'time_point', 'nb of variants', 'p values < 0.05 Case', 'p values < 0.05 Control'])

for file in files :
    with open(file, "rb") as f:
        file_infos = file.split('/')[-1].replace('.pickle', '').split('_')

        df_test = pickle.load(f)
        df_test = df_test.reset_index()
        i = 0
        i_case = 0
        while (df_test.loc[i]['p_value'] <= 0.05):
            if (df_test.loc[i]['stat_value'] >= 0.0):
                i_case += 1
            i += 1
        j = 0
        j_control = 0
        while (df_test.loc[j]['p_value'] <= 0.05) :
            if (df_test.loc[j]['stat_value'] <= 0.0) :
                j_control += 1
            j += 1
        
        infos = {'tissue' : file_infos[0], 'sex' : int(file_infos[2]), 'time_point' : int(file_infos[3]),  'nb of variants' : len(df_test), 'p values < 0.05 Case' : i_case, 'p values < 0.05 Control' : j_control}

        df_summary = df_summary.append(infos, ignore_index=True)


df_summary = df_summary.sort_values(['tissue', 'time_point', 'sex'])
print(df_summary)
df_summary.to_csv('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/testSummary.csv', index = False)

