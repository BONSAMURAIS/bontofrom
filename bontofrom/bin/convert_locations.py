import json
from bontofrom.load_metadata import metadata

s = lambda x: x.replace("http://rdf.bonsai.uno/activitytype/exiobase3_3_17/", "brdfat:")

data = {
    "@context": {
        "bont" : "http://ontology.bonsai.uno/core#",
        "brdfat" : "http://rdf.bonsai.uno/activitytype/exiobase3_3_17/",
    },
    "@graph": []
}

for name, uri in metadata['activity type'].items():
    data['@graph'].append({
        '@id': s(uri),
        "@type" : "bont:ActivityType",
        "label": name,
    })

with open("activitytype.jsonld", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
