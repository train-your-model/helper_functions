import os
import re
from zipfile import ZipFile


def unzip_data_fold():
    """
    Unzips the zipped data folder present in the current working directory

    :return: Unzipped data folder or contents of the data folder
    """
    for ind, f in enumerate(os.listdir(os.getcwd())):
        zfs = re.findall("zip\Z", f)
        if len(zfs)!=0:
            fold_ind = ind
            # Unzip and Display the contents of the zip folder
            z = ZipFile(os.listdir(os.getcwd())[fold_ind],'r')
            z.extractall()
            z.close()

