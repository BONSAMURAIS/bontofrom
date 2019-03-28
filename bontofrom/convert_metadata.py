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
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle bontofrom/output/unit.jsonld > bontofrom/output/unit.ttl
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle bontofrom/output/time.jsonld > bontofrom/output/time.ttl
""".format((Path(__file__).parent.parent).absolute())


class Converter:
    def __init__(self, abbrev, full, filename, type_, metadata):
        self.context = {
                "bont" : "http://ontology.bonsai.uno/core#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "gn": "http://sws.geonames.org/",
                "schema": "http://schema.org/",
        }
        if abbrev:
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
                "@type": self.type_,
                "rdfs:label": name,
            })
        return data

    def write_file(self):
        with open(output_dir / (self.filename + ".jsonld"), "w", encoding='utf-8') as f:
            json.dump(self.get_data(), f,
                      ensure_ascii=False, indent=2)


class ProperInterval(Converter):
    def __init__(self, years):
        """``years`` is a list of integer years."""
        self.years = years
        self.filename = "time"

    def map_wikidata_year(self, year):
        MAPPING = {
            2011: "https://www.wikidata.org/wiki/Q1994",
            2015: "https://www.wikidata.org/wiki/Q2002",
            2016: "https://www.wikidata.org/wiki/Q25245",
            2017: "https://www.wikidata.org/wiki/Q25290",
            2018: "https://www.wikidata.org/wiki/Q25291",
        }
        return MAPPING[year]

    def get_data(self):
        data = {
            "@context" : {
                "years" : {
                    "@id" : "https://www.w3.org/TR/owl-time/years",
                    "@type" : "http://www.w3.org/2001/XMLSchema#integer"
                },
                "sameAs" : {
                    "@id" : "http://www.w3.org/2002/07/owl#sameAs",
                    "@type" : "@id"
                },
                "hasEnd" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasEnd",
                    "@type" : "@id"
                },
                "hasDurationDescription" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasDurationDescription",
                "@type" : "@id"
                },
                "hasBeginning" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasBeginning",
                    "@type" : "@id"
                },
                "inXSDDate" : {
                    "@id" : "https://www.w3.org/TR/owl-time/inXSDDate",
                    "@type" : "http://www.w3.org/2001/XMLSchema#date"
                },
                "brdftim" : "http://rdf.bonsai.uno/time/",
                "time" : "https://www.w3.org/TR/owl-time/",
                },
            "@graph": [{
                "@id" : "brdftim:oneyearlong",
                "@type" : "time:DurationDescription",
                "time:years" : 1
            }]
        }
        for year in self.years:
            data['@graph'].extend([{
                "@id": "brdftim:{}end".format(year),
                "@type": "time:Instant",
                "inXSDDate": "{}-12-31".format(year),
            }, {
                "@id": "brdftim:{}start".format(year),
                "@type": "time:Instant",
                "inXSDDate": "{}-01-01".format(year),
            }, {
                "@id": "brdftim:{}".format(year),
                "@type": "time:ProperInterval",
                "sameAs": [
                    self.map_wikidata_year(year),
                    "http://reference.data.gov.uk/doc/year/{}".format(year)
                ],
                "hasBeginning": "brdftim:{}start".format(year),
                "hasDurationDescription": "brdftim:oneyearlong",
                "hasEnd": "brdftim:{}end".format(year),
            }])
        return data


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

    unit = Converter(
        "om",
        "http://www.ontology-of-units-of-measure.org/resource/om-2/",
        "unit",
        "om:Unit",
        metadata,
    )
    unit.write_file()

    time = ProperInterval([2011, 2016, 2017, 2018])
    time.write_file()

    print(EXIOBASE_DOCKER)
    pass
