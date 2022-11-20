import ember
def create_data(data_dir):
    """
    Create the data files for the ember dataset.

    Args:
        data_dir (str): The directory to save the data files to.
    """
    ember.create_vectorized_features(data_dir, 1)
    _ = ember.create_metadata(data_dir)