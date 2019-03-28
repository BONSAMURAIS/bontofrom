import json
from bontofrom.load_metadata import get_metadata
from pathlib import Path


output_dir = Path(__file__).parent / "output"


EXIOBASE_DOCKER = """
Please run the following to convert JSON-LD to TTL:

    cd "{0}"
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle bontofrom/output/flowobject.jsonld > bontofrom/output/flowobject.ttl
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle bontofrom/output/activitytype.jsonld > bontofrom/output/activitytype.ttl
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle bontofrom/output/location.jsonld > bontofrom/output/location.ttl
""".format((Path(__file__).parent.parent).absolute())


class Converter:
    def __init__(self, abbrev, full, filename, type_, metadata):
        self.context = {
                "bont" : "http://ontology.bonsai.uno/core#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "gn": "http://sws.geonames.org/",
                "schema": "http://schema.org/",
        }
        self.context.update({abbrev: full})
        self.metadata = metadata
        self.filename = filename
        self.type_ = type_

    def substitute(self, string):
        for k, v in self.context.items():
            string = string.replace(v, k + ":")
        return string

    def get_data(self):
        data = {
            "@context": self.context,
            "@graph": []
        }
        for name, uri in self.metadata[self.filename].items():
            data['@graph'].append({
                '@id': self.substitute(uri),
                "@type" : self.type_,
                "rdfs:label": name,
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

    location = Converter(
        "brdfl",
        "http://rdf.bonsai.uno/location/exiobase3_3_17/",
        "location",
        "schema:Place",
        metadata,
    )
    location.write_file()

    print(EXIOBASE_DOCKER)
    pass
