# ------------------
# IMPORTS
# ------------------
import json
import os
from zipfile import ZipFile
import shutil
from pathlib import Path

from setup_update import ReturnUser
import dir_paths as dp
import yaml

def unzip_and_extract(manager: ReturnUser):
    """
    This function performs the following tasks:
        1. For a given directory, locate and unzip the zipped data folder.
        2. Once unzipped, moves out the contents from it, into the directory
    """
    working_dir = manager.proj_dirpath

    b4_cont = os.listdir(working_dir)

    # Determining the Zip File Path in the Directory
    for ind, f in enumerate(b4_cont):
        print(f"{ind}:{f}")

    f_ind = int(input("Enter the Index for the Zip Folder: "))
    f_path = os.path.join(working_dir, b4_cont[f_ind])
    z = ZipFile(f_path)
    z.extractall(path=working_dir)
    z.close()

    af8_cont = os.listdir(working_dir)

    unzip_fold_name = list(map(str,set(af8_cont).difference(set(b4_cont))))
    unzip_fold_path = [os.path.join(working_dir,x) for x in unzip_fold_name]

    # Extracting out of the Zipped Folder and Removing the unzipped folder
    for d in unzip_fold_path:
        for f in os.listdir(d):
            f_path = os.path.join(working_dir, d, f)
            shutil.move(f_path, working_dir)

    # Empty Folder Removal
    for d in unzip_fold_path:
        os.rmdir(path=d)

def copy_template(prob_type: int, manager: ReturnUser):
    """
    Case-Specific .ipynb template been copied to the working directory of the project
    """
    with open(dp.config_path, 'r') as f:
        template_folder = yaml.safe_load(f)["defaults"]["templates_dir"]
        path = yaml.safe_load(f)["json_files"]["templates_names"]
        with open(path, 'r') as jf:
            template_dict = json.load(jf)

    for k,v in template_dict.items():
        if v == prob_type:
            temp_file_ky = k
            full_temp_file = Path(k).with_suffix(".ipynb")

            file_src = os.path.join(template_folder, full_temp_file)
            shutil.move(file_src, manager.proj_dirpath)
