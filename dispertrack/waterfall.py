import json
from pathlib import Path

import h5py
import numpy as np


def create_waterfall(data_filename, out_filename, axis=1):
    """ Reads the data and creates a waterfall by adding all the pixels in the vertical direction."""
    input_path = Path(data_filename)
    input_filename = input_path.name

    if not input_path.is_file():
        raise Exception(f'The specified path {data_filename} does not exist')
    output_path = Path(out_filename)
    directory = output_path.parents[0]
    directory.mkdir(exist_ok=True)

    with h5py.File(data_filename, 'r') as data:
        metadata = json.loads(data['data']['metadata'][()].decode())
        timelapse = data['data']['timelapse']
        movie_data = timelapse[:, :, :metadata['frames']]
        waterfall = np.sum(movie_data, axis)

    with h5py.File(out_filename, "a") as f:
        group = f.create_group(input_filename)
        group.create_dataset('waterfall', data=waterfall)