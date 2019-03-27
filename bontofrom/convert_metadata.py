import json
from bontofrom.load_metadata import get_metadata
from pathlib import Path


output_dir = Path(__file__).parent / "output"


EXIOBASE_DOCKER = """
Please run the following to convert JSON-LD to TTL:

    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle {0}flowobject.jsonld > {0}flowobject.ttl"
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle {0}activitytype.jsonld > {0}activitytype.ttl"
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle {0}location.jsonld > {0}location.ttl"
""".format(output_dir)


class Converter:
    def __init__(self, abbrev, full, filename, type_, metadata):
        self.abbrev = abbrev
        self.full = full
        self.metadata = metadata
        self.filename = filename
        self.type_ = type_

    def substitute(self, string):
        return string.replace(
            self.full,
            self.abbrev + ":"
        )

    def get_data(self):
        data = {
            "@context": {
                "bont" : "http://ontology.bonsai.uno/core#",
                self.abbrev : self.full,
            },
            "@graph": []
        }
        for name, uri in self.metadata[self.filename].items():
            data['@graph'].append({
                '@id': self.substitute(uri),
                "@type" : self.type_,
                "label": name,
            })
        return data

    def write_file(self):
        with open(output_dir / (self.filename + ".jsonld"), "w", encoding='utf-8') as f:
            json.dump(self.get_data(), f,
                      ensure_ascii=False, indent=2)



def convert_exiobase():
    metadata = get_metadata()

    flow_object = Converter(
        "brdffo",
        "http://rdf.bonsai.uno/flowobject/exiobase3_3_17/",
        "flowobject",
        "bont:FlowObject",
        metadata,
    )
    flow_object.write_file()

    activity_type = Converter(
        "brdfat",
        "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/",
        "activitytype",
        "bont:ActivityType",
        metadata,
    )
    activity_type.write_file()

    print(EXIOBASE_DOCKER)
    pass
