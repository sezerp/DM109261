import requests
from tqdm.notebook import tqdm
from warnings import warn
import ntpath
from os import path


def download_data(url: str, target_path: str) -> None:
    file_name = ntpath.basename(target_path)
    if path.exists(target_path):
        warn(f'File {file_name} on {target_path} path is already exist.')
        return

    req = requests.get(url, stream=True)
    file_size = int(req.headers.get('content-length', 0))
    block_size = 1024 * 1024
    p_bar = tqdm(total=file_size, unit='iM', unit_scale=True)
    with open(target_path, 'wb') as f:
        for data in req.iter_content(block_size):
            p_bar.update(len(data))
            p_bar.set_description(f'Downloading: {file_name}')
            f.write(data)
    p_bar.close()
    if file_size != 0 and p_bar.n != file_size:
        warn("ERROR, something went wrong")
