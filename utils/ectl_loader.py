import numpy as np

from utils.record_9B import Record9B
from utils.record_1C import Record1C
from utils.record_generator import RecordGenerator
from utils.simple_verbose_counter import SimpleVerboseCounter

def load_data(file_path, process_image=lambda x: x, truncate=0):
    count = SimpleVerboseCounter(period=24000, message="Loaded {} total. {} elapsed since last.")

    x = []
    labels = []
    with open(file_path, "rb") as f:
        for record in RecordGenerator(f, Record9B, num_dummy_records=1):
            image = process_image(record.image)
            image_array = np.asarray(image.getdata()).reshape(image.size)
            x.append(image_array)
            labels.append(record.JIS_code)

            if truncate and count >= truncate: break
            count()

    x = np.asarray(x, dtype=np.uint8)[:, :, :, np.newaxis]
    y = np.asarray(labels, dtype=np.int32)

    return x, y
