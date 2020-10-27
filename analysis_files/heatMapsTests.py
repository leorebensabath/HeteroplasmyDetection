import pandas as pd
import glob
import pickle
import seaborn
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np

tissue = 30
sex = 1

files = glob.glob(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_*.pickle')
len(files)
df_stats = pd.DataFrame()
df_p_values = pd.DataFrame()

if len(files) == 4 :
    for time_point in time_points :
        with open(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', "rb") as f:
            df = pickle.load(f)
            df.index = df.index.astype(int)
            df = df[df["p_value"] < 0.05]
            df.drop("bonf", axis = 1)
            df_stats = pd.concat([df_stats, df["stat_value"]], axis = 1, join = 'outer')
            df_p_values = pd.concat([df_p_values, df["p_value"]], axis = 1, join = 'outer')
            df_stats = df_stats.rename(columns = {'stat_value' : dic_time_points[time_point]})
            df_p_values = df_p_values.rename(columns = {'p_value' : dic_time_points[time_point]})

    df_stats = df_stats.fillna(0)
    df_p_values = df_p_values.fillna(1)

x = np.array([1, 2, 4, 8]).reshape((-1, 1))
for elt in df.index :
    y = list(df_stats.loc[elt])
    reg = LinearRegression().fit(x, y)
    plt.scatter(x, y)
    plt.plot(x, reg.predict(x), color = "red")
    plt.show()

########################################################################################################################
tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]
time_points = [8, 9, 10, 11]
dic_time_points = {8 : '1w', 9 : '2w', 10 : '4w', 11: '8w'}

i = 0
for tissue in tissues :
    for sex in sexs :

        files = glob.glob(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_*.pickle')
        len(files)
        df_stats = pd.DataFrame()
        df_p_values = pd.DataFrame()

        if len(files) == 4 :
            for time_point in time_points :
                with open(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', "rb") as f:
                    df = pickle.load(f)
                    df.index = df.index.astype(int)
                    df = df[df["p_value"] < 0.05]
                    df.drop("bonf", axis = 1)
                    df_stats = pd.concat([df_stats, df["stat_value"]], axis = 1, join = 'outer')
                    df_p_values = pd.concat([df_p_values, df["p_value"]], axis = 1, join = 'outer')
                    df_stats = df_stats.rename(columns = {'stat_value' : dic_time_points[time_point]})
                    df_p_values = df_p_values.rename(columns = {'p_value' : dic_time_points[time_point]})

            df_stats = df_stats.fillna(0)
            df_p_values = df_p_values.fillna(1)

            #fg = seaborn.clustermap(df_stats, cmap = "coolwarm")
            #fg.title(f'T : {tissue} - TP : {time_point}')
            #fg.fig.set(xlabel='Time point', ylabel='Locations')
            #fg.fig.suptitle(f'T : {tissue} - TP : {time_point}')
            #plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/clusterMapVariants/{tissue}_{sex}.png')
            i+=1
df_stats
plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/heatMapVariants/all_cluster.png')

########################################################################################################################
tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]
time_points = [8, 9, 10, 11]
dic_time_points = {8 : '1w', 9 : '2w', 10 : '4w', 11: '8w'}

fig, axs = plt.subplots(6, 6)
fig.set_figheight(25)
fig.set_figwidth(30)
i = 0
for tissue in tissues :
    for sex in sexs :

        files = glob.glob(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_*.pickle')
        len(files)
        df_stats = pd.DataFrame()
        df_p_values = pd.DataFrame()

        if len(files) == 4 :
            for time_point in time_points :
                with open(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', "rb") as f:
                    df = pickle.load(f)
                    df.drop("bonf", axis = 1)
                    df_stats = pd.concat([df_stats, df["stat_value"]], axis = 1, join = 'outer')
                    df_p_values = pd.concat([df_p_values, df["p_value"]], axis = 1, join = 'outer')
                    df_stats = df_stats.rename(columns = {'stat_value' : dic_time_points[time_point]})
                    df_p_values = df_p_values.rename(columns = {'p_value' : dic_time_points[time_point]})

            df_stats = df_stats.fillna(0)
            df_p_values = df_p_values.fillna(1)

            map_p_value = df_p_values<0.05
            map_index_p_value = map_p_value.any(axis = 1)
            map_p_value_reduced = map_p_value[map_index_p_value]

            df_stats_reduce = df_stats[map_index_p_value]

            map_stats = df_stats_reduce[map_p_value_reduced].fillna(0)
            map_stats[map_stats < 0] = -1
            map_stats[map_stats > 0] = 1

            map_stats.index = map_stats.index.map(int)
            map_stats = map_stats.sort_index(axis = 0)

#            seaborn.heatmap(map_stats, cmap = "coolwarm")
            seaborn.heatmap(map_stats, cmap = "coolwarm", ax = axs[i//6, i%6])
#            seaborn.clustermap(map_stats, cmap = "coolwarm", ax = axs[i//6, i%6])

#            plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/heatMapVariants/{tissue}_{sex}.png')
#            plt.clf()
            i+=1

plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/code/stat_study_manual/heatMapVariants/all_cluster.png')

#df_stats = df_stats.any(map_p_value)
#df_stats[map_p_value].fillna(False).
#seaborn.clustermap(map_stats_reduce, col_cluster = False, cmap = "Spectral")

#seaborn.clustermap(df_stats, col_cluster = False, cmap = "Spectral")
#seaborn.clustermap(df_p_values, col_cluster = False)
#seaborn.clustermap(a, col_cluster = False, cmap = "Spectral")

########################################################################################################################

tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]
time_points = [8, 9, 10, 11]

fig, axs = plt.subplots(8, 9)
fig.set_figheight(50)
fig.set_figwidth(50)
i = 0

'''
with open('/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/70_2_1_11.pickle', 'rb') as file1:
    df1 = pickle.load(file1)
with open('/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/70_2_2_11.pickle', 'rb') as file2:
    df2 = pickle.load(file2)

df1 = df1[df1['p_value']<0.05]
df2 = df2[df2['p_value']<0.05]
'''
sex_dic = {1 : "male", 2 : "female"}
for tissue in tissues :
    for time_point in time_points :
        files = glob.glob(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_*_{time_point}.pickle')
        df_stats = pd.DataFrame()
        df_p_values = pd.DataFrame()

        if len(files) == 2 :
            for sex in sexs :
                with open(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/dfTestPickleFile/{tissue}_2_{sex}_{time_point}.pickle', "rb") as f:
                    df = pickle.load(f)
                    df.drop("bonf", axis = 1)
                    df_stats = pd.concat([df_stats, df["stat_value"]], axis = 1, join = 'outer')
                    df_p_values = pd.concat([df_p_values, df["p_value"]], axis = 1, join = 'outer')
                    df_stats = df_stats.rename(columns = {'stat_value' : sex_dic[sex]})
                    df_p_values = df_p_values.rename(columns = {'p_value' : sex_dic[sex]})

            df_stats = df_stats.fillna(0)
            df_p_values = df_p_values.fillna(1)

            map_p_value = df_p_values<0.05
            map_index_p_value = map_p_value.any(axis = 1)
            map_p_value_reduced = map_p_value[map_index_p_value]

            df_stats_reduce = df_stats[map_index_p_value]

            map_stats = df_stats_reduce[map_p_value_reduced].fillna(0)
            map_stats[map_stats < 0] = -1
            map_stats[map_stats > 0] = 1

            map_stats.index = map_stats.index.map(int)
            map_stats = map_stats.sort_index(axis = 0)

#            seaborn.heatmap(map_stats, cmap = "coolwarm")

            seaborn.heatmap(map_stats, cmap = "coolwarm", ax = axs[i//9, i%9])
            axs[i//9, i%9].set_title(f'T : {tissue} - TP : {time_point}')
#            seaborn.clustermap(map_stats, cmap = "coolwarm", ax = axs[i//6, i%6])
#            plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/heatMapVariants_sex/{tissue}_{time_point}.png')
#            plt.clf()
            i+=1

plt.savefig(f'/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/results_pass1B/all_cluster_sex.png')
