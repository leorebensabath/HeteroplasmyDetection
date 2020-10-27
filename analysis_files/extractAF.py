import glob
import pickle

def extract_AF(vcf_file, AF_pickle, threshold = 0.0) :

    dic = {}
    dic_lists = {}

    with open(vcf_file, 'r') as file:

        line_count = 0
        for line in file :
            if line[0] != '#':
                line_count += 1
                line = line.split('\t')
                if line[6] == 'PASS' :
                    location = int(line[1])
                    format = line[8].split(':')

                    AF_index = 0
                    while format[AF_index] != 'AF' :
                        AF_index+=1

                    genotypes = line[9:]
                    AF_sum  = 0.0
                    dic_lists[location] = []

                    for elt in genotypes :
                        if (elt[0] == '0')&(elt[2] == '1') :
                            elt = elt.split(':')

                            AF_list = elt[AF_index].split(',')
                            sum = 0
                            for AF in AF_list :
                                if AF[0] == '0' :
                                    AF = float(AF)
                                    if AF > threshold :
                                        sum += AF
                            dic_lists[location].append(sum)
                            AF_sum += sum
                        else :
                            dic_lists[location].append(0)

                    if AF_sum == 0.0 :
                        dic_lists.pop(location)
                    else :
                        dic[location] = AF_sum

    with open(AF_pickle, "wb") as file:
        mon_pickler = pickle.Pickler(file)
        mon_pickler.dump(dic)
        mon_pickler.dump(dic_lists)

    with open("/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/mergedVcfVariantCounts.txt", 'a') as f :
        f.write(f'{vcf_file.split("/")[-1]} : {line_count}\n')

    return dic_lists


if __name__ == "__main__":
    vcf_files = glob.glob("/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/mergedFiles/*.vcf")

    for vcf_file in vcf_files :
        pickle_name = vcf_file.split("/")[-1].replace("vcf", "pickle")
        pickle_file = f'/oak/stanford/groups/euan/projects/leore_mtdna/data_pass1B/AFPickleFiles/{pickle_name}'
        extract_AF(vcf_file, pickle_file)
