import json
import os
from typing import List, Tuple
from PIL import Image
from pathlib import Path


def load_data(input_dir: str) -> Tuple[List, List]:
    records: List = []
    not_found_list: List = []
    included_extensions = ['jpg', 'jpeg', 'bmp', 'png']
    file_names = [fn for fn in os.listdir(input_dir)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    fid = 1
    for _file in file_names:
        # print(os.path.join(input_dir, _file))
        filename = Path(_file)
        filename_json_ext = os.path.join(input_dir, filename.with_suffix('.json'))

        if not os.path.isfile(filename_json_ext):
            not_found_list.append(filename_json_ext)
            continue

        record = {
            "id": fid,
            "file": os.path.join(input_dir, _file),
            "json": filename_json_ext,
            "isReviewed": True,
            "error": 0
        }
        records.append(record)
        fid += 1

    return records, not_found_list
