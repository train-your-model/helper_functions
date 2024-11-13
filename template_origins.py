import argparse
import os
import shutil
import process_file as pf

# Instantiate
parser = argparse.ArgumentParser()

# Arguments
parser.add_argument('site_name', choices=['MH', 'ZN', 'KG', 'AI', 'AV'],
                    help='Name of the Website containing the Project')
parser.add_argument('working_directory', help='Name of the Project Folder')
parser.add_argument('problem_type', type=int, help='1- Tabular Regression, 2- Tabular Classification')

# Parsing
args = parser.parse_args()

# Abbreviation Dictionary
abb_dict = {'MH': "MachineHack",
            'ZN': "Zindi",
            'KG': "Kaggle",
            'AI': "AI_Crowd",
            'AV': "Analytics Vidya"}

# Working Directory Creation
path = os.path.join(pf.read_config(sec='Base_Directories', ky='hackathon_parent_dir'),
                    abb_dict.get(args.site_name), args.working_directory)

os.mkdir(path)
return_to_previous_state = 0

# Template Copying into the Working Directory
try:
    if args.problem_type == 2:
        file_source = pf.read_config(sec='Templates', ky='tabular_classification_file')
        file_dest = str(path)+"\\"
        shutil.copy2(file_source, file_dest)

except PermissionError:
    return_to_previous_state = 1
    print("Template File has NO required permissions to be copied onto the Project Working Directory")

finally:
    if return_to_previous_state == 1:
        os.rmdir(path)
        print("The Newly Created Directory has been DELETED due to exception.")

    else:
        print("Working Directory has been created and the relevant template has been copied successfully.")
