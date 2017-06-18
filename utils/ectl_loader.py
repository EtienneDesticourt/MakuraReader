import numpy as np

from utils.record_generator import RecordGenerator
from utils.simple_verbose_counter import SimpleVerboseCounter

def load_data(file_path, Record, record_range=None, process_image=lambda x: x, truncate=0):
    count = SimpleVerboseCounter(period=10000, message="Loaded {} total. {} elapsed since last.")

    x = []
    labels = []
    with open(file_path, "rb") as f:
        records = RecordGenerator(f, Record, num_dummy_records=1)
        for i, record in enumerate(records):
            if record_range and i not in record_range: continue
            image = process_image(record.image)
            image_array = np.array(image).astype(np.uint8)
            x.append(image_array)
            labels.append(record.JIS_code)

            if truncate and count >= truncate: break
            count()

    x = np.asarray(x, dtype=np.uint8)[:, :, :, np.newaxis]
    y = np.asarray(labels, dtype=np.int32)

    return x, y
    