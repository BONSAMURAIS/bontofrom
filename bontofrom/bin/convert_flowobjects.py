import json
from bontofrom.load_metadata import metadata

def main():
    s = lambda x: x.replace("http://rdf.bonsai.uno/flowobject/exiobase3_3_17/", "brdffo:")

    data = {
        "@context": {
            "bont" : "http://ontology.bonsai.uno/core#",
            "brdffo" : "http://rdf.bonsai.uno/flowobject/exiobase3_3_17/",
        },
        "@graph": []
    }

    for name, uri in metadata['flow object'].items():
        data['@graph'].append({
            '@id': s(uri),
            "@type" : "bont:FlowObject",
            "label": name,
        })

    with open("flowobject.jsonld", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Convert to TTL:\ndocker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle flowobject.jsonld > flowobject.ttl")

if __name__ == "__main__":
    main()
