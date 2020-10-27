import glob
import pandas as pd
import pickle
import collections

tissues = [30, 31, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
sexs = [1, 2]

for tissue in tissues :
    for sex in sexs :

        files = glob.glob(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/dfTestPickleFile/{tissue}_2_{sex}_*.pickle')

        if len(files) == 4 :

            dic = {}
            dic_results = {"case_locations":[], "control_locations":[]}
            for file in files :
                with open(file, "rb") as f:
                    file_infos = file.split('/')[-1].replace('.pickle', '').split('_')
                    time_point = int(file_infos[3])

                    dic[time_point] = {}

                    df = pickle.load(f)
                    df = df.reset_index()
                    df = df.astype({"location": int})
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

                    dic_results["case_locations"] += dic[time_point]["case locations"]
                    dic_results["control_locations"] += dic[time_point]["control locations"]

            case_occurrences = collections.Counter(dic_results["case_locations"])
            control_occurrences = collections.Counter(dic_results["control_locations"])

            casesLocations = list(dict(filter(lambda elem: elem[1] >= 2, case_occurrences.items())).keys())
            controlLocations = list(dict(filter(lambda elem: elem[1] >= 2, control_occurrences.items())).keys())

            significantLocations = casesLocations + controlLocations
            significantLocations = [str(elt) for elt in significantLocations]
            
            with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/annotatedVcfTissue/{tissue}_{sex}', 'r') as file:
                df_annotations = pd.DataFrame(columns = ['Location', 'Consequence'])
                output_lines = []
                for line in file :
                    if line[0] == '#':
                        output_lines.append(line)
                    if line[0] != '#':
                        line_list = line.split()
                        location = line_list[0].split('_')[1]
                        if location in significantLocations : 
                            output_lines.append(line) 

            with open(f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/annotatedVcfTissueSignificant/{tissue}_{sex}.vcf', 'w') as output_file:
                for line in output_lines : 
                   output_file.write(line)        
                   
