def fetch_from_competition(competition_name:str, path:str):
    """
    Fetches data from a kaggle competition and saves it to a specified path
    """
    import kaggle
    kaggle.api.authenticate()
    kaggle.api.competition_download_files(competition_name, path=path, quiet=False)

def unzip_data(path:str):
    """
    Unzips data from a specified path
    """
    import zipfile
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("data/raw")

def clean_zips(path:str):
    """
    Deletes all zip files from a specified path
    """
    import os
    for file in os.listdir(path):
        if file.endswith(".zip"):
            os.remove(os.path.join(path, file))

def make_cats_and_dogs(path:str, remove_residuals=True):
    """
    Fetches and unzips data from the dogs-vs-cats kaggle competition
    """
    COMPETITION_NAME = "dogs-vs-cats"
    fetch_from_competition(COMPETITION_NAME, path)

    print("Unzipping data...")
    unzip_data(f"{path}/{COMPETITION_NAME}.zip")
    unzip_data(f"{path}/train.zip")
    unzip_data(f"{path}/test1.zip")

    if remove_residuals:
        clean_zips(path)

def make_denoise(path:str):
    """
    https://www.kaggle.com/datasets/rajat95gupta/smartphone-image-denoising-dataset
    """
    COMPETITION_NAME = "rajat95gupta/smartphone-image-denoising-dataset"
    fetch_from_competition(COMPETITION_NAME, path)

    print("Unzipping data...")
    unzip_data(f"{path}/smartphone-image-denoising-dataset.zip")

AVAILABLE_DATASETS = {
    "cats_and_dogs": make_cats_and_dogs,
    "denoise": make_denoise,
}

if __name__ == "__main__":
    # Read in command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="The dataset to fetch", type=str)
    parser.add_argument("--path", help="The path to save the data to", type=str, default="data/raw")
    args = parser.parse_args()

    # Fetch the dataset
    if args.dataset in AVAILABLE_DATASETS:
        AVAILABLE_DATASETS[args.dataset](args.path)
    else:
        raise Exception(f"Dataset {args.dataset} not available")