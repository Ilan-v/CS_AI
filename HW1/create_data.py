import ember
import pandas as pd
from tqdm import tqdm
import pickle
import os
tqdm.pandas()

def create_vectorized_data(data_dir):
    """
    Create the data files for the ember dataset.

    Args:
        data_dir (str): The directory to save the data files to.
    """
    ember.create_vectorized_features(data_dir, 1)
    _ = ember.create_metadata(data_dir)

def extract_features(df,metadata_columns):
    """
    Extract the features from the ember dataset.
    Args:
        df (pandas.DataFrame): The dataframe to extract the features from.
        metadata_columns (list): The columns to keep from the dataframe.
    """
    df = df.copy()
    # flatten general data, and save the dataframe with the metadata
    print('Extracting general data...')
    df_general = pd.concat([df.drop(['general'], axis=1)[metadata_columns], df['general'].progress_apply(pd.Series)], axis=1)
    # flatten strings data
    print('Extracting strings data...')
    df_strings = pd.concat([df_general, df['strings'].progress_apply(pd.Series)], axis=1)
    # remove printabledist column
    df_strings = df_strings.drop(['printabledist'], axis=1)
    return df_strings


def create_train_data(imports_dir, processed_dir):
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
    for i in range(len(files)):
        print(f'Processing file: train_features_{i+1}.jsonl')
        df = pd.read_json(files[i], lines=True)
        processed_df = extract_features(df,metadata_columns)
        processed_df.to_parquet(f'{processed_dir}/train_features_{i+1}.parquet')


def create_test_data(filepath, processed_dir):
    df = pd.read_json(filepath, lines=True)
    metadata_columns = ['sha256', 'md5', 'appeared', 'label', 'avclass']
    processed_df = extract_features(df,metadata_columns)
    processed_df.to_parquet(f'{processed_dir}/test.parquet')

def concat_train_data(data_dir):
    """
    Concatenate the tabular data for analysis.

    Args:
        data_dir (str): The directory to pull the data from.
    """
    # create list of data files paths
    files = [f'{data_dir}/train_features_{i}.parquet' for i in range(1, 6)]
    # run through the files and create the dataframe (with tqdm for progress)
    df = pd.concat([pd.read_parquet(f) for f in tqdm(files)])
    # save dataframe to pickle
    df.to_parquet(f'{data_dir}/train.parquet')

def build_train_data(imports_dir,processed_dir):
    """
    Build the tabular training data for analysis.

    Args:
        imports_dir (str): The directory to pull the data from.
        processed_dir (str): The directory to save the data files to.
    """
    # create tabular data
    create_train_data(imports_dir, processed_dir)
    # concatenate tabular data
    concat_train_data(processed_dir)


if __name__ == '__main__':
    # create the tabular data
    data_dir = os.path.join(os.getcwd(),'HW1\\data')
    processed_dir = os.path.join(data_dir,'processed')
    build_train_data(data_dir,processed_dir)
    create_test_data(f'{data_dir}/test_features.jsonl', processed_dir)
    