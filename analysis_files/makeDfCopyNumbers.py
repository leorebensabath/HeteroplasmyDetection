import pandas as pd
import glob
import pickle 

df = pd.DataFrame(columns = ['sample_name', 'av_autosomal_depth', 'av_mitochondrial_depth', 'copy_number'])
files = glob.glob("/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/batch*/coverageInfos/*")
for file in files :
    print("entre________________________")
    print(file)
    with open(file, 'r') as f :
        line = f.readline()
        print(line)
    infos = line.split()
    print(infos)
    df = df.append({'sample_name' : infos[0], 'av_autosomal_depth' : infos[1], 'av_mitochondrial_depth' : infos[2], 'copy_number' : infos[3]}, ignore_index=True)  

with open('/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/copyNumberDf.pickle', 'wb') as file :
    myPickler = pickle.Pickler(file)
    myPickler.dump(df)
