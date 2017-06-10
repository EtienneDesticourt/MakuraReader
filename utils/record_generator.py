import struct


class RecordGenerator(object):

    def __init__(self, f, Record, num_dummy_records=0):
        self.num_dummy_records = num_dummy_records
        self.Record = Record
        self.file = f
        self.file.seek(self.num_dummy_records * self.Record.SIZE)
        self.current_record = self.num_dummy_records

    def __iter__(self):
        return self

    def __next__(self):
        raw = self.file.read(self.Record.SIZE)
        try:
            record = self.Record(*struct.unpack(self.Record.STRUCTURE, raw))
        except struct.error:
            raise StopIteration
        self.current_record += 1
        return record
        