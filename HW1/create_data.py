import ember
import pandas as pd
from tqdm import tqdm
import pickle
import os

def create_vectorized_data(data_dir):
    """
    Create the data files for the ember dataset.

    Args:
        data_dir (str): The directory to save the data files to.
    """
    ember.create_vectorized_features(data_dir, 1)
    _ = ember.create_metadata(data_dir)

def create_train_data(imports_dir, exports_dir):
    """
    Create the tabular data for analysis.

    Args:
        imports_dir (str): The directory to pull the data from.
        exports_dir (str): The directory to save the data files to.
    """
    # create list of data files paths
    files = [f'{imports_dir}/train_features_{i}.jsonl' for i in range(1, 6)]
    metadata_columns = ['sha256', 'md5', 'appeared', 'label', 'avclass']
    # run through the files and create the dataframe (with tqdm for progress)
    for i in tqdm(range(len(files))):
        df = pd.read_json(files[i], lines=True)
        # flatten general data, and save the dataframe with the metadata
        df_general = pd.concat([df.drop(['general'], axis=1)[metadata_columns], df['general'].apply(pd.Series)], axis=1)
        # save dataframe to pickle
        df_general.to_pickle(f'{exports_dir}/train_features_{i+1}.pkl')


def open_file(file_path):
    df = pd.read_json(file_path, lines=True)
    return df

if __name__ == '__main__':
    # create the tabular data
    data_dir = os.path.join(os.getcwd(),'HW1\\data')
    processed_dir = os.path.join(data_dir,'processed')
    create_train_data(data_dir, processed_dir)
    