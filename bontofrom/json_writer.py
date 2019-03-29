import bz2
import json
from .exiobase_header import HEADER as GENERIC_HEADER


class StreamingCompressedJSONWriter:
    def __init__(self, filepath, header=GENERIC_HEADER):
        self._first_object = None
        if not filepath.endswith(".jsonld.bz2"):
            filepath += ".jsonld.bz2"
        self.file = bz2.open(filepath, mode='at', compresslevel=9, encoding='utf-8')
        open(filepath, "a")
        self.file.write('{"@context": ')
        self.write_obj(GENERIC_HEADER["@context"], header=True)
        self.file.write('"@data": [')

    def write_obj(self, obj, header=False):
        """Write each element of a graph instance (activity, flow, or otherwise).

        Will write elements of a list separately"""
        if isinstance(obj, list):
            return [self.write_obj(elem) for elem in obj]

        if self._first_object is None and not header:
            self._first_object = obj
            return

        self.file.write(json.dumps(obj, ensure_ascii=False) + ",\n")

    def finish(self):
        self.file.write(json.dumps(self._first_object, ensure_ascii=False))
        self.file.write("]\n}")
        self.file.close()
