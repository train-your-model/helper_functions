import os
import shutil
import json
import argparse
import process_file as pf

# Dealing with JSONS
with open(pf.read_config(sec='JSON_Files', ky='site_names'), 'r') as abb_file:
    abb_dict = json.load(abb_file)

with open(pf.read_config(sec='JSON_Files', ky='templates_names_json'), 'r') as temp_file:
    templates_dict = json.load(temp_file)

# Instantiate
parser = argparse.ArgumentParser(description="Setting-up the Directory for Different Projects")

# Positional Arguments
parser.add_argument("site_name_abbv", help="Name of the Site containing the project")
parser.add_argument("working_dir_name", help="Name of the Case-Specific Directory")
parser.add_argument('problem_type', type=int,
                    help='1- Tabular Regression, 2- Tabular Classification, 3- Time Series Forecasting ')
parser.add_argument("target_date", type=str,
                    help="Date of Data Folder and Files Download. Date Format dd-mm-yyyy")
parser.add_argument("workbook_name", type=str,
                    help="Rename the template workbook copied into the working directory")

# Parsing
args = parser.parse_args()

# Supplementary Functions
def create_parent_dir(user_input):
    par_dir = os.path.join(pf.read_config(sec='Base_Directories', ky='hackathon_parent_dir'), user_input)
    os.mkdir(par_dir)


def create_working_directory(temp_dict, working_directory):
    work_dir = os.path.join(pf.read_config(sec='Base_Directories', ky='hackathon_parent_dir'),
                            temp_dict.get(args.site_name_abbv), working_directory)
    os.mkdir(work_dir)


def copy_template(temp_dict, template_type, file_dest):
    temp_file_ky = ''
    for k, v in temp_dict.items():
        if v == template_type:
            temp_file_ky = k

    file_src = pf.read_config(sec='Templates', ky=temp_file_ky)
    shutil.copy2(file_src, file_dest)


# Working Code
if __name__ == "__main__":
    if str(args.site_name_abbv).upper() not in abb_dict.keys():
        v_input = str(input("Enter the full name of the Site: "))
        abb_dict.update({str(args.site_name_abbv).upper(): v_input})

        # Create New Parent Directory
        create_parent_dir(user_input=v_input)
        print("New Parent Directory has been created")

        with open(pf.read_config(sec='JSON_Files', ky='site_names'), 'w') as site:
            json.dump(abb_dict, site)
        print("JSON file has been updated with the newly created site-name")

    try:
        # Creating Working Directory and Copying the relevant template into the directory
        create_working_directory(temp_dict=abb_dict, working_directory=args.working_dir_name)

        file_destination = os.path.join(pf.read_config(sec='Base_Directories', ky='hackathon_parent_dir'),
                                        abb_dict.get(args.site_name_abbv), args.working_dir_name)
        copy_template(temp_dict=templates_dict, template_type=args.problem_type,
                      file_dest=str(file_destination+"\\"))

        print("Working Directory has been created and relevant template has been copied into the directory.",
              end='\n')

        # Template Renaming in the Working Directory
        old_ipynb_name = file_destination+"\\"+os.listdir(file_destination)[0]
        new_ipynb_name = file_destination+"\\"+args.workbook_name

        os.rename(old_ipynb_name, new_ipynb_name)

        # Moving the Data Files/Folder into the Directory and unzipping it
        files_and_folders = pf.MoveDatafold(targ_dt=args.target_date, targ_dir=file_destination)
        files_and_folders()

        print("Data Folder/Files have been moved into the Working Directory.", end='\n')

    except PermissionError:
        print("Template File has NO required permissions to be copied onto the Project Working Directory")
