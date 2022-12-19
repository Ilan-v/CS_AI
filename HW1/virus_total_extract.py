import pandas as pd
import os
import json
from tqdm import tqdm

def extract_data_from_file(filepath: str):
    """
    extract data from a json file to a dataframe
    """
    with open(filepath) as f:
        data = json.load(f)
    df = pd.DataFrame(data.keys(), columns = ['sha256'])
    df['num_undetected'] = df['sha256'].apply(lambda x: data[x]['data']['attributes']['last_analysis_stats']['undetected'])
    df['num_malicious'] = df['sha256'].apply(lambda x: data[x]['data']['attributes']['last_analysis_stats']['malicious'])
    df['num_harmless'] = df['sha256'].apply(lambda x: data[x]['data']['attributes']['last_analysis_stats']['harmless'])
    df['trid'] = df['sha256'].apply(lambda x: data[x]['data']['attributes']['trid'])
    return df

def build_vt_data(dir: str, dataset_name: str):
    """
    build a dataframe with all the data from the json files
    """
    print(f'Building {dataset_name} data...')
    # get the list of json files
    data_dir = os.path.join(dir, dataset_name)
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    # extract data from the first file
    df = extract_data_from_file(os.path.join(data_dir, json_files[0]))
    # loop over the rest of the files
    for f in tqdm(json_files[1:]):
        df = pd.concat([df, extract_data_from_file(os.path.join(data_dir, f))], ignore_index = True)
    # save the dataframe
    df.to_csv(os.path.join(dir, f'{dataset_name}_vt_data.csv'), index = False)

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    virustotal_path = os.path.join(dir_path,'data\\virustotal')
    build_vt_data(virustotal_path, 'test')
    build_vt_data(virustotal_path, 'train')