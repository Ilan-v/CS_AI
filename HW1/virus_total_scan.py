import requests
import json
import pandas as pd
import os
import time
from tqdm import tqdm
# Ilan's API key
from vt_api_key import api_key

def get_remaning_daily_quota(api_key):
    """
    Get the remaining daily quota for the user.
    """
    url = f"https://www.virustotal.com/api/v3/users/{api_key}/overall_quotas"

    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    response = requests.get(url, headers=headers)
    user_daily_quota = response.json()['data']['api_requests_daily']['user']
    used = user_daily_quota['used']
    allowed = user_daily_quota['allowed']
    return allowed - used

def create_batches(start_index, df_size):
    num_avilable_requests = get_remaning_daily_quota(api_key)
    num_requests = 0 
    batches = []
    while num_requests < num_avilable_requests and start_index < df_size:
        batch_samples = min([1000, num_avilable_requests - num_requests, df_size - start_index])
        end_index = start_index + batch_samples 
        batches.append(range(start_index, end_index))
        num_requests += 1000
        start_index = end_index
    return batches

def add_files(dir: str, api_key: str, dataset_name: str):
    """
    get more files from virustotal
    """
    df_path = os.path.join(dir,f'{dataset_name}_file_status.csv')
    json_path = os.path.join(dir,f'{dataset_name}_file_data.json')
    
    status_df = pd.read_csv(df_path)
    with open(json_path, 'r') as f:
        data_dic = json.load(f)
    # index of the first file to be added
    start_index = status_df[status_df['status_code'] == 0].index[0]
    # create batches
    batches = create_batches(start_index, len(status_df))
    # loop over the batches
    for b in range(len(batches)):
        for idx in tqdm(batches[b], desc = f"batch {b}"):
            sha256 = status_df.loc[idx, 'sha256']
            # get response
            url = f"https://www.virustotal.com/api/v3/files/{sha256}"
            headers = {
                "accept": "application/json",
                "x-apikey": api_key
            }
            response = requests.get(url, headers=headers)
            # update status and timestamp
            status_df.loc[idx, 'timestamp'] = pd.Timestamp.now()
            status_df.loc[idx, 'status_code'] = response.status_code
            # save response json
            data_dic[sha256] = response.json()

        # save progress
        status_df.to_csv(df_path, index=False)
        with open(json_path, 'w') as f:
                json.dump(data_dic, f)

# different paths
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path,'data')
processed_path = os.path.join(data_path,'processed')
virustotal_path = os.path.join(data_path,'virustotal')

if __name__ == '__main__':
    add_files(virustotal_path, api_key, dataset_name='train')