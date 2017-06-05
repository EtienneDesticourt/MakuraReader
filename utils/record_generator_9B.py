import struct

from utils.record_9B import Record9B


class RecordGenerator9B(object):
    NUM_DUMMY_RECORDS = 1

    def __init__(self, f):
        self.file = f
        self.file.seek(self.NUM_DUMMY_RECORDS * Record9B.SIZE)
        self.current_record = self.NUM_DUMMY_RECORDS

    def __iter__(self):
        return self

    def __next__(self):
        raw = self.file.read(Record9B.SIZE)
        try:
        	record = Record9B(*struct.unpack('>2H4s504s64x', raw)) # See Record9B doc to understand unpacking string
        except struct.error:
        	raise StopIteration
        self.current_record += 1
        return record