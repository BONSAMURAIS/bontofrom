import bz2
import json
from .exiobase_header import HEADER as GENERIC_HEADER


class StreamingCompressedJSONWriter:
    def __init__(self, filepath, header=GENERIC_HEADER):
        if not filepath.endswith(".json.bz2"):
            filepath += ".json.bz2"
        self.file = bz2.open(filepath, mode='at', compresslevel=9, encoding='utf-8')
        open(filepath, "a")
        self.file.write('{"@context": ')
        self.write_obj(GENERIC_HEADER["@context"])
        self.file.write('"@data": [')

    def write_obj(self, obj):
        """Write each element of a graph instance (activity, flow, or otherwise).

        Will write elements of a list separately"""
        if isinstance(obj, list):
            return [self.write_obj(elem) for elem in obj]

        self.file.write(json.dumps(obj, ensure_ascii=False) + ",\n")

    def finish(self):
        self.file.write("]\n}")
        self.file.close()
