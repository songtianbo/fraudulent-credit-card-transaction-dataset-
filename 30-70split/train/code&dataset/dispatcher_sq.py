
import os

import csv

import pandas as pd

import matplotlib.pyplot as plt


from pandas.core.frame import DataFrame

import warnings
from sklearn.manifold import TSNE

from sklearn.preprocessing import StandardScaler
warnings.simplefilter('ignore')
import random

P = 'Cred_train.csv'
#P = 'creditcardsort.csv'

n = 5                         # number of output directories
file_path_set = set('')         #this is file path set contains file_path
#file_path_set_after_hash = set('')
csv_data = pd.read_csv(P)
file_d_dic_seq = {}            # seq dic of file path ex: 0:path
title =csv_data[0:0]
b_of_lines = 1920
#(32kb -b_of_lines == 60)
def gen_dir():
#os.path.abspath(os.path.dirname(os.getcwd()))   upper

    currentP = os.getcwd()
    print('currentP\t'+currentP)
    main_dispatcher_folder = currentP + '\\dispatcher_folder_credit\\'
    if not os.path.exists(main_dispatcher_folder):
        os.mkdir(main_dispatcher_folder)
    base = main_dispatcher_folder + 'output'
    i = 1
    for j in range(n):
        file_name = base + str(i)+ '.csv'
        file_path_set.add(file_name)
        if not os.path.exists(file_name):
            title.to_csv(file_name, index=False)
        i = i+1
    return file_path_set


def to_seq_dic(file_path_set):
    index = 0
    #file_d_dic_seq = {}
    for file_path in file_path_set:   # iterate path set to put in hash

        file_d_dic_seq[index] = file_path
        index += 1
    #file_d_dic_seq = sorted(file_d_dic_seq.keys())
    print(file_d_dic_seq)
    return file_d_dic_seq



def allot_operation_block(file_d_after_hash_sorted):

    with open(P, 'rt', encoding='UTF-8') as main_f:
        cr = csv.reader(main_f)
        next(cr)
        match_index = 0
        str_row =[]
        line_num = 1
        for row in cr:    #iter rows
            str_row.append(row)     #str_row append

            if line_num % b_of_lines == 0 or line_num == len(csv_data):
                #print(line_num,len(csv_data))
                allo_path = file_d_dic_seq.get(match_index)
                #print('linenum','???',match_index,len(file_d_dic_seq))

                with open(allo_path, 'a+', encoding='UTF-8') as newf:
                    cw = csv.writer(newf, lineterminator='\n')
                    #print('alllll',str_row)
                    number=str(line_num)
                    #str_row.append(number)
                    for insdiderow in str_row:
                        cw.writerow(insdiderow)
                str_row = []
                match_index += 1
                if match_index == len(file_d_dic_seq):
                    match_index = 0

            line_num = line_num+1
            #str_row.append('\n')


def allot_operation(file_d_after_hash_sorted):
    #l = []
    with open(P, 'rt', encoding='UTF-8') as main_f:
        cr = csv.reader(main_f)
        next(cr)
        match_index = 0
        for row in cr:
            allo_path = file_d_dic_seq.get(match_index)

            with open(allo_path, 'a', encoding='UTF-8') as newf:
                cw = csv.writer(newf, lineterminator='\n')
                cw.writerow(row) #write csv as a row
            match_index += 1
            if match_index == len(file_d_dic_seq):
                match_index = 0

def allot_operation_rand(file_d_after_hash_sorted):
    #l = []
    with open(P, 'rt', encoding='UTF-8') as main_f:
        cr = csv.reader(main_f)
        next(cr)
        #match_index = 0
        for row in cr:
            #print(row)
            #l.append(row) #list
            # str_row = "".join(row)
            # sha1_row = str_encrypt(str_row)
            # key = match(file_d_after_hash_sorted, sha1_row)
            len_dic= len(file_d_dic_seq)-1
            match_index = random.randint(0 , len_dic)
            #print(len_dic,match_index)
            allo_path = file_d_dic_seq.get(match_index)
            #print(allo_path)
            #print(str_encrypt(str4))
            with open(allo_path, 'a', encoding='UTF-8') as newf:
                cw = csv.writer(newf, lineterminator='\n')
            #for item in l:
                cw.writerow(row) #write csv as a row
            # match_index += 1
            # if match_index == len(file_d_dic_seq):
            #     match_index = 0


def allot_operation_block_rand(file_d_after_hash_sorted):

    with open(P, 'rt', encoding='UTF-8') as main_f:
        cr = csv.reader(main_f)
        next(cr)
        match_index = 0
        str_row =[]
        line_num = 1
        for row in cr:    #iter rows
            str_row.append(row)     #str_row append

            if line_num % b_of_lines == 0:
                len_dic= len(file_d_dic_seq)-1
                match_index = random.randint(0 , len_dic)
                allo_path = file_d_dic_seq.get(match_index)
                #print('linenum','???',match_index,len(file_d_dic_seq))

                with open(allo_path, 'a+', encoding='UTF-8') as newf:
                    cw = csv.writer(newf, lineterminator='\n')
                    #print('alllll',str_row)
                    number=str(line_num)
                    #str_row.append(number)
                    for insdiderow in str_row:
                        cw.writerow(insdiderow)
                str_row = []

            line_num = line_num+1
            str_row.append('\n')


def analyzation(file_d_dic_seq):
    analyze_num_d = {}
    label_counts_list = []
    i = 1
    for file_path in file_d_dic_seq.values():
        output_data = pd.read_csv(file_path, header=None)
        output_data.columns = ["text", "label"]
        short_name = file_path[-11:-4]
        analyze_num_d[short_name] = output_data.shape[0]
        label_counts = output_data['label'].value_counts()
        current_label_count = list()
        # print(label_counts)
        # order_dir_counts = label_counts.to_dict().items()
        # print(order_dir_counts,label_counts [0] )
        current_label_count.append(short_name)
        current_label_count.append(label_counts[0])
        current_label_count.append(label_counts[1])

        label_counts_list.append(current_label_count)
        sorted_label_counts = sorted(label_counts_list,key=(lambda x:x[0]))
        #print(sorted_label_counts)

    return [analyze_num_d, sorted_label_counts]

def anal_credit(file_d_dic_seq):
    analyze_num_d = {}
    label_counts_list = []
    i = 1
    for file_path in file_d_dic_seq.values():
        output_data = pd.read_csv(file_path)
        #output_data.columns = ["text", "label"]
        short_name = file_path[-11:-4]
        analyze_num_d[short_name] = output_data.shape[0]
        label_counts = output_data['Class'].value_counts()
        current_label_count = list()
        print('label_counts',label_counts)
        # order_dir_counts = label_counts.to_dict().items()
        if(len(label_counts)<2):
            label_counts = [1,1]

        current_label_count.append(short_name)
        #current_label_count.append(label_counts[0])
        current_label_count.append(label_counts[1])

        label_counts_list.append(current_label_count)
        sorted_label_counts = sorted(label_counts_list,key=(lambda x:x[0]))
        #print(sorted_label_counts)

    return [analyze_num_d, sorted_label_counts]


def plot_num(analyze_d):
    sorted_analyze = sorted(analyze_d.items(), key=lambda obj: obj[0])
    print(sorted_analyze)
    plt.bar(*zip(*sorted_analyze))
    plt.show()
    #plt.bar(list(analyze_d.keys()), analyze_d.values(), color='g')




def plot_label(analyze_d):
    label = analyze_d

    mc = DataFrame(label)
    mc.reset_index()
    # mc=mc.drop(['index'], axis=1)

    mc.rename(columns={0:'name', 1:0, 2:1}, inplace = True)
    mc.set_index('name')

    print(mc)
    mc.plot.bar(x='name',stacked=True, alpha=0.5)
    plt.show()

def test():
    file_path_set = gen_dir()
    file_d_dic_seq = to_seq_dic(file_path_set)
    allot_operation(file_d_dic_seq)
    #pltsne(file_d_dic_seq)
    print(file_d_dic_seq)
    analyze_d = analyzation(file_d_dic_seq)
    #analyze_d = anal_credit(file_d_dic_seq)
    plot_num(analyze_d[0])
    print(csv_data.shape)
    plot_label(analyze_d[1])




def testrand():

    file_path_set = gen_dir()
    file_d_dic_seq = to_seq_dic(file_path_set)
    allot_operation_rand(file_d_dic_seq)
    print(file_d_dic_seq)
    #pltsne(file_d_dic_seq)
    analyze_d = analyzation(file_d_dic_seq)
    #analyze_d = anal_credit(file_d_dic_seq)
    plot_num(analyze_d[0])
    print(csv_data.shape)
    plot_label(analyze_d[1])


def testblock():

    file_path_set = gen_dir()
    file_d_dic_seq = to_seq_dic(file_path_set)
    allot_operation_block(file_d_dic_seq)
    #pltsne(file_d_dic_seq)
    print(file_d_dic_seq)

    #analyze_d = analyzation(file_d_dic_seq)
    analyze_d = anal_credit(file_d_dic_seq)
    print(analyze_d)
    #plot_num(analyze_d[0])
    print(csv_data.shape)
    plot_label(analyze_d[1])

def testblock_rand():

    file_path_set = gen_dir()
    file_d_dic_seq = to_seq_dic(file_path_set)
    allot_operation_block_rand(file_d_dic_seq)
    #pltsne(file_d_dic_seq)
    print(file_d_dic_seq)

    #analyze_d = analyzation(file_d_dic_seq)
    analyze_d = anal_credit(file_d_dic_seq)
    print(analyze_d)
    #plot_num(analyze_d[0])
    print(csv_data.shape)
    plot_label(analyze_d[1])


testblock()

#testblock_rand()




