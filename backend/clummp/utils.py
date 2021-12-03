import gzip 
import os 
import shutil

def dump_data(path): 
    """
    From: https://www.techiedelight.com/delete-all-files-directory-python/
    Delete all files in the given directory. 
    
    Params
    ------
    - `path`: the path to the directory as a string
    
    Returns
    ------
    None
    """

    for f in os.listdir(path):
        os.remove(os.path.join(path, f))


def unzip(file_path):
    """
    Unzips the given `.gz` file to the same directory as the file. 
    
    Params
    ------
    - `file_path`: path to file to unzip as a string
    
    Returns
    ------
    None
    """
    dirname = os.path.dirname(file_path)
    out_filename = os.path.basename(file_path).replace('.gz', '')
    print('Unzipping ' + file_path)
    # https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python#
    with gzip.open(file_path, 'rb') as f_in:
        with open(os.path.join(dirname, out_filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('Unzipped to ' + os.path.join(dirname, out_filename))
    return os.path.join(dirname, out_filename)

