import os
import pandas as pd
import csv

one_val_cols_list = ['@module', '@class', 'barcode', 'protocol', 'channel_id', '@version']
NaN_cols_list = ['diagnostic_summary', 'diagnostic_interpolated']

def transform_data():
    '''
    Transformation of the JSON files (one file per battery) into
    csv with concatenate data for a given measurement
    '''

    #path of the files when doing the transformation
    dir_path = os.path.dirname(__file__)
    initial_data_path = os.path.join(dir_path, "..", "..", "raw_data", "initial_data")
    initial_data_path = os.path.normpath(initial_data_path)
    transformed_data_path = os.path.join(dir_path, "..", "..", "raw_data", "transformed_data")
    transformed_data_path = os.path.normpath(transformed_data_path)

    # files names to transform
    onlyfiles = [f for f in os.listdir(initial_data_path) if f[-1] != 'r']

    # definition of the shape of the 1st file
    first_file_path = os.path.join(initial_data_path, onlyfiles[0])
    df = pd.read_json(first_file_path)
    indexes_list = df.index
    column_list = df.columns

    initialize_files(df, transformed_data_path)
    i = 0

    for file_name in onlyfiles:
        '''
        reading each JSON file, and spread data into multiple csv files
        data dispatching is done by add_line method
        '''
        file_path = os.path.join(initial_data_path, file_name)
        df = pd.read_json(file_path)
        valide_shape(df,indexes_list,column_list,one_val_cols_list,NaN_cols_list)
        add_lines(df,transformed_data_path)
        print(f"File {i}")
        i += 1

def valide_shape(df,indexes,cols,one_val_cols,NaN_cols):
    '''validate that the file has the same shape as the 1st file opened'''
    assert(df.index.all() == indexes.all())
    assert(df.columns.all() == cols.all())
    for col in one_val_cols:
        assert(len(set(df[col].values))== 1)
    for col in NaN_cols:
        assert(df[col].isna().sum()== 21)

def initialize_files(df, path):
    '''creation of the csv files with headers'''
    file_path = os.path.join(path, 'test_details.csv')
    with open(file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=one_val_cols_list)
        writer.writeheader()
    # for values in df.index:
    #     file_path = os.path.join(path, f"summary_{values}.csv")
    #     with open(file_path, 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=['barcode'] +[i for i in range(0,3000)])
    #         writer.writeheader()
    # for values in df.index:
    #     file_path = os.path.join(path, f"cycles_interpolated_{values}.csv")
    #     with open(file_path, 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=['barcode'] +[i for i in range(0,3000)])
    #         writer.writeheader()

def add_lines(df,path):
    '''add in each csv file, one line of data (one per battery)'''
    file_path = os.path.join(path, 'test_details.csv')

    dict = {}
    for val in one_val_cols_list:
        dict[val] = df[val].iloc[0]
    dict['barcode'] = dict['barcode'].upper()

    with open(file_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dict.keys())
        writer.writerow(dict)

    for values in df.index:
        if isinstance(df['summary'][values], float) == False:
            file_path = os.path.join(path, f"summary_{values}.csv")
            with open(file_path, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([df['barcode'].iloc[0]] + df['summary'][values])

    for values in df.index:
        if isinstance(df['cycles_interpolated'][values], float) == False:
            file_path = os.path.join(path, f"cycles_interpolated_{values}.csv")
            with open(file_path, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([df['barcode'].iloc[0]] + df['cycles_interpolated'][values])

    print("file written")


transform_data()