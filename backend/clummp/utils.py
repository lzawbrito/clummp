import gzip 
import os 
import shutil

def dump_data(path): 
    """
    https://www.techiedelight.com/delete-all-files-directory-python/
    """

    for f in os.listdir(path):
        os.remove(os.path.join(path, f))



def unzip(file_path):
    dirname = os.path.dirname(file_path)
    out_filename = os.path.basename(file_path).replace('.gz', '')
    print('Unzipping ' + file_path)
    # https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python#
    with gzip.open(file_path, 'rb') as f_in:
        with open(os.path.join(dirname, out_filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('Unzipped to ' + os.path.join(dirname, out_filename))
    return os.path.join(dirname, out_filename)

