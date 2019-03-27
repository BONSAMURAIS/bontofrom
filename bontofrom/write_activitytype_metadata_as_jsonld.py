import json
from .load_metadata import metadata

data = {
    "@context": {
        "bont" : "http://ontology.bonsai.uno/core#",
        "brdfat" : "http://rdf.bonsai.uno/activitytype/#",
    },
    "@graph": []
}

for name, uri in metadata['activity type'].items():
    data['@graph'].append({
        '@id': uri,
        "@type" : "bont:ActivityType",
        "label": name,
    })


with open("activitytype.jsonld", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
