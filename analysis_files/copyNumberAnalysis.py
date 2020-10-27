import pickle
from scipy.stats import ranksums
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open('/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/pheno_viallabel-data.pickle', 'rb') as file :
    df1 = pickle.load(file)
df1
with open('/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/pickle/copyNumberDf.pickle', 'rb') as file :
    df2 = pickle.load(file)
    df2 = df2.set_index('sample_name')
len(df2)
len(df1)
list(df2["av_mitochondrial_depth"])
np.mean([float(df2["av_mitochondrial_depth"][i]) for i in range(len(df2))])
df1 = df1.loc[list(df2.index)]

sexes = [1, 2]
time_points = [8, 9, 10, 11]
tissues = [30, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]

df = pd.DataFrame(columns = ['tissue', 'time_point', 'sex', 'stat_value', 'p_value'])

for sex in sexes :
    for time_point in time_points :
        for tissue in tissues :
            sampleCandidates_case = list(df1.loc[(df1['pass1bf0009'] == str(2)) & (df1['pass1bf0027'] == str(sex)) & (df1['pass1bf0010'] == str(time_point))].index)
            samples_case = list(filter(lambda x: x[7:9] == str(tissue), sampleCandidates_case))

            sampleCandidates_control = list(df1.loc[(df1['pass1bf0009'] == str(3)) & (df1['pass1bf0027'] == str(sex)) & (df1['pass1bf0010'] == str(11))].index)
            samples_control = list(filter(lambda x: x[7:9] == str(tissue), sampleCandidates_control))
            print("samples_case: ", samples_case)
            print("samples_control: ", samples_control)
            copyNumber_case = list(df2.loc[samples_case]['copy_number'])
            copyNumber_control = list(df2.loc[samples_control]['copy_number'])
            print(copyNumber_case, "  ", copyNumber_case)
            if (len(copyNumber_case)!=0)&(len(copyNumber_control)!=0) :
                stat_value, p_value = ranksums(copyNumber_case, copyNumber_control)
                df = df.append({'tissue' : int(tissue), 'time_point' : int(time_point), 'sex' : int(sex), 'stat_value' : stat_value, 'p_value' : p_value}, ignore_index=True)

plt.hist(df["p_value"], bins = 20)
plt.xticks(np.arange(0, 1, 0.1))
line = plt.axvline(0.05, color = "red", linewidth=2)
plt.xlabel("p values")
plt.ylabel("counts")
plt.savefig("/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/results_pass1B/copyNumbersPvalues.png")

df.sort_values(["p_value"])

plt.hist(df["stat_value"], bins = 20)
plt.xticks(np.arange(-3, 3, 0.5))
#line = plt.axvline(0.05, color = "red", linewidth=2)
plt.xlabel("Stat value")
plt.ylabel("counts")
plt.savefig("/Users/leore/Desktop/AshleyLabProject/mtdna/code/stat_study_manual/results_pass1B/copyNumbersStatValues.png")
